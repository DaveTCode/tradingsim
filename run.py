import argparse
import logging
import pygame
import tradingsim.configuration as configuration
from tradingsim.game import Game
import tradingsim.manualdata as manualdata
from tradingsim.renderers.dotrenderer import DotRenderer
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run the trading simulation application')
    parser.add_argument('--loglevel', choices=['DEBUG', 'ERROR'])
    args = parser.parse_args()

    if args.loglevel == 'DEBUG':
        logging.basicConfig(format='%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s', filename="log.txt", level=logging.DEBUG)
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
    else:
        logging.basicConfig(format='%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s', filename="log.txt", level=logging.ERROR)

    pygame.init()
    pygame.font.init()

    simulation = manualdata.create_simulation()
    renderer = DotRenderer()
    game = Game(configuration.WIDTH,
                configuration.HEIGHT,
                simulation,
                renderer)

    game.run()
