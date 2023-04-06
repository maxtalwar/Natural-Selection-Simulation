class Plant:
    def __init__(self, size, reproduction_rate, water_consumption):
        self.size = size
        self.reproduction_rate = reproduction_rate
        self.water_consumption = water_consumption

class Herbivore:
    def __init__(self, size, speed, reproduction_rate, food_consumption):
        self.size = size
        self.speed = speed
        self.reproduction_rate = reproduction_rate
        self.food_consumption = food_consumption

class Carnivore:
    def __init__(self, size, speed, reproduction_rate, food_consumption):
        self.size = size
        self.speed = speed
        self.reproduction_rate = reproduction_rate
        self.food_consumption = food_consumption
