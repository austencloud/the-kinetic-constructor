import json
import re
from PyQt6.QtCore import Qt
from constants import ANTI, PRO, RED, BLUE, LEADING, TRAILING
from typing import Dict, Tuple, Union
from objects.motion.motion import Motion

from objects.pictograph.pictograph import Pictograph


class WASD_AdjustmentManager:
    def __init__(self, pictograph: Pictograph):
        self.pictograph = pictograph

    def handle_arrow_movement(self, key, shift_held) -> None:
        if not self.pictograph.selected_arrow:
            return

        adjustment_increment = 15 if shift_held else 5
        adjustment = self.get_adjustment(key, adjustment_increment)
        self.update_arrow_adjustments_in_json(adjustment)

    def update_arrow_adjustments_in_json(self, adjustment) -> None:
        if not self.pictograph.selected_arrow:
            return
        red_motion = self.pictograph.motions[RED]
        blue_motion = self.pictograph.motions[BLUE]

        if blue_motion.turns in [0.0, 1.0, 2.0, 3.0]:
            blue_motion.turns = int(blue_motion.turns)
        if red_motion.turns in [0.0, 1.0, 2.0, 3.0]:
            red_motion.turns = int(red_motion.turns)
        pro_motion = red_motion if red_motion.motion_type == PRO else blue_motion
        anti_motion = blue_motion if blue_motion.motion_type == ANTI else red_motion
        with open("arrow_placement/special_placements.json", "r") as file:
            data: Dict = json.load(file)
        if self.pictograph.letter in ["E", "G", "H", "P", "Q"]:
            adjustment_key = (blue_motion.turns, red_motion.turns)
            letter_data: Dict = data.get(self.pictograph.letter, {})
            turn_data = letter_data.get(str(adjustment_key))
            if turn_data:
                turn_data[self.pictograph.selected_arrow.color][0] += adjustment[0]
                turn_data[self.pictograph.selected_arrow.color][1] += adjustment[1]
                letter_data[str(adjustment_key)] = turn_data
                data[self.pictograph.letter] = letter_data
        elif self.pictograph.letter in ["I", "R", "U", "V", "X"]:
            adjustment_key = (pro_motion.turns, anti_motion.turns)
            letter_data = data.get(self.pictograph.letter, {})
            turn_data = letter_data.get(str(adjustment_key))
            if turn_data:
                turn_data[self.pictograph.selected_arrow.motion_type][0] += adjustment[
                    0
                ]
                turn_data[self.pictograph.selected_arrow.motion_type][1] += adjustment[
                    1
                ]
                letter_data[str(adjustment_key)] = turn_data
                data[self.pictograph.letter] = letter_data
        elif self.pictograph.letter in ["S", "T"]:
            leading_motion = self.pictograph.get_leading_motion(
                self.pictograph.blue_motion, self.pictograph.red_motion
            )
            trailing_motion = (
                self.pictograph.blue_motion
                if leading_motion == self.pictograph.red_motion
                else self.pictograph.red_motion
            )

            adjustment_key = (leading_motion.turns, trailing_motion.turns)
            letter_data = data.get(self.pictograph.letter, {})
            turn_data = letter_data.get(str(adjustment_key))
            if turn_data:
                turn_data[self.pictograph.selected_arrow.lead_state][0] += adjustment[0]
                turn_data[self.pictograph.selected_arrow.lead_state][1] += adjustment[1]
                letter_data[str(adjustment_key)] = turn_data
                data[self.pictograph.letter] = letter_data
        json_str = json.dumps(data, indent=2)

        compact_json_str = re.sub(
            r'": \[\s+(-?\d+),\s+(-?\d+)\s+\]', r'": [\1, \2]', json_str
        )
        with open("arrow_placement/special_placements.json", "w") as file:
            file.write(compact_json_str)

    def get_adjustment(
        self, key, increment
    ) -> Tuple[Union[int, float], Union[int, float]]:
        if self.pictograph.letter in "PQRST":
            return self.get_letter_specific_adjustment(key, increment)
        else:
            return self.get_default_adjustment(key, increment)

    def get_letter_specific_adjustment(self, key, increment):
        direction_map = {
            Qt.Key.Key_W: (0, -1),
            Qt.Key.Key_A: (-1, 0),
            Qt.Key.Key_S: (0, 1),
            Qt.Key.Key_D: (1, 0),
        }

        dx, dy = direction_map.get(key, (0, 0))

        if (
            self.pictograph.letter in "PQR"
            and self.pictograph.selected_arrow.color in [RED, BLUE]
        ):
            if key in [Qt.Key.Key_A, Qt.Key.Key_D]:
                dx = -dx

        if (
            self.pictograph.letter in "ST"
            and self.pictograph.selected_arrow.lead_state in [LEADING, TRAILING]
        ):
            dy, dx = dx, dy

        return dx * increment, dy * increment

    def get_default_adjustment(self, key, increment):
        adjustment_map = {
            Qt.Key.Key_W: (0, -increment),
            Qt.Key.Key_A: (-increment, 0),
            Qt.Key.Key_S: (0, increment),
            Qt.Key.Key_D: (increment, 0),
        }
        return adjustment_map.get(key, (0, 0))
