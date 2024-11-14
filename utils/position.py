from config import SCREEN_HEIGHT, SCREEN_WIDTH

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