import math
import pygame
import random
import concurrent.futures
import requests

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
    A class to represent a ball in the Bouncing Balls game.

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

def get_weather_data(latitude, longitude):
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
            
            return temperature, wind_speed
        else:
            return None, None
    else:
        return None, None
    
def generate_balls() -> list[Ball]:
    """
    Generates a list of Ball objects such that each ball is randomly placed on the screen without overlapping.
    """
    balls = []
    for _ in range(NUM_BALLS):
        x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
        y = random.randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        initial_speed = 5
        initial_angle = random.uniform(0, 360)
        ball = Ball(x, y, color, initial_speed, initial_angle)
        for other_ball in balls:
            while ball.is_colliding(other_ball):
                ball.x = random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
                ball.y = random.randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)
        balls.append(ball)
    return balls

def main():
    latitude = 37.7749
    longitude = -122.4194
    temperature, wind_speed = get_weather_data(latitude, longitude)
    print(f"Temperature: {temperature}°F")
    print(f"Wind Speed: {wind_speed}")
    balls = generate_balls()
    
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
    
    pygame.quit()

if __name__ == "__main__":
    main()
