import math
import unittest
import tradingsim.configuration as configuration
from tradingsim.simulation.agent import Agent, AgentGood
from tradingsim.simulation.goods import Goods
from tradingsim.simulation.location import Location


class AgentTests(unittest.TestCase):

    def test_distance_function(self):
        location = Location("a", 100, 100)
        agent = Agent("a", 100, 100)

        self.assertAlmostEqual(agent.distance_to_location(location), 0.0)
        location.x = 101
        self.assertAlmostEqual(agent.distance_to_location(location), 1.0)
        location.x = 99
        self.assertAlmostEqual(agent.distance_to_location(location), 1.0)
        location.y = 99
        self.assertAlmostEqual(agent.distance_to_location(location), math.sqrt(2))

    def test_velocity_function(self):
        location = Location("a", 100, 100)
        agent = Agent("a", 100, 100)
        agent.destination = None

        self.assertAlmostEqual(agent.velocity(), (0, 0))
        agent.destination = location
        self.assertAlmostEqual(agent.velocity()[0], 0)
        self.assertAlmostEqual(agent.velocity()[1], 0)

        location.x = 101
        self.assertAlmostEqual(agent.velocity()[0], agent.speed)
        self.assertAlmostEqual(agent.velocity()[1], 0)

        location.y = 101
        location.x = 100
        self.assertAlmostEqual(agent.velocity()[0], 0)
        self.assertAlmostEqual(agent.velocity()[1], agent.speed)

        location.y = 100
        location.x = 99
        self.assertAlmostEqual(agent.velocity()[0], -1 * agent.speed)
        self.assertAlmostEqual(agent.velocity()[1], 0)

        location.x = 100
        location.y = 99
        self.assertAlmostEqual(agent.velocity()[0], 0)
        self.assertAlmostEqual(agent.velocity()[1], -1 * agent.speed)

        location.x = 484
        location.y = 235
        agent.x = 558
        agent.y = 184
        self.assertAlmostEqual(agent.velocity()[0], -8.233920666857287)
        self.assertAlmostEqual(agent.velocity()[1], 5.6747291082394815)

    def test_space_remaining_function(self):
        agent = Agent("a", 1, 1)
        good1 = Goods("1", 1, 1, 1, 1)
        good2 = Goods("2", 1, 1, 1, 1)
        agent.goods[good1] = AgentGood(good1, 5, 1)
        agent.goods[good2] = AgentGood(good2, 2, 1)
        self.assertEqual(agent.space_remaining(), configuration.AGENT_MAX_GOODS - 5 - 2)
