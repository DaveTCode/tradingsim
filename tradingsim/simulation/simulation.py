class Simulation:

    def __init__(self, step_time_ms, width, height):
        self.step_time_ms = step_time_ms
        self.width = width
        self.height = height
        self.agents = []
        self.locations = []
        self.goods = []

    def step(self):
        for agent in self.agents:
            agent.step(self.step_time_ms)

        for location in self.locations:
            location.act(self.step_time_ms)

    def handle_event(self, event):
        pass
