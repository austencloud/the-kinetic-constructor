import unittest
from PyQt6.QtCore import QPointF
from objects.arrow import Arrow


class TestArrow(unittest.TestCase):
    def setUp(self):
        self.graphboard = None  # Replace with an actual GraphBoard object
        self.attributes = {
            "color": "red",
            "motion_type": "pro",
            "rotation_direction": "clockwise",
            "quadrant": "northeast",
            "start_location": "W",
            "end_location": "E",
            "turns": 1,
        }
        self.arrow = Arrow(self.graphboard, self.attributes)

    def test_init(self):
        self.assertEqual(self.arrow.color, "red")
        self.assertEqual(self.arrow.motion_type, "pro")
        self.assertEqual(self.arrow.rotation_direction, "clockwise")
        self.assertEqual(self.arrow.quadrant, "northeast")
        self.assertEqual(self.arrow.start_location, "W")
        self.assertEqual(self.arrow.end_location, "E")
        self.assertEqual(self.arrow.turns, 1)

    def test_get_svg_file(self):
        svg_file = self.arrow.get_svg_file("pro", 1)
        self.assertEqual(svg_file, "shift_dir/pro_1.svg")

    def test_increment_turns(self):
        self.arrow.add_turn()
        self.assertEqual(self.arrow.turns, 2)

    def test_decrement_turns(self):
        self.arrow.subtract_turn()
        self.assertEqual(self.arrow.turns, 0)

    def test_set_attributes_from_dict(self):
        new_attributes = {
            "color": "blue",
            "motion_type": "anti",
            "rotation_direction": "counter_clockwise",
            "quadrant": "southeast",
            "start_location": "E",
            "end_location": "W",
            "turns": 2,
        }
        self.arrow.set_attributes_from_dict(new_attributes)
        self.assertEqual(self.arrow.color, "blue")
        self.assertEqual(self.arrow.motion_type, "anti")
        self.assertEqual(self.arrow.rotation_direction, "counter_clockwise")
        self.assertEqual(self.arrow.quadrant, "southeast")
        self.assertEqual(self.arrow.start_location, "E")
        self.assertEqual(self.arrow.end_location, "W")
        self.assertEqual(self.arrow.turns, 2)


if __name__ == "__main__":
    unittest.main()
