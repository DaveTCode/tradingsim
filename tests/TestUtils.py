import pytest
import tradingsim.utils as utils


class TestUtils:

    def test_is_point_on_line_segment(self):
        # Normal line
        assert utils.is_point_on_line_segment(1, 1, 3, 3, 2, 2) is True
        assert utils.is_point_on_line_segment(1, 1, 3, 3, 2, 3) is False
        assert utils.is_point_on_line_segment(1, 1, 3, 3, 4, 4) is False
        assert utils.is_point_on_line_segment(1, 1, 3, 3, -1, -1) is False

        # Backwards line
        assert utils.is_point_on_line_segment(3, 3, 1, 1, 2, 2) is True
        assert utils.is_point_on_line_segment(3, 3, 1, 1, 2, 3) is False
        assert utils.is_point_on_line_segment(3, 3, 1, 1, 4, 4) is False
        assert utils.is_point_on_line_segment(3, 3, 1, 1, 0, 0) is False

        # Vertical line
        assert utils.is_point_on_line_segment(1, 1, 1, 100, 1, 99) is True
        assert utils.is_point_on_line_segment(1, 1, 1, 100, 2, 99) is False
        assert utils.is_point_on_line_segment(1, 1, 1, 100, 1, 101) is False
        assert utils.is_point_on_line_segment(1, 1, 1, 100, 1, -10) is False

        # Vertical upside down line
        assert utils.is_point_on_line_segment(1, 100, 1, 1, 1, 99) is True
        assert utils.is_point_on_line_segment(1, 100, 1, 1, 2, 99) is False
        assert utils.is_point_on_line_segment(1, 100, 1, 1, 1, 101) is False
        assert utils.is_point_on_line_segment(1, 100, 1, 1, 1, -10) is False
