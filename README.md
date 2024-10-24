# bouncing-balls

## To run:

```bash
source venv/bin/activate
python main.py
```

## "Adding new features" assignment

I augmented my bouncing balls program to be a visualization of the weather of US
cities. The program takes in a list of cities and gets the current weather of
each city. The temperature of each city is represented by the color of the ball,
with the color being a gradient from blue to red. The wind speed of each city is
represented by the initial speed of the ball, with the speed being proportional
to the wind speed. The balls bounce around the screen and collide with each
other. This program can theoretically be used to visualize the weather of any
number of cities, but I currently have 50 cities in the csv file that I use to
get the weather data. I use concurrent.futures to generate each ball and request
each city's weather data concurrently, which performs much faster than if I were
to request each city's weather data sequentially. I also use concurrent.futures
to update the position of each ball concurrently.
