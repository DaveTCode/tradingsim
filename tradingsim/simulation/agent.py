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
        self.logger = logging.getLogger("root")

        self.ai = AgentAI(self)  # Owned by the agent but also holds a reference. 1-1 relationship

    def step(self, dt, simulation):
        if self.is_dead():
            self.logger.debug("Agent {0} is dead".format(self.name))

        vel = self.velocity()

        next_x = self.x + dt * vel[0]
        next_y = self.y + dt * vel[1]

        if self.destination is not None and utils.is_point_on_line_segment(self.x, self.y, next_x, next_y, self.destination.x, self.destination.y):
            self.arrive()

        self.x = next_x
        self.y = next_y

        self.ai.act(simulation)  # TODO: Maybe don't call on every step.

    def velocity(self):
        if self.destination is None or (utils.are_points_nearly_equal(self.destination.x, self.x, self.destination.y, self.y)):
            return 0, 0
        else:
            dx = self.destination.x - self.x
            dy = self.destination.y - self.y
            theta = math.atan2(dx, dy)

            return self.speed * math.sin(theta), self.speed * math.cos(theta)

    def distance_to_location(self, location):
        return math.sqrt((self.x - location.x) ** 2 + (self.y - location.y) ** 2)

    def is_dead(self):
        """
            An agent is defined as dead if they have no money and no goods to sell.
        """
        return self.money == 0 and len([good for good in self.goods.keys() if self.goods[good] == 0])

    def arrive(self):
        """
            Called when the agent arrives at their destination.
        """
        message = "Agent {0} arrives at {1} which has:  ".format(self.name, self.destination)
        for good, amount in self.destination.goods_quantity.items():
            message += "{0} of {1}, ".format(amount, good)

        self.logger.debug(message)

        self.x = self.destination.x
        self.y = self.destination.y

        self.ai.arrived(self.destination)

        self.current_location = self.destination
        self.destination = None

    def space_remaining(self):
        """
            The amount of space remaining taking into account the goods
            already purchased.
        """
        return self.max_goods - self.total_goods()

    def total_goods(self):
        """
            The total number of all goods in stock
        """
        total = 0
        for good_amount in self.goods.values():
            total += good_amount.amount

        return total

    def buy(self, destination, good, amount):
        """
            Attempt to purchase the requested amount of goods.
        """
        cost = good.purchase_cost(destination.goods_quantity[good], amount)
        if good not in self.goods.keys():
            self.goods[good] = AgentGood(good, amount, cost / amount)
        else:
            self.goods[good].amount += amount
            self.goods[good].average_purchase_cost = cost / amount  # TODO - This currently resets the average_purchase_cost to the new one which isn't quite right. Should be updating it instead if there are still that were bought at the old cost

        self.money -= cost
        destination.goods_quantity[good] -= amount

        self.logger.debug("Agent {0} purchases {1} of {2} for {3} at {4}".format(self.name, amount, good, cost, destination))

    def sell(self, destination, good, amount):
        """
            Attempt to sell the requested number of goods.
        """
        cost = good.sale_cost(destination.goods_quantity[good], amount)

        self.goods[good].amount -= amount

        self.money += cost
        self.destination.goods_quantity[good] += amount

        self.logger.debug("Agent {0} sells {1} of {2} for {3} at {4}".format(self.name, amount, good, cost, destination))

    def set_destination(self, destination):
        self.destination = destination
        self.last_location = self.current_location
        self.current_location = None

        message = "Agent {0} sets destination to {1}".format(self.name, destination)
        self.logger.debug(message)

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
            self.agent.logger.debug("Agent {0} has no current destination".format(self.agent.name))
            if self.agent.last_location is None:
                self.agent.set_destination(self._choose_purchase_destination(simulation))
            else:
                if self.agent.space_remaining() > self.agent.total_goods():
                    self.agent.set_destination(self._choose_purchase_destination(simulation))
                else:
                    self.agent.set_destination(self._choose_sale_destination(simulation))

    def arrived(self, destination):
        def _maybe_sell(dest):
            agent_goods = {good: value for good, value in self.agent.goods.items() if value.amount > 0}

            if len(agent_goods) == 0:
                self.agent.logger.debug("Agent {0} has nothing to sell".format(self.agent.name))
                return False
            else:
                for good, good_amount in agent_goods.items():
                    for num_to_sell in range(good_amount.amount, 1, -1):
                        if good.sale_cost(dest.goods_quantity[good], num_to_sell) > good_amount.average_purchase_cost * num_to_sell:
                            self.agent.sell(dest, good, num_to_sell)
                            break

        def _maybe_buy(dest):
            for good in [good for good, amount in dest.goods_quantity.items() if amount > 0]:
                space_remaining = self.agent.space_remaining()

                actual_num_to_buy = 0
                for possible_num_to_buy in range(1, space_remaining):
                    cost_to_buy = good.purchase_cost(dest.goods_quantity[good], possible_num_to_buy)
                    cost_per_item = int(math.ceil(cost_to_buy / possible_num_to_buy))
                    if cost_to_buy > self.agent.money:
                        # Stop buying if we run out of money
                        break
                    elif possible_num_to_buy > dest.goods_quantity[good]:
                        # Destination doesn't have any more so stop buying.
                        break
                    elif good in self.last_sale_value.keys():
                        if cost_per_item >= self.last_sale_value[good]:
                            # Stop buying if it is now more expensive than the last time we sold.
                            break
                    elif good in self.last_known_costs.keys():
                        if cost_per_item > self.last_known_costs[good]:
                            # Stop buying if it is now more expensive than the last time we bought.
                            break
                    else:
                        actual_num_to_buy = possible_num_to_buy

                if actual_num_to_buy > 0:
                    self.agent.buy(dest, good, actual_num_to_buy)

        _maybe_sell(destination)
        _maybe_buy(destination)

    def _choose_sale_destination(self, simulation):
        def _score_unvisited_location(loc):
            return self.agent.distance_to_location(loc) / simulation.max_distance

        def _score_visited_location(loc):
            """
                A location is good to visit for sale if there is at least one
                good worth selling there.

                If there are no goods worth selling there and there are some
                goods NOT worth selling there then it is bad to visit.

                Currently no weighting given to potential profit.
            """
            goods_worth_selling = 0
            goods_not_worth_selling = 0
            for good in self.last_known_costs.keys():
                if good in self.agent.goods.keys():
                    if self.last_known_costs[good] - self.agent.goods[good].average_purchase_cost > self.good_profit_per_item:
                        goods_worth_selling += 1
                    else:
                        goods_not_worth_selling += 1

            if goods_worth_selling > 0:
                return _score_unvisited_location(loc) + goods_worth_selling
            else:
                return _score_unvisited_location(loc) - goods_not_worth_selling

        weighted_locations = {location: 0 for location in simulation.locations if location != self.agent.current_location}

        for location in weighted_locations.keys():
            if location in self.last_known_costs.keys():
                weighted_locations[location] = _score_visited_location(location)
            else:
                weighted_locations[location] = _score_unvisited_location(location)

        self.agent.logger.debug("Choosing from {0} sale destinations".format(len(weighted_locations)))
        return self._choose_from_weighted_locations(weighted_locations)

    def _choose_purchase_destination(self, simulation):
        """
            A purchase destination is good if there is a good there with a
            known cost that is low enough that we can make a profit on the
            most recent sale value.

            A purchase destination is bad if there are no goods worth buying
            and one or more goods not worth buying.
        """
        def _score_unvisited_location(loc):
            return self.agent.distance_to_location(loc) / simulation.max_distance

        def _score_visited_location(loc):
            goods_worth_buying = 0
            goods_not_worth_buying = 0
            for good, cost in self.last_known_costs[loc].items():
                if good in self.last_sale_value:
                    if self.last_sale_value[good] - cost > self.good_profit_per_item:
                        goods_worth_buying += 1
                    else:
                        goods_not_worth_buying += 1

            if goods_worth_buying > 0:
                return _score_unvisited_location(loc) + goods_worth_buying
            else:
                return _score_unvisited_location(loc) + goods_not_worth_buying

        weighted_locations = {location: 0 for location in simulation.locations if location != self.agent.current_location}

        for location in weighted_locations.keys():
            if location in self.last_known_costs.keys():
                weighted_locations[location] = _score_visited_location(location)
            else:
                weighted_locations[location] = _score_unvisited_location(location)

        return self._choose_from_weighted_locations(weighted_locations)

    @staticmethod
    def _choose_from_weighted_locations(locations):
        sorted_locations = sorted(locations.items(), key=lambda x: x[1])
        index = 0
        while random.randint(0, 10) > 9 and index < len(sorted_locations):
            index = (index + 1) % len(sorted_locations)

        return sorted_locations[index][0]
