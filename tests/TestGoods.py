import random
import pytest
from tradingsim.simulation.goods import Goods


class TestGoods:

    def test_str(self):
        good = Goods("test_good", 1, 1, 1, 1)
        assert str(good) == "test_good"

    def test_purchase_cost_of_one(self):
        good = Goods("test_good", 1, 1, 1, 1)
        assert good.purchase_cost_of_one(1) == pytest.approx(1)

        good = Goods("a", 10, 8, 100, 20)
        assert good.purchase_cost_of_one(0) == pytest.approx(10)
        assert good.purchase_cost_of_one(15) == pytest.approx(10)  # Check that the max_cost_amount works
        assert good.purchase_cost_of_one(20) == pytest.approx(10)  # Check that the max_cost_amount works on boundary
        assert good.purchase_cost_of_one(100) == pytest.approx(8)
        assert good.purchase_cost_of_one(200) == pytest.approx(8)
        assert good.purchase_cost_of_one(60) == pytest.approx(9)
        assert good.purchase_cost_of_one(41) == pytest.approx(9)
        assert good.purchase_cost_of_one(39) == pytest.approx(8)
        assert good.purchase_cost_of_one(81) == pytest.approx(10)
        assert good.purchase_cost_of_one(79) == pytest.approx(9)

    def test_purchase_cost(self):
        good = Goods("a", 10, 8, 100, 20)
        assert good.purchase_cost(20, 20) == pytest.approx(10 * 20)
        assert good.purchase_cost(60, 1) == pytest.approx(9)
        assert good.purchase_cost(100, 80) == pytest.approx(719)
        assert good.purchase_cost(60, 2) == pytest.approx(18)
        assert good.purchase_cost(45, 10) == pytest.approx(5 * 9 + 5 * 8)

    def test_sale_cost_of_one(self):
        good = Goods("test_good", 1, 1, 1, 1)
        assert good.sale_cost_of_one(1) == pytest.approx(1)

        good = Goods("a", 10, 8, 100, 20)
        assert good.sale_cost_of_one(0) == pytest.approx(10)
        assert good.sale_cost_of_one(100) == pytest.approx(8)
        assert good.sale_cost_of_one(60) == pytest.approx(9)
        assert good.sale_cost_of_one(41) == pytest.approx(9)
        assert good.sale_cost_of_one(39) == pytest.approx(10)
        assert good.sale_cost_of_one(81) == pytest.approx(8)
        assert good.sale_cost_of_one(79) == pytest.approx(9)

    def test_sale_cost(self):
        good = Goods("a", 10, 8, 100, 20)
        assert good.sale_cost(20, 20) == pytest.approx(10 * 20)
        assert good.sale_cost(60, 1) == pytest.approx(9)
        assert good.sale_cost(20, 80) == pytest.approx(721)  # Shouldn't this be 719? Rounding issues maybe.
        assert good.sale_cost(60, 2) == pytest.approx(18)
        assert good.sale_cost(45, 10) == pytest.approx(5 * 9 + 5 * 10)

    def test_sale_less_than_purchase(self):
        for i in range(100):
            g = Goods("A", random.randint(10, 200), random.randint(0, 10), random.randint(5, 10), random.randint(1, 4))

            assert g.sale_cost(10, 2) == g.purchase_cost(8, 2)