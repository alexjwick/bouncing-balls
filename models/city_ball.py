import random
from models.ball import Ball
from models.city import City
from utils.color import fahrenheit_to_rgb
from utils.position import get_position_on_screen

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