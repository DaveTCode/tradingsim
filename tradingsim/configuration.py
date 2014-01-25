import pygame

WINDOW_TITLE = 'Trading Simulation'

WIDTH = 1024
HEIGHT = 768

SIMULATION_WIDTH = 1024
SIMULATION_HEIGHT = 768

BACKGROUND_COLOR = pygame.Color(0, 0, 0)

FPS = 30
SIMULATION_STEP_MS = 1000 / FPS

AGENT_COLOR = pygame.Color(0, 0, 255)
AGENT_RADIUS = 3

LOCATION_COLOR = pygame.Color(255, 0, 0)
LOCATION_WIDTH = 4

RENDERER_KEY_CONFIG = {
    "left": pygame.K_LEFT,
    "right": pygame.K_RIGHT,
    "up": pygame.K_UP,
    "down": pygame.K_DOWN,
    "adjuster": pygame.K_LSHIFT,
    "zoom_in": pygame.K_EQUALS,
    "zoom_out": pygame.K_MINUS
}

VIEWPORT_ZOOM_ADJUSTER = 2
VIEWPORT_MOVEMENT_ADJUSTER = 10
VIEWPORT_VEL_X = 1
VIEWPORT_VEL_Y = 1
VIEWPORT_ZOOM_VEL = 0.01
