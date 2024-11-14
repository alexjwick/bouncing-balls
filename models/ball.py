import math
import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, BALL_RADIUS

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

    def draw(self, screen: pygame.Surface):
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