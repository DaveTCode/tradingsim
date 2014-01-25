class Simulation:

    def __init__(self, step_time_ms, width, height):
        self.step_time_ms = step_time_ms
        self.agents = []
        self.locations = []
        self.width = width
        self.height = height

    def step(self):
        for agent in self.agents:
            agent.step(self.step_time_ms)

    def handle_event(self, event):
        pass
