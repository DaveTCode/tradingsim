import math
import pygame


class Simulation:

    def __init__(self, width: int, height: int, ms_to_minutes: float):
        """
            width - The width of the simulation in arbitrary internal units.
            height - The height of the simulation in arbitrary internal units.
            ms_to_minutes - Multiplied by the number of milliseconds in
                a step to give the number of real time minutes that a step
                corresponds to.
        """
        self.base_ms_to_minutes = ms_to_minutes
        self.zoom = 1
        self.minutes_since_start = 0
        self.width = width
        self.height = height
        self.max_distance = math.sqrt(math.pow(width, 2) + math.pow(height, 2))
        self.agents = []
        self.locations = []
        self.goods = []

    def step(self, dt_ms: float):
        """
            Called to step the simulation on by the given number of
            milliseconds.

            This maps to a particular number of simulation minutes as defined
            in the constructor.
        """
        step_time_minutes = dt_ms * self.base_ms_to_minutes

        for _ in range(0, self.zoom):
            self.minutes_since_start += step_time_minutes

            for agent in self.agents:
                agent.step(step_time_minutes, self)

            for location in self.locations:
                location.step(step_time_minutes)

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.zoom = 1
            elif event.key == pygame.K_2:
                self.zoom = 2
            elif event.key == pygame.K_3:
                self.zoom = 5
            elif event.key == pygame.K_4:
                self.zoom = 10
            elif event.key == pygame.K_5:
                self.zoom = 100

    def time_str(self) -> str:
        """
            Provides a string representation of the time since the simulation
            started.
        """
        hours = self.minutes_since_start // 60
        minutes = self.minutes_since_start % 60.0

        return "{0:d}:{1:d}    (x{2:d})".format(int(hours), int(minutes), int(self.zoom))

    def total_money(self) -> float:
        """
            Provides access to information on the total money across all agents
            in the simulation.
        """
        money = 0
        for agent in self.agents:
            money += agent.money

        return money