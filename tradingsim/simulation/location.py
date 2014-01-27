class Location:

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.goods_creation_rate = {}
        self.goods_consumption_rate = {}
        self.goods_quantity = {}

    def act(self, dt):
        for good in self.goods_creation_rate.keys():
            if not good in self.goods_quantity:
                self.goods_quantity[good] = 0

            self.goods_quantity[good] += dt * self.goods_creation_rate[good]

        for good in self.goods_consumption_rate.keys():
            if good in self.goods_quantity:
                self.goods_quantity[good] = max(0, self.goods_quantity[good] - dt * self.goods_consumption_rate[good])

    def __str__(self):
        return self.name
