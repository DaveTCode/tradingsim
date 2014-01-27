import pygame
import configuration


class DotRenderer:

    def __init__(self):
        self.top_left_x = 0
        self.top_left_y = 0
        self.scale = 1
        self.keys = {v: (k, False) for (k, v) in configuration.RENDERER_KEY_CONFIG.iteritems()}
        self.location_highlighted = None
        self.font = pygame.font.Font(None, 12)

    def move_camera(self, dx, dy):
        self.top_left_x += dx
        self.top_left_y += dy

    def zoom_camera(self, amount):
        self.scale += amount

    def render(self, window, simulation):
        self._update_viewport()

        (mouse_x, mouse_y) = pygame.mouse.get_pos()

        for agent in simulation.agents:
            self._render_agent(window, agent)

        for location in simulation.locations:
            render_location_text = (abs(location.x - mouse_x) < configuration.DIST_FROM_LOCATION_TO_HIGHLIGHT and
                                    abs(location.y - mouse_y) < configuration.DIST_FROM_LOCATION_TO_HIGHLIGHT)

            self._render_location(window, location, render_location_text)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in self.keys.keys():
            self.keys[event.key] = (self.keys[event.key][0], True)
        if event.type == pygame.KEYUP and event.key in self.keys.keys():
            self.keys[event.key] = (self.keys[event.key][0], False)

    def _update_viewport(self):
        keys_down = [v[0] for (k, v) in self.keys.iteritems() if v[1]]
        dx = 0
        dy = 0
        dz = 0

        if "left" in keys_down:
            dx -= configuration.VIEWPORT_VEL_X
        if "right" in keys_down:
            dx += configuration.VIEWPORT_VEL_X
        if "up" in keys_down:
            dy -= configuration.VIEWPORT_VEL_Y
        if "down" in keys_down:
            dy += configuration.VIEWPORT_VEL_Y
        if "zoom_in" in keys_down:
            dz += configuration.VIEWPORT_ZOOM_VEL
        if "zoom_out" in keys_down:
            dz -= configuration.VIEWPORT_ZOOM_VEL

        if "adjuster" in keys_down:
            dx *= configuration.VIEWPORT_MOVEMENT_ADJUSTER
            dy *= configuration.VIEWPORT_MOVEMENT_ADJUSTER
            dz *= configuration.VIEWPORT_ZOOM_ADJUSTER

        self.move_camera(dx, dy)
        self.zoom_camera(dz)

    def _agent_to_window_coords(self, x, y):
        return ((x * self.scale) - self.top_left_x, (y * self.scale) - self.top_left_y)

    def _window_to_agent_coords(self, x, y):
        return ((x + self.top_left_x) / self.scale, (y + self.top_left_y) / self.scale)

    def _render_agent(self, window, agent):
        (x, y) = self._agent_to_window_coords(agent.x, agent.y)

        pygame.draw.circle(window,
                           configuration.AGENT_COLOR,
                           (x, y),
                           configuration.AGENT_RADIUS)

    def _render_location(self, window, location, render_text):
        (x, y) = self._agent_to_window_coords(location.x, location.y)

        pygame.draw.rect(window,
                         configuration.LOCATION_COLOR,
                         (x,
                          y,
                          configuration.LOCATION_WIDTH,
                          configuration.LOCATION_WIDTH))

        if render_text:
            text = ""
            for good, amount in location.goods_quantity.iteritems():
                text += str(good) + "=" + str(amount) + ", "
            text_rendered = self.font.render(text[:-2], 1, (255, 255, 255))
            window.blit(text_rendered, (location.x, location.y))
