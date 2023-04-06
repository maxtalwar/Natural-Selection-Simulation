import random, math

class Cell:
    OPTIMAL_TEMPERATURE = 20
    OPTIMAL_ELEVATION = 2000
    ELEVATION_RANGE = 3000
    OPTIMAL_PRESSURE = 1000
    OPTIMAL_WIND_SPEED = 5
    NUTRIENT_GAIN = 1
    PLANT_WATER_CONSUMPTION = 0.5
    PLANT_NUTRIENT_CONSUMPTION = 0.5
    MAX_WIND_SPEED = 15

    # TODO: add spring, summer, and fall seasons

    def __init__(self, water, temperature, elevation, tick, soil_nutrients, sunlight, humidity, air_pressure, wind_speed):
        """
        Initialize the Cell with given environmental variables and organisms.
        """
        # cell resources
        self.water = water
        self.soil_nutrients = soil_nutrients
        
        # cell state traits
        self.tick = tick
        self.temperature = temperature
        self.elevation = elevation # always constant
        self.sunlight = sunlight
        self.humidity = humidity
        self.air_pressure = air_pressure # not yet dyanmic
        self.wind_speed = wind_speed # not yet dyanmic
        self.evaporation = 0
        self.precipitation_probability = self.calculate_precipitation_probability()
        self.max_water_capacity = self.calculate_max_water_capacity()

        # cell weather traits
        self.storm_effect = 0
        self.drought_effect = 0
        self.heatwave_effect = 0
        self.precipitation = 0

        # state of organisms in cell
        self.plants = []
        self.herbivores = []
        self.carnivores = []

    def update_variables(self, tick_duration=1):
        """
        Update all environmental variables in the cell for one time step.
        """
        self.update_temperature()
        self.update_water()
        self.update_humidity()
        self.update_soil_nutrients()
        self.update_sunlight()
        self.update_wind_speed()

        # Increment the tick value based on tick_duration
        self.tick += tick_duration


    def calculate_precipitation_probability(self):
        """
        Calculate the probability of precipitation based on environmental factors.
        """
        # Factor 1: Humidity (higher humidity increases precipitation probability)
        humidity_factor = self.humidity / 100

        # Factor 2: Temperature (e.g., precipitation is more likely in a specific temperature range)
        temperature_factor = max(0, 1 - abs(self.temperature - self.OPTIMAL_TEMPERATURE) / 40)

        # Factor 3: Elevation (e.g., precipitation is more likely at higher elevations)
        elevation_factor = 1 / (1 + math.exp(-(self.elevation - self.OPTIMAL_ELEVATION) / self.ELEVATION_RANGE))

        # Factor 4: Air pressure
        pressure_factor = max(0, 1 - abs(self.air_pressure - self.OPTIMAL_PRESSURE) / 200)

        # Factor 5: Wind patterns
        wind_factor = max(0, 1 - abs(self.wind_speed - self.OPTIMAL_WIND_SPEED) / 10)

        # Calculate the overall precipitation probability by combining the factors
        overall_probability = (humidity_factor + temperature_factor + elevation_factor +
                               pressure_factor + wind_factor) / 5

        # Add seasonal precipitation variation
        seasonal_precipitation_variation = 0.1
        annual_precipitation_period = 365
        winter_solstice_tick = 355
        precipitation_seasonal_factor = (1 + seasonal_precipitation_variation * math.cos(2 * math.pi * (self.tick - winter_solstice_tick) / annual_precipitation_period))
        overall_probability *= precipitation_seasonal_factor

        return overall_probability
    
    def calculate_max_water_capacity(self):
        base_capacity = 200
        elevation_factor = 1 - self.elevation / self.ELEVATION_RANGE
        return base_capacity * elevation_factor
    
    def update_soil_nutrients(self):
        """
        Update the soil nutrients availability based on nutrient gain and plant consumption.
        """
        # Calculate total plant nutrient consumption
        total_plant_nutrient_consumption = sum(plant.nutrient_consumption for plant in self.plants)

        # Calculate nutrient gain based on water availability (using a quadratic function)
        optimal_water = self.MAX_WATER / 2
        water_factor = 1 - ((self.water - optimal_water) / optimal_water) ** 2
        nutrient_gain = self.NUTRIENT_GAIN * water_factor

        # Update soil nutrients availability
        self.soil_nutrients = self.soil_nutrients + nutrient_gain - total_plant_nutrient_consumption

        # Ensure soil nutrients availability doesn't go below 0
        if self.soil_nutrients < 0:
            self.soil_nutrients = 0

    def update_water(self):
        # Calculate precipitation based on updated precipitation probability
        self.precipitation_probability = self.calculate_precipitation_probability()
        random_value = random.random()
        self.precipitation = 0  # Initialize precipitation value
        if random_value <= self.precipitation_probability:
            self.precipitation = random.uniform(0, 10)
        
        sunlight_factor = self.sunlight / 100

        # Calculate evaporation (e.g., based on temperature, sunlight, and humidity)
        self.evaporation = (self.temperature / 100) * (self.sunlight / 100) * (1 - self.humidity / 100) * (1 + self.wind_speed / self.MAX_WIND_SPEED)

        # Calculate plant consumption (e.g., fixed rate per plant)
        plant_consumption = self.PLANT_WATER_CONSUMPTION * len(self.plants)

        # Update water availability
        self.water = self.water + self.precipitation - self.evaporation - plant_consumption

        # Ensure water availability doesn't go below 0
        if self.water < 0:
            self.water = 0
        if self.water > self.max_water_capacity:
            self.water = self.max_water_capacity

        return self.evaporation  # Return evaporation value



    def update_temperature(self):
        # Introduce daily temperature fluctuation using a sine wave
        temperature_amplitude = 5
        temperature_mean = 20
        angular_frequency = 2 * math.pi / 24
        temperature_noise = random.gauss(0, 1.5)

        # Add seasonal temperature variation
        seasonal_temperature_variation = 10
        annual_temperature_period = 365
        winter_solstice_tick = 355
        temperature_mean -= seasonal_temperature_variation * math.cos(2 * math.pi * (self.tick - winter_solstice_tick) / annual_temperature_period)

        self.temperature = (temperature_mean +
                            temperature_amplitude * math.sin(angular_frequency * self.tick) +
                            temperature_noise)

    
    def update_humidity(self):
        # Increase humidity when there's precipitation
        self.humidity += self.precipitation / 20

        # Decrease humidity based on temperature, evaporation, and precipitation
        evaporation_factor = (self.temperature / 100) * (1 - self.humidity / 100)
        self.humidity -= evaporation_factor * 0.05

        # Introduce temperature-dependent carrying capacity for humidity
        carrying_capacity = max(0, 100 - abs(self.temperature - 20) * 2)

        # Ensure humidity stays within bounds (0 - carrying_capacity)
        if self.humidity < 0:
            self.humidity = 0
        elif self.humidity > carrying_capacity:
            self.humidity = carrying_capacity

    def update_sunlight(self):
        # Introduce daily sunlight fluctuation using a sine wave
        sunlight_amplitude = 20
        sunlight_mean = 80
        angular_frequency = 2 * math.pi / 24
        sunlight_noise = random.gauss(0, 5)

        # Add seasonal sunlight variation
        seasonal_sunlight_variation = 20
        annual_sunlight_period = 365
        winter_solstice_tick = 355
        sunlight_mean -= seasonal_sunlight_variation * math.cos(2 * math.pi * (self.tick - winter_solstice_tick) / annual_sunlight_period)

        self.sunlight = (sunlight_mean +
                         sunlight_amplitude * math.sin(angular_frequency * self.tick) +
                         sunlight_noise)
        

    def update_wind_speed(self):
        # Add random fluctuations to the wind speed
        wind_speed_noise = random.gauss(0, 2)  # You can adjust the standard deviation (e.g., 2) for larger fluctuations
        self.wind_speed += wind_speed_noise

        # Ensure wind speed stays within a reasonable range
        self.wind_speed = min(max(0, self.wind_speed), 15)