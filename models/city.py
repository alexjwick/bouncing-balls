from utils.weather import get_weather_data

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