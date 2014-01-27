class Agent:

    def __init__(self, name, x, y):
        self.x = x
        self.y = y
        self.vel = (0, 0)  # units per ms
        self.acc = (0, 0)  # units per ms
        self.name = name

    def step(self, dt):
        self.x += dt * self.vel[0]
        self.y += dt * self.vel[1]
        self.vel = (self.acc[0] * dt + self.vel[0],
                    self.acc[1] * dt + self.vel[1])

    def __str__(self):
        return "{0} ({1},{2})".format(self.name, self.x, self.y)


class AgentAI:

    def __init__(self, agent):
        self.agent = agent

    def act(self, simulation):
        pass
