import math
import pygame
import random
import concurrent.futures
import requests
import argparse

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 10
NUM_BALLS = 50
FPS = 30

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Bouncing Balls")
clock = pygame.time.Clock()

class Ball:
    """
    A class to represent a ball.

    Attributes
    ----------
    x : int
        the x-coordinate of the ball
    y : int
        the y-coordinate of the ball
    color : tuple[int, int, int]
        the color of the ball in RGB format
    dx : float
        the x-velocity of the ball
    dy : float
        the y-velocity of the ball
    """

    def __init__(
            self,
            x: int,
            y: int,
            color: tuple[int, int, int],
            initial_speed: float,
            initial_angle: float
        ):
        """
        Constructs all the necessary attributes for the Ball object.

        Parameters
        ----------
        x : int, optional
            the x-coordinate of the ball (default is random anywhere on the screen)
        y : int, optional
            the y-coordinate of the ball (default is random anywhere on the screen)
        color : tuple[int, int, int], optional
            the color of the ball in RGB format (default is random)
        initial_speed : float
            the initial speed of the ball
        initial_angle : float
            the initial angle of the ball in degrees
        
        Returns
        -------
        None
        """
        self.x: int = x
        self.y: int = y
        self.color: tuple[int, int, int] = color
        self.dx: float = initial_speed * math.cos(math.radians(initial_angle))
        self.dy: float = initial_speed * math.sin(math.radians(initial_angle))
    
    def update(self):
        """
        Updates the position of the ball based on its velocity and acceleration.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        # Update position
        self.x += self.dx
        self.y += self.dy

        # Bounce off walls
        if self.x - BALL_RADIUS < 0 or self.x + BALL_RADIUS > SCREEN_WIDTH:
            self.dx *= -1
        if self.y - BALL_RADIUS < 0 or self.y + BALL_RADIUS > SCREEN_HEIGHT:
            self.dy *= -1

    def draw(self):
        """
        Draws the ball on the screen.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        pygame.draw.circle(screen, self.color, (self.x, self.y), BALL_RADIUS)
    
    def is_colliding(self, other: "Ball") -> bool:
        """
        Checks if the ball is colliding with another ball.

        Parameters
        ----------
        other : Ball
            the other ball to check for a collision with

        Returns
        -------
        bool
            True if the balls are colliding, False otherwise
        """
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.hypot(dx, dy)
        return distance < 2 * BALL_RADIUS
    
    def collide(self, other: "Ball"):
        """
        Checks for a collision with another ball and updates velocities accordingly.

        Parameters
        ----------
        other : Ball
            the other ball to check for a collision with

        Returns
        -------
        None
        """
        if self.is_colliding(other):
            # Swap velocities for a basic collision response
            self.dx, other.dx = other.dx, self.dx
            self.dy, other.dy = other.dy, self.dy

class City:
    """
    A class to represent a city.

    Attributes
    ----------
    name : str
        the name of the city
    latitude : float
        the latitude of the city
    longitude : float
        the longitude of the city
    """

    def __init__(self, name: str, latitude: float, longitude: float):
        """
        Constructs all the necessary attributes for the City object.

        Parameters
        ----------
        name : str
            the name of the city
        latitude : float
            the latitude of the city
        longitude : float
            the longitude of the city
        
        Returns
        -------
        None
        """
        self.name: str = name
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.temperature: int = 0
        self.wind_speed: int = 0
        self.update_weather()
    
    def get_current_weather(self) -> tuple[int, int]:
        """
        Gets the current temperature and wind speed for the city.

        Parameters
        ----------
        None

        Returns
        -------
        tuple[int, int]
            a tuple containing the current temperature and wind speed
        """
        return get_weather_data(self.latitude, self.longitude)
    
    def update_weather(self):
        """
        Updates the weather data for the city.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.temperature, self.wind_speed = self.get_current_weather()

class CityBall(Ball):
    """
    A class to represent a ball that is associated with a city.

    Attributes
    ----------
    city : City
        the city associated with the ball
    """

    def __init__(self, city: "City"):
        """
        Constructs all the necessary attributes for the CityBall object.

        Parameters
        ----------
        city : City
            the city associated with the ball
        
        Returns
        -------
        None

        Raises
        ------
        ValueError
            if the weather data for the city cannot be retrieved
        """
        self.city = city
        temperature, wind_speed = city.temperature, city.wind_speed
        if temperature is None or wind_speed is None:
            raise ValueError(f"Failed to get weather data for {city.name}")
        # X and Y coordinates are calculated based on the city's latitude and longitude within the continental US
        x, y = get_position_on_screen(city.latitude, city.longitude)
        color = fahrenheit_to_rgb(temperature)
        initial_speed = wind_speed / 3
        initial_angle = random.uniform(0, 360)
        super().__init__(x, y, color, initial_speed, initial_angle)

    def update_weather(self):
        """
        Updates the weather data for the city associated with the ball.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.city.update_weather()
        self.color = fahrenheit_to_rgb(self.city.temperature)

