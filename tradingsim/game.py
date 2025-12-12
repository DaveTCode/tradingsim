import pygame
import sys
import tradingsim.configuration as configuration
from tradingsim.renderers.dotrenderer import DotRenderer
from tradingsim.simulation.simulation import Simulation


class Game:

    def __init__(
        self, width: int, height: int, simulation: Simulation, renderer: DotRenderer
    ):
        self.width = width
        self.height = height
        self.simulation = simulation
        self.renderer = renderer
        self.paused = False

        pygame.display.set_caption(configuration.WINDOW_TITLE)
        self.window = pygame.display.set_mode((self.width, self.height))
        self.main_loop_clock = pygame.time.Clock()

    def run(self):
        while True:
            self.window.fill(configuration.BACKGROUND_COLOR)

            self.handle_input()

            if not self.paused:
                self.simulation.step(1000 / configuration.FPS)

            self.renderer.render(self.window, self.simulation)

            pygame.display.update()

            self.main_loop_clock.tick(configuration.FPS)

    def _handle_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.paused = not self.paused

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            else:
                # TODO: Switch to a "register for messages" system.
                self.simulation.handle_event(event)
                self.renderer.handle_event(event)
                self._handle_event(event)
