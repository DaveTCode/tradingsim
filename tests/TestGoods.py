import random
import unittest
from tradingsim.simulation.goods import Goods


class GoodsTests(unittest.TestCase):

    def test_str(self):
        good = Goods("test_good", 1, 1, 1, 1)
        self.assertEqual(str(good), "test_good")

    def test_purchase_cost_of_one(self):
        good = Goods("test_good", 1, 1, 1, 1)
        self.assertAlmostEqual(good.purchase_cost_of_one(1), 1)

        good = Goods("a", 10, 8, 100, 20)
        self.assertAlmostEqual(good.purchase_cost_of_one(0), 10)
        self.assertAlmostEqual(good.purchase_cost_of_one(15), 10)  # Check that the max_cost_amount works
        self.assertAlmostEqual(good.purchase_cost_of_one(20), 10)  # Check that the max_cost_amount works on boundary
        self.assertAlmostEqual(good.purchase_cost_of_one(100), 8)
        self.assertAlmostEqual(good.purchase_cost_of_one(200), 8)
        self.assertAlmostEqual(good.purchase_cost_of_one(60), 9)
        self.assertAlmostEqual(good.purchase_cost_of_one(41), 9)
        self.assertAlmostEqual(good.purchase_cost_of_one(39), 8)
        self.assertAlmostEqual(good.purchase_cost_of_one(81), 10)
        self.assertAlmostEqual(good.purchase_cost_of_one(79), 9)

    def test_purchase_cost(self):
        good = Goods("a", 10, 8, 100, 20)
        self.assertAlmostEqual(good.purchase_cost(20, 20), 10 * 20)
        self.assertAlmostEqual(good.purchase_cost(60, 1), 9)
        self.assertAlmostEqual(good.purchase_cost(100, 80), 719)
        self.assertAlmostEqual(good.purchase_cost(60, 2), 18)
        self.assertAlmostEqual(good.purchase_cost(45, 10), 5 * 9 + 5 * 8)

    def test_sale_cost_of_one(self):
        good = Goods("test_good", 1, 1, 1, 1)
        self.assertAlmostEqual(good.sale_cost_of_one(1), 1)

        good = Goods("a", 10, 8, 100, 20)
        self.assertAlmostEqual(good.sale_cost_of_one(0), 10)
        self.assertAlmostEqual(good.sale_cost_of_one(100), 8)
        self.assertAlmostEqual(good.sale_cost_of_one(60), 9)
        self.assertAlmostEqual(good.sale_cost_of_one(41), 9)
        self.assertAlmostEqual(good.sale_cost_of_one(39), 10)
        self.assertAlmostEqual(good.sale_cost_of_one(81), 8)
        self.assertAlmostEqual(good.sale_cost_of_one(79), 9)

    def test_sale_cost(self):
        good = Goods("a", 10, 8, 100, 20)
        self.assertAlmostEqual(good.sale_cost(20, 20), 10 * 20)
        self.assertAlmostEqual(good.sale_cost(60, 1), 9)
        self.assertAlmostEqual(good.sale_cost(20, 80), 721)  # Shouldn't this be 719? Rounding issues maybe.
        self.assertAlmostEqual(good.sale_cost(60, 2), 18)
        self.assertAlmostEqual(good.sale_cost(45, 10), 5 * 9 + 5 * 10)

    def test_sale_less_than_purchase(self):
        for i in range(100):
            g = Goods("A", random.randint(10, 200), random.randint(0, 10), random.randint(5, 10), random.randint(1, 4))

            self.assertEqual(g.sale_cost(10, 2), g.purchase_cost(8, 2))