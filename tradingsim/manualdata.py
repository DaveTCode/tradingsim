import random

import configuration
from simulation.simulation import Simulation
from simulation.goods import Goods
from simulation.location import Location


def create_simulation():
    def create_goods(simulation):
        simulation.goods.append(Goods("A",
                                      random.randint(10, 200),
                                      random.randint(0, 10),
                                      random.randint(1, 10)))
        simulation.goods.append(Goods("B",
                                      random.randint(10, 200),
                                      random.randint(0, 10),
                                      random.randint(1, 10)))
        simulation.goods.append(Goods("C",
                                      random.randint(10, 200),
                                      random.randint(0, 10),
                                      random.randint(1, 10)))
        simulation.goods.append(Goods("D",
                                      random.randint(10, 200),
                                      random.randint(0, 10),
                                      random.randint(1, 10)))

    def create_locations(simulation):
        for ii in range(0, random.randint(10, 20)):
            x = random.randint(0, simulation.width)
            y = random.randint(0, simulation.height)

            location = Location(str(ii), x, y)
            for goods in simulation.goods:
                location.goods_creation_rate[goods] = random.randint(0, 10) / 10
                location.goods_consumption_rate[goods] = random.randint(0, 10) / 10

            simulation.locations.append(location)

    simulation = Simulation(configuration.SIMULATION_STEP_MS,
                            configuration.SIMULATION_WIDTH,
                            configuration.SIMULATION_HEIGHT)
    create_goods(simulation)

    create_locations(simulation)

    return simulation
