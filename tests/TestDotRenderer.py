import pygame
import pytest
from tradingsim.renderers.dotrenderer import DotRenderer


@pytest.fixture(scope="module")
def pygame_init():
    """Initialize pygame for renderer tests."""
    pygame.init()
    pygame.font.init()
    yield
    pygame.quit()


class TestDotRenderer:

    def test_agent_to_window_coords_no_change(self, pygame_init):
        renderer = DotRenderer()
        assert renderer._agent_to_window_coords(0, 0) == (0, 0)
        assert renderer._agent_to_window_coords(10, 10) == (10, 10)
        assert renderer._agent_to_window_coords(0, 21) == (0, 21)

    def test_agent_to_window_coords_offset(self, pygame_init):
        renderer = DotRenderer()
        renderer.move_camera(18, 23)
        assert renderer._agent_to_window_coords(0, 0) == (-18, -23)
        assert renderer._agent_to_window_coords(100, 100) == (82, 77)
        assert renderer._agent_to_window_coords(18, 83) == (0, 60)

    def test_agent_to_window_coords_scale(self, pygame_init):
        renderer = DotRenderer()
        renderer.zoom_camera(1)
        assert renderer._agent_to_window_coords(0, 0) == (0, 0)
        assert renderer._agent_to_window_coords(10, 10) == (20, 20)
        assert renderer._agent_to_window_coords(0, 21) == (0, 42)

    def test_agent_to_window_coords_scale_and_move(self, pygame_init):
        renderer = DotRenderer()
        renderer.zoom_camera(1)
        renderer.move_camera(19, 1)
        assert renderer._agent_to_window_coords(0, 0) == (-19, -1)
        assert renderer._agent_to_window_coords(10, 10) == (1, 19)

    def test_window_to_agent_coords_no_change(self, pygame_init):
        renderer = DotRenderer()
        assert renderer._window_to_agent_coords(0, 0) == (0, 0)
        assert renderer._window_to_agent_coords(10, 10) == (10, 10)
        assert renderer._window_to_agent_coords(0, 21) == (0, 21)

    def test_window_to_agent_coords_offset(self, pygame_init):
        renderer = DotRenderer()
        renderer.move_camera(5, 7)
        assert renderer._window_to_agent_coords(0, 0) == (5, 7)
        assert renderer._window_to_agent_coords(10, 10) == (15, 17)
        assert renderer._window_to_agent_coords(0, 21) == (5, 28)

    def test_window_to_agent_coords_zoom(self, pygame_init):
        renderer = DotRenderer()
        renderer.zoom_camera(1)
        assert renderer._window_to_agent_coords(0, 0) == (0, 0)
        assert renderer._window_to_agent_coords(10, 10) == (5, 5)
        assert renderer._window_to_agent_coords(4, 22) == (2, 11)

    def test_window_to_agent_coords_scale_and_move(self, pygame_init):
        renderer = DotRenderer()
        renderer.zoom_camera(1)
        renderer.move_camera(19, 1)
        assert renderer._window_to_agent_coords(0, 0) == (9.5, 0.5)
        assert renderer._window_to_agent_coords(10, 10) == (14.5, 5.5)
