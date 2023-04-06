import matplotlib.pyplot as plt
from environment import Cell

def simulate_cell(cell, time_steps):
    # Initialize lists to store weather states
    temperature = []
    humidity = []
    water = []
    precipitation_probability = []
    evaporation = []
    sunlight = []

    # Update cell state and store the values over time
    for _ in range(time_steps):
        # update the environment state
        cell.update_variables()

        temperature.append(cell.temperature)
        humidity.append(cell.humidity)
        water.append(cell.water)
        precipitation_probability.append(cell.precipitation_probability)
        evaporation.append(cell.evaporation)
        sunlight.append(cell.sunlight)

        print(f"Temp: {round(cell.temperature, 2)}\n Humidity: {round(cell.humidity, 2)}\n Water: {round(cell.water, 2)}\n Precipitation Prob.: {round(cell.precipitation_probability, 2)}\n Evaporation: {round(cell.evaporation, 3)}\n Sunlight: {round(cell.sunlight, 2)} \n")

    return {
        "temperature": temperature,
        "humidity": humidity,
        "water": water,
        "precipitation_probability": precipitation_probability,
        "evaporation": evaporation,
        "sunlight": sunlight
    }




def plot_weather_states(states):
    plt.figure()

    plt.subplot(3, 2, 1)
    plt.plot(states["temperature"])
    plt.title("Temperature")

    plt.subplot(3, 2, 2)
    plt.plot(states["humidity"])
    plt.title("Humidity")

    plt.subplot(3, 2, 3)
    plt.plot(states["water"])
    plt.title("Water")

    plt.subplot(3, 2, 4)
    plt.plot(states["precipitation_probability"])
    plt.title("Precipitation Probability")

    plt.subplot(3, 2, 5)
    plt.plot(states["evaporation"])  # Add a subplot for evaporation
    plt.title("Evaporation")

    plt.subplot(3, 2, 6)
    plt.plot(states["sunlight"])  # Add a subplot for evaporation
    plt.title("Sunlight")

    plt.tight_layout()
    plt.show()



# Initialize a Cell instance with random values
cell = Cell(
    water=100, 
    temperature=20, 
    elevation=1000, 
    tick=0, 
    soil_nutrients=100, 
    sunlight=80, 
    humidity=60, 
    air_pressure=1000, 
    wind_speed=5
)

# Simulate the cell for 100 time steps
time_steps = 500
weather_states = simulate_cell(cell, time_steps)

# Plot the weather states over time
plot_weather_states(weather_states)
