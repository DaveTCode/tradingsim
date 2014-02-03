import unittest
from tradingsim.simulation.goods import Goods


class GoodsTests(unittest.TestCase):

    def test_str(self):
        good = Goods("test_good", 1, 1, 1)
        self.assertEqual(str(good), good.name)

    def test_cost_of_one(self):
        good = Goods("test_good", 1, 1, 1)
        self.assertAlmostEqual(good.cost_of_one(1), 1)

        good = Goods("a", 10, 1, 100)
        self.assertAlmostEqual(good.cost_of_one(0), 10)
        self.assertAlmostEqual(good.cost_of_one(100), 1)
        self.assertAlmostEqual(good.cost_of_one(50), 5.5)
        self.assertAlmostEqual(good.cost_of_one(40), 6.4)
        self.assertAlmostEqual(good.cost_of_one(30), 7.3)
        self.assertAlmostEqual(good.cost_of_one(20), 8.2)
        self.assertAlmostEqual(good.cost_of_one(10), 9.1)

    def test_cost(self):
        good = Goods("a", 10, 1, 100)

        self.assertEqual(good.cost(200, 1), 1)
        self.assertEqual(good.cost(50, 1), 6)
        self.assertEqual(good.cost(100, 100), 550)
        self.assertEqual(good.cost(1000, 100), 100)
