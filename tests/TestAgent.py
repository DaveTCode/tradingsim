import math
import unittest
from tradingsim.simulation.location import Location
from tradingsim.simulation.agent import Agent


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
