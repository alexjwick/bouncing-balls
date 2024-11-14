import argparse
import pygame
import concurrent.futures
from models.ball import Ball
from models.city import City
from models.city_ball import CityBall
from config import SCREEN_HEIGHT, SCREEN_WIDTH, FPS

def load_cities_from_file(file_path: str, has_headers: bool = False) -> list["City"]:
    """
    Loads cities from a CSV file containing city names, latitudes, and longitudes.

    Parameters
    ----------
    file_path : str
        the path to the CSV file containing city data
    
    Returns
    -------
    list[City]
        a list of City objects
    """
    cities = []
    with open(file_path, "r") as file:
        if has_headers:
            next(file)
        for line in file:
            name, latitude, longitude = line.strip().split(",")
            city = City(name, float(latitude), float(longitude))
            cities.append(city)
    return cities

def generate_balls(cities: list["City"]) -> list["Ball"]:
    """
    Generates a list of Ball objects such that each ball is randomly placed on the screen without overlapping.
    The color of the balls is dependent on the temperature, and the initial speed is dependent on the wind speed.

    Parameters
    ----------
    cities : list[City]
        a list of cities to generate balls for
    
    Returns
    -------
    list[Ball]
        a list of Ball objects
    """
    balls = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(CityBall, city) for city in cities]
        for future in concurrent.futures.as_completed(futures):
            try:
                ball = future.result()
                print(f"Created ball for {ball.city.name} ({ball.city.temperature}°F, {ball.city.wind_speed} mph)")
                balls.append(ball)
            except ValueError as e:
                print(e)
    return balls

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Simulate bouncing balls on a screen with weather data from cities")
    parser.add_argument("file_path", type=str, help="the path to the CSV file containing city data")
    args = parser.parse_args()

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Bouncing Balls")
    clock = pygame.time.Clock()

    # Load cities from a file
    print(f"Reading cities from {args.file_path}...")
    cities = load_cities_from_file(args.file_path, has_headers=True)
    print(f"Loaded {len(cities)} cities")
    print("Generating balls...")
    balls = generate_balls(cities)
    print(f"Generated {len(balls)} balls")
    print("Each ball represents a city. The color of the ball is based on the temperature, and the initial speed is based on the wind speed.")
    print("Starting simulation...")
    print("Press 'Esc' to exit or 'U' to update weather data")
    
    running = True

    with concurrent.futures.ThreadPoolExecutor() as executor:
        while running:
            screen.fill((0, 0, 0))

            # Update all balls concurrently
            futures = [executor.submit(ball.update) for ball in balls]
            concurrent.futures.wait(futures)

            # Check for collisions concurrently
            collision_futures = []
            for i, ball in enumerate(balls):
                for j in range(i + 1, len(balls)):
                    collision_futures.append(executor.submit(ball.collide, balls[j]))
            concurrent.futures.wait(collision_futures)

            # Draw all balls in the main thread
            for ball in balls:
                ball.draw(screen)

            pygame.display.flip()
            clock.tick(FPS)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_u:
                        weather_futures = [executor.submit(ball.update_weather) for ball in balls]
                        concurrent.futures.wait(weather_futures)
                        print("Updated weather data for all cities")
    
    pygame.quit()

if __name__ == "__main__":
    main()
