class Goods:

    def __init__(self, name, max_cost, min_cost, min_cost_amount):
        self.name = name

    def cost(self, current_amount, purchase_amount):
        initial_cost = max(self.min_cost,
                           (current_amount / self.min_cost_amount) * self.min_cost)
        final_cost = min(self.max_cost,
                         ((current_amount - purchase_amount) / self.min_cost_amount) * self.min_cost)

        return (final_cost - initial_cost) / 2

    def __str__(self):
        return self.name
