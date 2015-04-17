class Location:

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.goods_creation_rate = {}
        self.goods_consumption_rate = {}
        self.goods_quantity = {}
        self.goods_quantity_fractional = {}

    def step(self, dt):
        for good in self.goods_creation_rate.keys():
            if good not in self.goods_quantity:
                self.goods_quantity[good] = 0
                self.goods_quantity_fractional[good] = 0

            new_amount = (dt * self.goods_creation_rate[good] +
                          self.goods_quantity[good] +
                          self.goods_quantity_fractional[good])
            self.goods_quantity_fractional[good] = new_amount - int(new_amount)
            self.goods_quantity[good] = int(new_amount)

        for good in self.goods_consumption_rate.keys():
            if good in self.goods_quantity:
                new_amount = max(0, (self.goods_quantity[good] +
                                     self.goods_quantity_fractional[good] -
                                     dt * self.goods_consumption_rate[good]))
                self.goods_quantity_fractional[good] = new_amount - int(new_amount)
                self.goods_quantity[good] = int(new_amount)

    def __str__(self):
        return "{0} ({1},{2})".format(self.name, self.x, self.y)
