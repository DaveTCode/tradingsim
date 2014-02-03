import math
import random
import tradingsim.configuration as configuration


class Agent:

    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.speed = configuration.AGENT_SPEED  # simulation distance units by simulation time
        self.name = name
        self.goods = {}
        self.money = configuration.INITIAL_AGENT_MONEY
        self.destination = None
        self.last_location = None

        self.ai = AgentAI(self)  # Owned by the agent but also holds a reference. 1-1 relationship

    def step(self, dt, simulation):
        vel = self.velocity()
        self.x += dt * vel[0]
        self.y += dt * vel[1]

        self.ai.act(simulation)  # TODO: Maybe don't call on every step.

    def velocity(self):
        if self.destination is None or (self.destination.x == self.x and
                                        self.destination.y == self.y):
            return (0, 0)
        else:
            dx = self.destination.x - self.x
            dy = self.destination.y - self.y
            theta = math.atan2(dx, dy)
            return (self.speed * math.sin(theta), self.speed * math.cos(theta))

    def distance_to_location(self, location):
        return math.sqrt((self.x - location.x) ** 2 + (self.y - location.y) ** 2)

    def is_dead(self):
        '''
            An agent is defined as dead if they have no money and no goods to sell.
        '''
        return self.money == 0 and len([good for good in self.goods.keys() if self.goods[good] == 0])

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
        self.last_sale_value = {}
        self.good_profit_per_item = 1  # Changes over time as the AI finds it can get more

    def act(self, simulation):
        if self.agent.destination is None:
            self.agent.destination = self._choose_purchase_destination(simulation)

    def _choose_sale_destination(self, simulation):
        def _score_unvisited_location(location):
            return (self.agent.distance_to_location(location) / simulation.max_distance)

        def _score_visited_location(location):
            '''
                A location is good to visit for sale if there is at least one
                good worth selling there.

                If there are no goods worth selling there and there are some
                goods NOT worth selling there then it is bad to visit.

                Currently no weighting given to potential profit.
            '''
            goods_worth_selling = 0
            goods_not_worth_selling = 0
            for good in self.last_known_costs.keys():
                if good in self.agent.goods.keys():
                    if self.last_known_costs[good] - self.agent.goods[good].average_purchase_cost > self.good_profit_per_item:
                        goods_worth_selling += 1
                    else:
                        goods_not_worth_selling += 1

            if goods_worth_selling > 0:
                return _score_unvisited_location(location) + goods_worth_selling
            else:
                return _score_unvisited_location(location) - goods_not_worth_selling

        weighted_locations = {location: 0 for location in simulation.locations}

        for location in weighted_locations.keys():
            if location in self.last_known_costs.keys():
                weighted_locations[location] = _score_visited_location(location)
            else:
                weighted_locations[location] = _score_unvisited_location(location)

        return self._choose_from_weighted_locations(weighted_locations)

    def _choose_purchase_destination(self, simulation):
        '''
            A purchase destination is good if there is a good there with a
            known cost that is low enough that we can make a profit on the
            most recent sale value.

            A purchase destination is bad if there are no goods worth buying
            and one or more goods not worth buying.
        '''
        def _score_unvisited_location(location):
            return (self.agent.distance_to_location(location) / simulation.max_distance)

        def _score_visited_location(location):
            goods_worth_buying = 0
            goods_not_worth_buying = 0
            for good, cost in self.last_known_costs[location].iteritems():
                if good in self.last_sale_value:
                    if self.last_sale_value - cost > self.good_profit_per_item:
                        goods_worth_buying += 1
                    else:
                        goods_not_worth_buying += 1

            if goods_worth_buying > 0:
                return _score_unvisited_location(location) + goods_worth_buying
            else:
                return _score_unvisited_location(location) + goods_not_worth_buying

        weighted_locations = {location: 0 for location in simulation.locations}

        for location in weighted_locations.keys():
            if location in self.last_known_costs.keys():
                weighted_locations[location] = _score_visited_location(location)
            else:
                weighted_locations[location] = _score_unvisited_location(location)

        return self._choose_from_weighted_locations(weighted_locations)

    def _choose_from_weighted_locations(self, locations):
        sorted_locations = sorted(locations.items(), key=lambda x: x[1])
        index = 0
        while random.randint(0, 10) > 9:
            index = (index + 1) % len(sorted_locations)

        return sorted_locations[index][0]
