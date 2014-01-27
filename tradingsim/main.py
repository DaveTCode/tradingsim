import pygame
import sys
import configuration as configuration
from renderers.dotrenderer import DotRenderer
import manualdata


class Game:

    def __init__(self, width, height, simulation, renderer):
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

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    simulation = manualdata.create_simulation()
    renderer = DotRenderer()
    game = Game(configuration.WIDTH,
                configuration.HEIGHT,
                simulation,
                renderer)

    game.run()
