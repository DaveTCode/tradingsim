import pygame
import random
import sys
import configuration as configuration
from simulation.agent import Agent
from simulation.location import Location
from simulation.simulation import Simulation
from renderers.dotrenderer import DotRenderer


class Game:

    def __init__(self, width, height, simulation, renderer):
        self.width = width
        self.height = height
        self.simulation = simulation
        self.renderer = renderer
        self.paused = False

        self._init_pygame()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption(configuration.WINDOW_TITLE)
        self.window = pygame.display.set_mode((self.width, self.height))
        self.main_loop_clock = pygame.time.Clock()

    def run(self):
        while True:
            self.window.fill(configuration.BACKGROUND_COLOR)

            self.handle_input()

            if not self.paused:
                self.simulation.step()

            self.renderer.render(self.window, self.simulation)

            pygame.display.update()

            self.main_loop_clock.tick(configuration.FPS)

    def _handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.paused = True
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            self.paused = False

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            else:
                # TODO: Switch to a "register for messages" system.
                self.simulation.handle_event(event)
                self.renderer.handle_event(event)
                self._handle_event(event)


def generate_random_locations(simulation):
    for ii in range(0, random.randint(10, 20)):
        x = random.randint(0, simulation.width)
        y = random.randint(0, simulation.height)

        simulation.locations.append(Location(str(ii), x, y))

if __name__ == "__main__":
    simulation = Simulation(configuration.SIMULATION_STEP_MS,
                            configuration.SIMULATION_WIDTH,
                            configuration.SIMULATION_HEIGHT)
    renderer = DotRenderer()
    game = Game(configuration.WIDTH,
                configuration.HEIGHT,
                simulation,
                renderer)

    generate_random_locations(simulation)

    game.run()
