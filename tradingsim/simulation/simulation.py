import pygame


class Simulation:

    def __init__(self, width, height, ms_to_minutes):
        '''
            width - The width of the simulation in arbitrary internal units.
            height - The height of the simulation in arbitrary internal units.
            ms_to_minutes - Multiplied by the number of milliseconds in
                a step to give the number of real time minutes that a step
                corresponds to.
        '''
        self.base_ms_to_minutes = ms_to_minutes
        self.current_ms_to_minutes = ms_to_minutes
        self.minutes_since_start = 0
        self.width = width
        self.height = height
        self.agents = []
        self.locations = []
        self.goods = []

    def step(self, dt_ms):
        '''
            Called to step the simulation on by the given number of
            milliseconds.

            This maps to a particular number of simulation minutes as defined
            in the constructor.
        '''
        step_time_minutes = dt_ms * self.current_ms_to_minutes
        self.minutes_since_start += step_time_minutes

        for agent in self.agents:
            agent.step(step_time_minutes)

        for location in self.locations:
            location.step(step_time_minutes)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.current_ms_to_minutes = self.base_ms_to_minutes
            elif event.key == pygame.K_2:
                self.current_ms_to_minutes = self.base_ms_to_minutes * 2
            elif event.key == pygame.K_3:
                self.current_ms_to_minutes = self.base_ms_to_minutes * 5
            elif event.key == pygame.K_4:
                self.current_ms_to_minutes = self.base_ms_to_minutes * 10
            elif event.key == pygame.K_5:
                self.current_ms_to_minutes = self.base_ms_to_minutes * 100

    def time_str(self):
        '''
            Provides a string representation of the time since the simulation
            started.
        '''
        hours = self.minutes_since_start // 60
        minutes = self.minutes_since_start % 60.0
        zoom = self.current_ms_to_minutes // self.base_ms_to_minutes

        return "{0:d}:{1:d}    ({2:d})".format(int(hours), int(minutes), int(zoom))