def get_position_on_screen(latitude: float, longitude: float) -> tuple[int, int]:
    """
    Converts a latitude and longitude to an (x, y) position on the screen.

    Parameters
    ----------
    latitude : float
        the latitude of the location
    longitude : float
        the longitude of the location

    Returns
    -------
    tuple[int, int]
        a tuple containing the x and y coordinates on the screen
    """
    # X and Y coordinates are calculated based on the city's latitude and longitude within the continental US
    min_latitude = 25
    max_latitude = 50
    min_longitude = -125
    max_longitude = -65
    x = int((longitude - min_longitude) / (max_longitude - min_longitude) * SCREEN_WIDTH)
    y = int((1 - (latitude - min_latitude) / (max_latitude - min_latitude)) * SCREEN_HEIGHT)
    return x, y

def get_weather_data(latitude: float, longitude: float) -> tuple[int, int]:
    """
    Gets the current temperature and wind speed for a given latitude and longitude.

    Parameters
    ----------
    latitude : float
        the latitude of the location
    longitude : float
        the longitude of the location
    
    Returns
    -------
    tuple[int, int]
        a tuple containing the current temperature and wind speed
    """
    api_url = f"https://api.weather.gov/points/{latitude},{longitude}"

    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        forecast_url = data['properties']['forecast']
        
        forecast_response = requests.get(forecast_url)
        if forecast_response.status_code == 200:
            forecast_data = forecast_response.json()
            current_forecast = forecast_data['properties']['periods'][0]
            
            temperature = current_forecast['temperature']
            wind_speed = current_forecast['windSpeed']
            
            return int(temperature), int(wind_speed.split()[0])
        else:
            return None, None
    else:
        return None, None
    
def fahrenheit_to_rgb(fahrenheit: int) -> tuple[int, int, int]:
    """
    Converts a temperature in Fahrenheit to an RGB value using a rainbow palette.
    The temperature range is mapped from 0°F (blue) to 100°F (red).

    Parameters
    ----------
    fahrenheit : int
        the temperature in Fahrenheit

    Returns
    -------
    tuple[int, int, int]
        a tuple containing the red, green, and blue values for the color
    """
    min_temp = 0
    max_temp = 100
    
    if fahrenheit < min_temp:
        fahrenheit = min_temp
    elif fahrenheit > max_temp:
        fahrenheit = max_temp

    normalized_temp = (fahrenheit - min_temp) / (max_temp - min_temp)

    if normalized_temp <= 0.2:
        # Blue to Cyan transition
        blue_value = 255
        green_value = int(normalized_temp * 5 * 255)
        red_value = 0
    elif normalized_temp <= 0.4:
        # Cyan to Green transition
        blue_value = int((0.4 - normalized_temp) * 5 * 255)
        green_value = 255
        red_value = 0
    elif normalized_temp <= 0.6:
        # Green to Yellow transition
        blue_value = 0
        green_value = 255
        red_value = int((normalized_temp - 0.4) * 5 * 255)
    elif normalized_temp <= 0.8:
        # Yellow to Orange transition
        blue_value = 0
        green_value = int((0.8 - normalized_temp) * 5 * 255)
        red_value = 255
    else:
        # Orange to Red transition
        blue_value = 0
        green_value = 0
        red_value = 255

    return (red_value, green_value, blue_value)

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

def main():
    parser = argparse.ArgumentParser(description="Simulate bouncing balls on a screen with weather data from cities")
    parser.add_argument("file_path", type=str, help="the path to the CSV file containing city data")
    args = parser.parse_args()

    # Load cities from a file
    print(f"Loading cities from {args.file_path}...")
    cities = load_cities_from_file(args.file_path, has_headers=True)
    print(f"Loaded {len(cities)} cities")
    print("Generating balls...")
    balls = generate_balls(cities)
    print(f"Generated {len(balls)} balls")
    
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
                ball.draw()

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
