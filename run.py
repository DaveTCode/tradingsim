import argparse
import logging
import logging.config
import pygame
import tradingsim.configuration as configuration
from tradingsim.game import Game
import tradingsim.manualdata as manualdata
from tradingsim.renderers.dotrenderer import DotRenderer

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the trading simulation application')
    parser.add_argument('-l', '--loglevel', choices=['debug', 'error'], default='debug')
    args = parser.parse_args()

    logging.config.fileConfig('log.conf')
    logger = logging.getLogger("root")
    logger.setLevel(getattr(logging, args.loglevel.upper()))

    pygame.init()
    pygame.font.init()

    simulation = manualdata.create_simulation()
    renderer = DotRenderer()
    game = Game(configuration.WIDTH, configuration.HEIGHT, simulation, renderer)

    game.run()
