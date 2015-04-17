import unittest
from tradingsim.simulation.goods import Goods


class GoodsTests(unittest.TestCase):

    def test_str(self):
        good = Goods("test_good", 1, 1, 1)
        self.assertEqual(str(good), "test_good")

    def test_purchase_cost_of_one(self):
        good = Goods("test_good", 1, 1, 1)
        self.assertAlmostEqual(good.purchase_cost_of_one(1), 1)

        good = Goods("a", 10, 1, 100)
        self.assertAlmostEqual(good.purchase_cost_of_one(0), 10)
        self.assertAlmostEqual(good.purchase_cost_of_one(100), 1)
        self.assertAlmostEqual(good.purchase_cost_of_one(50), 5.5)
        self.assertAlmostEqual(good.purchase_cost_of_one(40), 6.4)
        self.assertAlmostEqual(good.purchase_cost_of_one(30), 7.3)
        self.assertAlmostEqual(good.purchase_cost_of_one(20), 8.2)
        self.assertAlmostEqual(good.purchase_cost_of_one(10), 9.1)

    def test_purchase_cost(self):
        good = Goods("a", 10, 1, 100)

        self.assertEqual(good.purchase_cost(200, 1), 1)
        self.assertEqual(good.purchase_cost(50, 1), 6)
        self.assertEqual(good.purchase_cost(100, 100), 550)
        self.assertEqual(good.purchase_cost(1000, 100), 100)

    def test_sale_amount(self):
        good = Goods("a", 10, 1, 100)

        self.assertEqual(good.sale_cost(200, 1), 1)
        self.assertEqual(good.sale_cost(50, 1), 6)
        self.assertEqual(good.sale_cost(100, 100), 550)
        self.assertEqual(good.sale_cost(1000, 100), 100)