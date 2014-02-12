import random

import tradingsim.configuration as configuration
from tradingsim.simulation.agent import Agent
from tradingsim.simulation.goods import Goods
from tradingsim.simulation.location import Location
from tradingsim.simulation.simulation import Simulation


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
                location.goods_creation_rate[goods] = random.randint(0, 10) / 10.0
                location.goods_consumption_rate[goods] = random.randint(0, 10) / 10.0

            simulation.locations.append(location)

    def create_agents(simulation):
        for ii in range(0, random.randint(configuration.MIN_AGENTS, configuration.MAX_AGENTS)):
            x = random.randint(0, simulation.width)
            y = random.randint(0, simulation.height)

            agent = Agent(str(ii), x, y)

            simulation.agents.append(agent)

    simulation = Simulation(configuration.SIMULATION_WIDTH,
                            configuration.SIMULATION_HEIGHT,
                            configuration.BASE_MS_TO_MINUTES)
    create_goods(simulation)

    create_locations(simulation)

    create_agents(simulation)

    return simulation
