from environment import Environment
from organisms import Plant, Herbivore, Carnivore
import time

def run_simulation(environment, plants, herbivores, carnivores):
    try:
        while True:
            # Update environment
            environment.update()

            # Update plants
            for plant in plants:
                plant.grow(environment)
                if plant.reproduce(environment):
                    plants.append(Plant(size=1, reproduction_rate=0.1, water_consumption=0.05))
            
            # Update herbivores
            for herbivore in herbivores:
                herbivore.search_food(plants)
                herbivore.eat()
                if herbivore.reproduce():
                    herbivores.append(Herbivore(size=1, speed=1, reproduction_rate=0.05, food_consumption=0.1))

            # Update carnivores
            for carnivore in carnivores:
                carnivore.hunt(herbivores)
                carnivore.eat()
                if carnivore.reproduce():
                    carnivores.append(Carnivore(size=2, speed=2, reproduction_rate=0.03, food_consumption=0.2))

            # Print the current state of the ecosystem
            print(f"Plants: {len(plants)}, Herbivores: {len(herbivores)}, Carnivores: {len(carnivores)}")

            # Add a delay between iterations (1 second in this example)
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nSimulation stopped by the user.")


def main():
    # Initialize environment
    environment = Environment(food=1000, water=1000, temperature=25)

    # Initialize plants, herbivores, and carnivores
    plants = [Plant(size=1, reproduction_rate=0.1, water_consumption=0.05) for _ in range(50)]
    herbivores = [Herbivore(size=1, speed=1, reproduction_rate=0.05, food_consumption=0.1) for _ in range(25)]
    carnivores = [Carnivore(size=2, speed=2, reproduction_rate=0.03, food_consumption=0.2) for _ in range(10)]

    # Run simulation
    run_simulation(environment, plants, herbivores, carnivores)

if __name__ == "__main__":
    main()
