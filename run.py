import pygame
import tradingsim.configuration as configuration
from tradingsim.game import Game
import tradingsim.manualdata as manualdata
from tradingsim.renderers.dotrenderer import DotRenderer

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
