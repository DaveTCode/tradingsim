import math
import random


class Agent:

    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.vel = (0, 0)  # simulation distance units by simulation time
        self.acc = (0, 0)  # simulation distance units by simulation time
        self.name = name
        self.goods = {}

    def step(self, dt):
        self.x += dt * self.vel[0]
        self.y += dt * self.vel[1]
        self.vel = (self.acc[0] * dt + self.vel[0],
                    self.acc[1] * dt + self.vel[1])

    def distance_to_location(self, location):
        return math.sqrt((self.x - location.x) ** 2 + (self.y - location.y) ** 2)

    def __str__(self):
        return "{0} ({1},{2})".format(self.name, self.x, self.y)


class AgentGood:

    def __init__(self, good, amount, average_purchase_cost):
        self.good = good
        self.amount = amount
        self.average_purchase_cost = average_purchase_cost


class AgentAI:

    def __init__(self, agent):
        self.agent = agent
        self.last_known_costs = {}
        self.destination = None
        self.good_profit_per_item = 1  # Changes over time as the AI finds it can get more

    def act(self, simulation):
        if self.destination is None:
            self.destination = self._choose_purchase_destination(simulation)

    def _choose_sale_destination(self, simulation):
        def _score_unvisited_location(location):
            return (self.agent.distance_to_location(location) / simulation.max_distance)

        def _score_visited_location(location):
            goods_worth_selling = 0
            for good in self.last_known_costs.keys():
                if good in self.agent.goods.keys():
                    if self.last_known_costs[good] - self.agent.goods[good] > self.good_profit_per_item:
                        goods_worth_selling += 1

            return (self.agent.distance_to_location(location) / simulation.max_distance +
                    goods_worth_selling)

        weighted_locations = {location: 0 for location in simulation.locations.keys()}

        for location in simulation.location.keys():
            if location in self.last_known_costs.keys():
                weighted_locations[location] = _score_visited_location(location)
            else:
                weighted_locations[location] = _score_unvisited_location(location)

        sorted_locations = sorted(weighted_locations.items(), key=lambda x: x[1])
        index = 0
        while random.randint(0, 10) > 9:
            index = (index + 1) % len(sorted_locations)

        return sorted_locations[index]

    def _choose_purchase_destination(self, simulation):

