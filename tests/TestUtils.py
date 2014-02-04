import unittest
import tradingsim.utils as utils


class TestUtils(unittest.TestCase):

    def test_is_point_on_line_segment(self):
        # Normal line
        self.assertEqual(utils.is_point_on_line_segment(1, 1, 3, 3, 2, 2), True)
        self.assertEqual(utils.is_point_on_line_segment(1, 1, 3, 3, 2, 3), False)
        self.assertEqual(utils.is_point_on_line_segment(1, 1, 3, 3, 4, 4), False)
        self.assertEqual(utils.is_point_on_line_segment(1, 1, 3, 3, -1, -1), False)

        # Backwards line
        self.assertEqual(utils.is_point_on_line_segment(3, 3, 1, 1, 2, 2), True)
        self.assertEqual(utils.is_point_on_line_segment(3, 3, 1, 1, 2, 3), False)
        self.assertEqual(utils.is_point_on_line_segment(3, 3, 1, 1, 4, 4), False)
        self.assertEqual(utils.is_point_on_line_segment(3, 3, 1, 1, 0, 0), False)

        # Vertical line
        self.assertEqual(utils.is_point_on_line_segment(1, 1, 1, 100, 1, 99), True)
        self.assertEqual(utils.is_point_on_line_segment(1, 1, 1, 100, 2, 99), False)
        self.assertEqual(utils.is_point_on_line_segment(1, 1, 1, 100, 1, 101), False)
        self.assertEqual(utils.is_point_on_line_segment(1, 1, 1, 100, 1, -10), False)

        # Vertical upside down line
        self.assertEqual(utils.is_point_on_line_segment(1, 100, 1, 1, 1, 99), True)
        self.assertEqual(utils.is_point_on_line_segment(1, 100, 1, 1, 2, 99), False)
        self.assertEqual(utils.is_point_on_line_segment(1, 100, 1, 1, 1, 101), False)
        self.assertEqual(utils.is_point_on_line_segment(1, 100, 1, 1, 1, -10), False)
