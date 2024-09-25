import math
import pygame
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 20
GRAVITY = 0.1
AIR_RESISTANCE = 0.99
NUM_BALLS = 10
FPS = 60

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Bouncing Balls")
clock = pygame.time.Clock()

gravity_on = False
air_resistance_on = False

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
            dx: float,
            dy: float,
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
        dx : float, optional
            the x-velocity of the ball (default is random between -5 and 5)
        dy : float, optional
            the y-velocity of the ball (default is random between -5 and 5)
        
        Returns
        -------
        None
        """
        self.x: int = x
        self.y: int = y
        self.color: tuple[int, int, int] = color
        self.dx: float = dx
        self.dy: float = dy
    
    def update(self):
        # Apply gravity
        global gravity_on
        if gravity_on:
            self.dy += GRAVITY

        # Apply air resistance
        global air_resistance_on
        if air_resistance_on:
            self.dx *= AIR_RESISTANCE
            self.dy *= AIR_RESISTANCE

        # Update position
        self.x += self.dx
        self.y += self.dy

        # Bounce off walls
        if self.x - BALL_RADIUS < 0 or self.x + BALL_RADIUS > SCREEN_WIDTH:
            self.dx *= -1
        if self.y - BALL_RADIUS < 0 or self.y + BALL_RADIUS > SCREEN_HEIGHT:
            self.dy *= -1

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), BALL_RADIUS)
    
    def collide(self, other: "Ball"):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.hypot(dx, dy)
        if distance < 2 * BALL_RADIUS:
            self.dx *= -1
            self.dy *= -1
            other.dx *= -1
            other.dy *= -1


def main():
    balls: list[Ball] = [Ball(
        x=random.randint(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS),
        y=random.randint(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS),
        color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
        dx=random.uniform(-5, 5),
        dy=random.uniform(-5, 5),
    ) for _ in range(NUM_BALLS)]
    running: bool = True

    while running:
        screen.fill((0, 0, 0))

        for ball in balls:
            ball.update()
            ball.draw()
            for other in balls:
                if ball != other:
                    ball.collide(other)

        pygame.display.flip()
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()