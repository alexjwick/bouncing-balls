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