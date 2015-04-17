import math


class Goods:
    """
    This represents the static data that constitutes a single good. It
    defines the cost of that good.
    """

    def __init__(self, name, max_cost, min_cost, min_cost_amount):
        self.name = name
        self.max_cost = float(max_cost)
        self.min_cost = float(min_cost)
        self.min_cost_amount = float(min_cost_amount)

    def purchase_cost_of_one(self, current_amount):
        """
        Used to calculate the cost of purchasing a single instance of this good
        given that the owner currently has "current_amount"

        :param current_amount: The amount in stock at the owner

        :return: The cost of a single instance of this good.
        """
        current_amount = float(current_amount)
        if current_amount > self.min_cost_amount:
            return self.min_cost
        else:
            m = (self.max_cost - self.min_cost) / self.min_cost_amount
            return -1.0 * m * current_amount + self.max_cost

    def purchase_cost(self, current_amount, purchase_amount):
        """
        Used to calculate the cost to purchase x of the good when the owner has
        y of them.

        :param current_amount: The amount that the owner currently has in
                               stock.
        :param purchase_amount: The amount that the buyer wants.

        :return: The total cost to purchase the required number.
        """
        initial_cost = self.purchase_cost_of_one(current_amount)
        final_cost = self.purchase_cost_of_one(current_amount - purchase_amount)
        total_cost = math.ceil(float(purchase_amount) * (initial_cost + final_cost) / 2.0)

        return int(total_cost)  # Response should be in full units

    def sale_cost(self, current_amount, sale_amount):
        """
        TODO: For now the sale cost is defined as equal to the purchase
        cost.
        """
        return self.purchase_cost(current_amount, sale_amount)

    def __str__(self):
        return self.name
