import math


class Goods:

    def __init__(self, name, max_cost, min_cost, min_cost_amount):
        self.name = name
        self.max_cost = float(max_cost)
        self.min_cost = float(min_cost)
        self.min_cost_amount = float(min_cost_amount)

    def cost_difference(self):
        return self.min_cost - self.max_cost

    def purchase_cost_of_one(self, current_amount):
        current_amount = float(current_amount)
        if current_amount > self.min_cost_amount:
            return self.min_cost
        else:
            m = (self.max_cost - self.min_cost) / self.min_cost_amount
            return -1.0 * m * current_amount + self.max_cost

    def purchase_cost(self, current_amount, purchase_amount):
        initial_cost = self.purchase_cost_of_one(current_amount)
        final_cost = self.purchase_cost_of_one(current_amount - purchase_amount)
        total_cost = math.ceil(float(purchase_amount) * (initial_cost + final_cost) / 2.0)

        return int(total_cost)  # Response should in full units

    def sale_cost(self, current_amount, sale_amount):
        '''
            TODO: For now the sale cose is defined as equal to the purchase
            cost.
        '''
        initial_cost = self.purchase_cost_of_one(current_amount)
        final_cost = self.purchase_cost_of_one(current_amount + sale_amount)
        total_cost = math.ceil(float(sale_amount) * (initial_cost + final_cost) / 2.0)

        return int(total_cost)

    def __str__(self):
        return self.name
