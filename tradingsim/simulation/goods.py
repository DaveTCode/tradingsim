class Goods:
    """
    Represents a tradeable good with dynamic pricing based on supply.
    
    Economic Model:
    - BUYING: Price decreases as inventory increases (supply/demand)
      * Low inventory (<= max_cost_amount): High price (max_cost)
      * High inventory (>= min_cost_amount): Low price (min_cost)
      * Linear interpolation between these points
    
    - SELLING: Price increases as inventory increases (reverse of buying)
      * When you have little stock, selling gets you less
      * When you have abundant stock, selling gets you more
      * This models market saturation/scarcity effects
    
    Parameters:
        max_cost: Highest price (when inventory is scarce)
        min_cost: Lowest price (when inventory is abundant)
        max_cost_amount: Inventory level at/below which max_cost applies
        min_cost_amount: Inventory level at/above which min_cost applies
    """

    def __init__(
        self,
        name: str,
        max_cost: int,
        min_cost: int,
        min_cost_amount: int,
        max_cost_amount: int,
    ) -> None:
        self.name = name
        self.max_cost = max_cost
        self.min_cost = min_cost
        self.min_cost_amount = min_cost_amount
        self.max_cost_amount = max_cost_amount

    def purchase_cost_of_one(self, current_amount: int) -> int:
        """
        Calculate the cost of purchasing ONE unit when you have current_amount.
        
        Economics: When you already have a lot, the market price is lower.
        Uses discrete integer rounding for stepped pricing.
        
        Args:
            current_amount: Current inventory level
            
        Returns:
            Price for purchasing one unit (rounded to nearest integer)
        """
        current_amount = current_amount
        if current_amount >= self.min_cost_amount:
            return self.min_cost
        elif current_amount <= self.max_cost_amount:
            return self.max_cost
        else:
            # Linear interpolation between the two price points with rounding
            slope = (self.max_cost - self.min_cost) / (self.min_cost_amount - self.max_cost_amount)
            return round(self.min_cost + slope * (current_amount - self.max_cost_amount))

    def sale_cost_of_one(self, current_amount: int) -> int:
        """
        Calculate the value received for selling ONE unit when you have current_amount.
        
        Economics: Same direction as purchase for selling.
        - Low inventory: Get low price (desperation/scarcity sale)
        - High inventory: Get high price (selling from abundance)
        Uses discrete integer rounding for stepped pricing.
        
        Args:
            current_amount: Current inventory level
            
        Returns:
            Value received for selling one unit (rounded to nearest integer)
        """
        if current_amount >= self.min_cost_amount:
            return self.min_cost
        elif current_amount <= self.max_cost_amount:
            return self.max_cost
        else:
            # Linear interpolation - same formula as purchase with rounding
            slope = float((self.max_cost - self.min_cost)) / float((self.max_cost_amount - self.min_cost_amount))
            return round(self.max_cost + slope * (current_amount - self.max_cost_amount))

    def purchase_cost(self, current_amount: int, purchase_amount: int) -> int:
        """
        Calculate total cost to purchase multiple units.
        
        As you buy each unit, your inventory increases, so the price changes.
        Example: Buying 10 units starting from 5 means buying at levels 5, 4, 3, 2, 1, 0, ...
        (each purchase reduces your effective inventory for the next purchase)
        
        Args:
            current_amount: Current inventory level
            purchase_amount: Number of units to purchase
            
        Returns:
            Total cost as integer (rounded down from float sum)
        """
        total_cost = 0.0
        for ii in range(purchase_amount):
            total_cost += self.purchase_cost_of_one(current_amount - ii)
        return int(total_cost)

    def sale_cost(self, current_amount: int, sale_amount: int) -> int:
        """
        Calculate total value received for selling multiple units.
        
        As you sell each unit, your inventory decreases, so the price per unit changes.
        Example: Selling 2 units from inventory of 10 means selling at levels 10, 11
        (each sale increases the "sold from" level)
        
        Args:
            current_amount: Current inventory level
            sale_amount: Number of units to sell
            
        Returns:
            Total value received as integer (rounded down from float sum)
        """
        total_cost = 0.0
        for ii in range(sale_amount):
            total_cost += self.sale_cost_of_one(current_amount + ii)
        return int(total_cost)

    def __str__(self) -> str:
        return self.name
