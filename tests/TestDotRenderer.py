import pygame

import unittest
from tradingsim.renderers.dotrenderer import DotRenderer


class DotRendererTests(unittest.TestCase):

    def setUp(self):
        """
            Renderer uses font objects so need to set this up.
        """
        pygame.init()
        pygame.font.init()

    def test_agent_to_window_coords_no_change(self):
        renderer = DotRenderer()
        self.assertEqual(renderer._agent_to_window_coords(0, 0), (0, 0))
        self.assertEqual(renderer._agent_to_window_coords(10, 10), (10, 10))
        self.assertEqual(renderer._agent_to_window_coords(0, 21), (0, 21))

    def test_agent_to_window_coords_offset(self):
        renderer = DotRenderer()
        renderer.move_camera(18, 23)
        self.assertEqual(renderer._agent_to_window_coords(0, 0), (-18, -23))
        self.assertEqual(renderer._agent_to_window_coords(100, 100), (82, 77))
        self.assertEqual(renderer._agent_to_window_coords(18, 83), (0, 60))

    def test_agent_to_window_coords_scale(self):
        renderer = DotRenderer()
        renderer.zoom_camera(1)
        self.assertEqual(renderer._agent_to_window_coords(0, 0), (0, 0))
        self.assertEqual(renderer._agent_to_window_coords(10, 10), (20, 20))
        self.assertEqual(renderer._agent_to_window_coords(0, 21), (0, 42))

    def test_agent_to_window_coords_scale_and_move(self):
        renderer = DotRenderer()
        renderer.zoom_camera(1)
        renderer.move_camera(19, 1)
        self.assertEqual(renderer._agent_to_window_coords(0, 0), (-19, -1))
        self.assertEqual(renderer._agent_to_window_coords(10, 10), (1, 19))

    def test_window_to_agent_coords_no_change(self):
        renderer = DotRenderer()
        self.assertEqual(renderer._window_to_agent_coords(0, 0), (0, 0))
        self.assertEqual(renderer._window_to_agent_coords(10, 10), (10, 10))
        self.assertEqual(renderer._window_to_agent_coords(0, 21), (0, 21))

    def test_window_to_agent_coords_offset(self):
        renderer = DotRenderer()
        renderer.move_camera(5, 7)
        self.assertEqual(renderer._window_to_agent_coords(0, 0), (5, 7))
        self.assertEqual(renderer._window_to_agent_coords(10, 10), (15, 17))
        self.assertEqual(renderer._window_to_agent_coords(0, 21), (5, 28))

    def test_window_to_agent_coords_zoom(self):
        renderer = DotRenderer()
        renderer.zoom_camera(1)
        self.assertEqual(renderer._window_to_agent_coords(0, 0), (0, 0))
        self.assertEqual(renderer._window_to_agent_coords(10, 10), (5, 5))
        self.assertEqual(renderer._window_to_agent_coords(4, 22), (2, 11))

    def test_window_to_agent_coords_scale_and_move(self):
        renderer = DotRenderer()
        renderer.zoom_camera(1)
        renderer.move_camera(19, 1)
        self.assertEqual(renderer._window_to_agent_coords(0, 0), (9.5, 0.5))
        self.assertEqual(renderer._window_to_agent_coords(10, 10), (14.5, 5.5))

if __name__ == '__main__':
    unittest.main()
