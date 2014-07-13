import logging
import math
import random
import tradingsim.configuration as configuration
import tradingsim.utils as utils


class Agent:

    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.speed = configuration.AGENT_SPEED  # simulation distance units by simulation time
        self.name = name
        self.goods = {}
        self.money = configuration.INITIAL_AGENT_MONEY
        self.max_goods = configuration.AGENT_MAX_GOODS
        self.current_location = None
        self.destination = None
        self.last_location = None

        self.ai = AgentAI(self)  # Owned by the agent but also holds a reference. 1-1 relationship

    def step(self, dt, simulation):
        if self.is_dead():
            logging.debug("Agent {0} is dead".format(self.name))

        vel = self.velocity()

        next_x = self.x + dt * vel[0]
        next_y = self.y + dt * vel[1]

        if not self.destination is None and utils.is_point_on_line_segment(self.x, self.y, next_x, next_y, self.destination.x, self.destination.y):
            self.arrive()

        self.x = next_x
        self.y = next_y

        self.ai.act(simulation)  # TODO: Maybe don't call on every step.

    def velocity(self):
        if self.destination is None or (utils.are_points_nearly_equal(self.destination.x, self.x, self.destination.y, self.y)):
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

    def arrive(self):
        '''
            Called when the agent arrives at their destination.
        '''
        logging.debug("Agent {0} arrives at {1}".format(self.name, self.destination))
        self.x = self.destination.x
        self.y = self.destination.y

        self.ai.arrived(self.destination)

        self.current_location = self.destination
        self.destination = None

    def space_remaining(self):
        '''
            The amount of space remaining taking into account the goods
            already purchased.
        '''
        return self.max_goods - reduce(lambda x, y: x + y.amount,
                                       [good_amount for good, good_amount in self.goods.iteritems()],
                                       0)

    def total_goods(self):
        '''
            The total number of all goods in stock
        '''
        return reduce(lambda x, y: x + y.amount,
                      [good_amount for good, good_amount in self.goods.iteritems()],
                      0)

    def buy(self, destination, good, amount):
        '''
            Attempt to purchase the requested amount of goods.
        '''
        cost = good.purchase_cost(destination.goods_quantity[good], amount)
        if not good in self.goods.keys():
            self.goods[good] = AgentGood(good, amount, cost / amount)
        else:
            self.goods[good].amount += amount
            self.goods[good].average_purchase_cost = cost / amount

        self.money -= cost
        destination.goods_quantity[good] -= amount
        logging.debug("Agent {0} purchases {1} of {2} for {3} at {4}".format(self.name, amount, good, cost, destination))

    def sell(self, destination, good, amount):
        '''
            Attempt to sell the requested number of goods.
        '''
        cost = good.sale_cost(destination.goods_quantity[good], amount)

        self.goods[good].amount -= amount

        self.money += cost
        self.destination.goods_quantity[good] += amount
        logging.debug("Agent {0} sells {1} of {2} for {3} at {4}".format(self.name, amount, good, cost, destination))

    def set_destination(self, destination):
        self.destination = destination
        self.last_location = self.current_location
        self.current_location = None

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
        self.good_profit_per_item = 1  # Changes over time as the AI finds it can get more. TODO

    def act(self, simulation):
        if self.agent.destination is None:
            if self.agent.last_location is None:
                self.agent.set_destination(self._choose_purchase_destination(simulation))
            else:
                if self.agent.space_remaining() > self.agent.total_goods():
                    self.agent.set_destination(self._choose_purchase_destination(simulation))
                else:
                    self.agent.set_destination(self._choose_sale_destination(simulation))

    def arrived(self, destination):
        def _maybe_sell(destination):
            agent_goods = {good: value for good, value in self.agent.goods.iteritems() if value.amount > 0}

            if len(agent_goods) == 0:
                return False
            else:
                for good, good_amount in agent_goods.iteritems():
                    for num_to_sell in range(good_amount.amount, 1, -1):
                        if good.sale_cost(destination.goods_quantity[good], num_to_sell) > good_amount.average_purchase_cost:
                            self.agent.sell(destination, good, num_to_sell)
                            break

        def _maybe_buy(destination):
            for good in [good for good, amount in destination.goods_quantity.iteritems() if amount > 0]:
                space_remaining = self.agent.space_remaining()

                actual_num_to_buy = 0
                for possible_num_to_buy in range(1, space_remaining):
                    cost_to_buy = good.purchase_cost(destination.goods_quantity[good], possible_num_to_buy)
                    cost_per_item = int(math.ceil(cost_to_buy / possible_num_to_buy))
                    if cost_to_buy > self.agent.money:
                        # Stop buying if we run out of money
                        break
                    elif possible_num_to_buy > destination.goods_quantity[good]:
                        # Destination doesn't have any more so stop buying.
                        break
                    elif good in self.last_sale_value.keys():
                        if cost_per_item > self.last_sale_value[good]:
                            # Stop buying if it is now more expensive than the last time we sold.
                            break
                    elif good in self.last_known_costs.keys():
                        if cost_per_item > self.last_known_costs[good]:
                            # Stop buying if it is now more expensive than the last time we bought.
                            break
                    else:
                        actual_num_to_buy = possible_num_to_buy

                if actual_num_to_buy > 0:
                    self.agent.buy(destination, good, actual_num_to_buy)

        _maybe_sell(destination)
        _maybe_buy(destination)

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

        weighted_locations = {location: 0 for location in simulation.locations if location != self.agent.current_location}

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
                    if self.last_sale_value[good] - cost > self.good_profit_per_item:
                        goods_worth_buying += 1
                    else:
                        goods_not_worth_buying += 1

            if goods_worth_buying > 0:
                return _score_unvisited_location(location) + goods_worth_buying
            else:
                return _score_unvisited_location(location) + goods_not_worth_buying

        weighted_locations = {location: 0 for location in simulation.locations if location != self.agent.current_location}

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
