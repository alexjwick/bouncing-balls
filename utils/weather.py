"""
File: weather.py
Author: Alexander Wick
Created: 2024-11-14
Copyright: GNU General Public License v3.0

Utility functions for retrieving weather data from the National Weather Service API.
"""

import requests

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
    return None, None