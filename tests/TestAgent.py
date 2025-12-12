import math
import pytest
import tradingsim.configuration as configuration
from tradingsim.simulation.agent import Agent, AgentGood
from tradingsim.simulation.goods import Goods
from tradingsim.simulation.location import Location


class TestAgent:

    def test_distance_function(self):
        location = Location("a", 100, 100)
        agent = Agent("a", 100, 100)

        assert agent.distance_to_location(location) == pytest.approx(0.0)
        location.x = 101
        assert agent.distance_to_location(location) == pytest.approx(1.0)
        location.x = 99
        assert agent.distance_to_location(location) == pytest.approx(1.0)
        location.y = 99
        assert agent.distance_to_location(location) == pytest.approx(math.sqrt(2))

    def test_velocity_function(self):
        location = Location("a", 100, 100)
        agent = Agent("a", 100, 100)
        agent.destination = None

        assert agent.velocity() == pytest.approx((0, 0))
        agent.destination = location
        assert agent.velocity()[0] == pytest.approx(0)
        assert agent.velocity()[1] == pytest.approx(0)

        location.x = 101
        assert agent.velocity()[0] == pytest.approx(agent.speed)
        assert agent.velocity()[1] == pytest.approx(0)

        location.y = 101
        location.x = 100
        assert agent.velocity()[0] == pytest.approx(0)
        assert agent.velocity()[1] == pytest.approx(agent.speed)

        location.y = 100
        location.x = 99
        assert agent.velocity()[0] == pytest.approx(-1 * agent.speed)
        assert agent.velocity()[1] == pytest.approx(0)

        location.x = 100
        location.y = 99
        assert agent.velocity()[0] == pytest.approx(0)
        assert agent.velocity()[1] == pytest.approx(-1 * agent.speed)

        location.x = 484
        location.y = 235
        agent.x = 558
        agent.y = 184
        assert agent.velocity()[0] == pytest.approx(-8.233920666857287)
        assert agent.velocity()[1] == pytest.approx(5.6747291082394815)

    def test_space_remaining_function(self):
        agent = Agent("a", 1, 1)
        good1 = Goods("1", 1, 1, 1, 1)
        good2 = Goods("2", 1, 1, 1, 1)
        agent.goods[good1] = AgentGood(good1, 5, 1)
        agent.goods[good2] = AgentGood(good2, 2, 1)
        assert agent.space_remaining() == configuration.AGENT_MAX_GOODS - 5 - 2
