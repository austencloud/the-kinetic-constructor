import json
import re
from PyQt6.QtCore import Qt
from constants import (
    ANTI,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    FLOAT,
    PRO,
    RED,
    BLUE,
    LEADING,
    STATIC,
    TRAILING,
)
from typing import Dict, Tuple, Union

from objects.pictograph.pictograph import Pictograph
from utilities.TypeChecking.Letters import (
    Letters,
    Type1_hybrid_letters,
    Type2_letters,
    non_hybrid_letters,
)


class WASD_AdjustmentManager:
    def __init__(self, pictograph: Pictograph) -> None:
        self.pictograph = pictograph
        self.red_motion = self.pictograph.motions[RED]
        self.blue_motion = self.pictograph.motions[BLUE]

    def handle_half_turns(self, key) -> None:
        if not self.pictograph.selected_arrow:
            return

        half_turn_adjustment = -0.5 if key == Qt.Key.Key_Q else 0.5
        self.adjust_turns(half_turn_adjustment)

    def adjust_turns(self, adjustment: float):
        selected_motion = self.pictograph.selected_arrow.motion
        new_turns = max(0, min(3, selected_motion.turns + adjustment))
        pictograph_dict = {f"{self.pictograph.selected_arrow.color}_turns": new_turns}
        self.pictograph.update_pictograph(pictograph_dict)

    def handle_arrow_movement(self, key, shift_held) -> None:
        if not self.pictograph.selected_arrow:
            return

        adjustment_increment = 15 if shift_held else 5
        adjustment = self.get_adjustment(key, adjustment_increment)
        self.update_arrow_adjustments_in_json(adjustment)

    def update_arrow_adjustments_in_json(self, adjustment) -> None:
        if not self.pictograph.selected_arrow:
            return
        data = self.load_json_data("arrow_placement/special_placements.json")

        handlers = {
            "S": self.handle_S_T,
            "T": self.handle_S_T,
            **{letter: self.handle_non_hybrid_letters for letter in non_hybrid_letters},
            **{
                letter: self.handle_pro_anti_hybrid_letters
                for letter in Type1_hybrid_letters
            },
            **{
                letter: self.handle_shift_static_hybrid_letters
                for letter in Type2_letters
            },
        }

        handler = handlers.get(self.pictograph.letter, lambda d, a: None)
        handler(data, adjustment)

        self.write_json_data(data, "arrow_placement/special_placements.json")

    def handle_non_hybrid_letters(self, data: Dict[Letters, Dict], adjustment):
        red_turns = self.red_motion.turns
        blue_turns = self.blue_motion.turns

        if red_turns in [0.0, 1.0, 2.0, 3.0]:
            adjustment_key = (blue_turns, int(red_turns))
        elif red_turns in [0.5, 1.5, 2.5]:
            adjustment_key = (blue_turns, red_turns)
        elif blue_turns in [0.0, 1.0, 2.0, 3.0]:
            adjustment_key = (int(blue_turns), red_turns)
        elif blue_turns in [0.5, 1.5, 2.5]:
            adjustment_key = (blue_turns, red_turns)
        elif red_turns in [0.0, 1.0, 2.0, 3.0] and blue_turns in [0.0, 1.0, 2.0, 3.0]:
            adjustment_key = (int(blue_turns), int(red_turns))

        if data.get(self.pictograph.letter, {}) is None:
            data[self.pictograph.letter] = {}
            

        turn_data = data.get(self.pictograph.letter, {}).get(str(adjustment_key), {})

        if turn_data:
            letter_data = data.get(self.pictograph.letter)
            turn_data[self.pictograph.selected_arrow.color][0] += adjustment[0]
            turn_data[self.pictograph.selected_arrow.color][1] += adjustment[1]
            letter_data[str(adjustment_key)] = turn_data
            data[self.pictograph.letter] = letter_data
        elif data.get(self.pictograph.letter, {}) is not None and not turn_data:
            letter_data = data.get(self.pictograph.letter, {})
            # Get default values from default_placements.json
            default_data = self.load_json_data(
                "arrow_placement/default_placements.json"
            )
            default_turn_data = default_data.get(
                self.pictograph.selected_arrow.motion_type
            ).get(str(self.pictograph.selected_arrow.turns))
            if default_turn_data:
                turn_data = {
                    BLUE: [
                        default_turn_data[0] + adjustment[0],
                        default_turn_data[1] + adjustment[1],
                    ],
                    RED: [
                        default_turn_data[0] + adjustment[0],
                        default_turn_data[1] + adjustment[1],
                    ],
                }
            letter_data[str(adjustment_key)] = turn_data
            data[self.pictograph.letter] = letter_data

    def handle_pro_anti_hybrid_letters(self, data: Dict, adjustment):
        self.pro_motion = (
            self.red_motion if self.red_motion.motion_type == PRO else self.blue_motion
        )
        self.anti_motion = (
            self.blue_motion
            if self.blue_motion.motion_type == ANTI
            else self.red_motion
        )

        adjustment_key = (self.pro_motion.turns, self.anti_motion.turns)
        letter_data = data.get(self.pictograph.letter, {})
        turn_data = letter_data.get(str(adjustment_key))

        if turn_data:
            turn_data[self.pictograph.selected_arrow.motion_type][0] += adjustment[0]
            turn_data[self.pictograph.selected_arrow.motion_type][1] += adjustment[1]
            letter_data[str(adjustment_key)] = turn_data
            data[self.pictograph.letter] = letter_data

        elif not turn_data:
            # Get default values from default_placements.json
            default_data = self.load_json_data(
                "arrow_placement/default_placements.json"
            )
            default_turn_data = default_data.get(
                self.pictograph.selected_arrow.motion_type
            ).get(str(self.pictograph.selected_arrow.turns))
            if default_turn_data:
                turn_data = {
                    self.pro_motion.motion_type: [
                        default_turn_data[0] + adjustment[0],
                        default_turn_data[1] + adjustment[1],
                    ],
                    self.anti_motion.motion_type: [
                        default_turn_data[0] + adjustment[0],
                        default_turn_data[1] + adjustment[1],
                    ],
                }
            letter_data[str(adjustment_key)] = turn_data
            data[self.pictograph.letter] = letter_data

    def handle_shift_static_hybrid_letters(self, data: Dict, adjustment):
        
        shift_motion = (
            self.red_motion
            if self.red_motion.motion_type in [PRO, ANTI, FLOAT]
            else self.blue_motion
        )
        static_motion = (
            self.red_motion
            if self.red_motion.motion_type == STATIC
            else self.blue_motion
        )
        other_arrow = (
            self.red_motion
            if self.pictograph.selected_arrow == self.blue_motion.arrow
            else self.blue_motion.arrow
        )
        if static_motion.prop_rot_dir == shift_motion.prop_rot_dir:
            direction = "opp"
        elif static_motion.prop_rot_dir != shift_motion.prop_rot_dir:
            direction = "same"

        static_motion_key = f"{static_motion.motion_type}_{direction}"

        adjustment_key = (shift_motion.turns, static_motion.turns)
        letter_data = data.get(self.pictograph.letter, {})
        turn_data = letter_data.get(str(adjustment_key))

        if turn_data and self.pictograph.selected_arrow.motion_type in [PRO, ANTI, FLOAT]:
            turn_data[self.pictograph.selected_arrow.motion_type][0] += adjustment[0]
            turn_data[self.pictograph.selected_arrow.motion_type][1] += adjustment[1]
            letter_data[str(adjustment_key)] = turn_data
            data[self.pictograph.letter] = letter_data

        elif turn_data and self.pictograph.selected_arrow.motion_type == STATIC:
            turn_data[static_motion_key][0] += adjustment[0]
            turn_data[static_motion_key][1] += adjustment[1]
            letter_data[str(adjustment_key)] = turn_data
            data[self.pictograph.letter] = letter_data

        elif not turn_data:
            default_data = self.load_json_data(
                "arrow_placement/default_placements.json"
            )
            default_turn_data_for_selected_arrow = default_data.get(
                self.pictograph.selected_arrow.motion_type
            ).get(str(self.pictograph.selected_arrow.turns))

            default_turn_data_for_other_arrow = default_data.get(
                other_arrow.motion_type
            ).get(str(other_arrow.turns))

            if self.pictograph.selected_arrow.motion_type == shift_motion.motion_type:
                turn_data = {
                    shift_motion.motion_type: [
                        default_turn_data_for_selected_arrow[0] + adjustment[0],
                        default_turn_data_for_selected_arrow[1] + adjustment[1],
                    ],
                    static_motion_key: [
                        default_turn_data_for_other_arrow[0] + adjustment[0],
                        default_turn_data_for_other_arrow[1] + adjustment[1],
                    ],
                }
            elif (
                self.pictograph.selected_arrow.motion_type == static_motion.motion_type
            ):
                turn_data = {
                    shift_motion.motion_type: [
                        default_turn_data_for_other_arrow[0] + adjustment[0],
                        default_turn_data_for_other_arrow[1] + adjustment[1],
                    ],
                    static_motion_key: [
                        default_turn_data_for_selected_arrow[0] + adjustment[0],
                        default_turn_data_for_selected_arrow[1] + adjustment[1],
                    ],
                }
            letter_data[str(adjustment_key)] = turn_data
            data[self.pictograph.letter] = letter_data

    def handle_S_T(self, data: Dict, adjustment):
        adjustment_key = (self.leading_motion.turns, self.trailing_motion.turns)
        letter_data = data.get(self.pictograph.letter, {})
        turn_data = letter_data.get(str(adjustment_key))

        if not turn_data:
            # Create new entry with default values
            default_leading_pos = (
                self.leading_motion.arrow.pos().x(),
                self.leading_motion.arrow.pos().y(),
            )
            default_trailing_pos = (
                self.trailing_motion.arrow.pos().x(),
                self.trailing_motion.arrow.pos().y(),
            )

            turn_data = {
                self.leading_motion.arrow.lead_state: [
                    default_leading_pos[0] + adjustment[0],
                    default_leading_pos[1] + adjustment[1],
                ],
                self.trailing_motion.arrow.lead_state: [
                    default_trailing_pos[0] + adjustment[0],
                    default_trailing_pos[1] + adjustment[1],
                ],
            }
        else:
            # Update existing entry
            turn_data[self.leading_motion.arrow.lead_state][0] += adjustment[0]
            turn_data[self.leading_motion.arrow.lead_state][1] += adjustment[1]
            turn_data[self.trailing_motion.arrow.lead_state][0] += adjustment[0]
            turn_data[self.trailing_motion.arrow.lead_state][1] += adjustment[1]

        letter_data[str(adjustment_key)] = turn_data
        data[self.pictograph.letter] = letter_data

    def load_json_data(self, file_path) -> Dict:
        with open(file_path, "r") as file:
            return json.load(file)

    def write_json_data(self, data, file_path) -> None:
        json_str = json.dumps(data, indent=2)
        compact_json_str = re.sub(
            r'": \[\s+(-?\d+),\s+(-?\d+)\s+\]', r'": [\1, \2]', json_str
        )
        with open(file_path, "w") as file:
            file.write(compact_json_str)

    def get_adjustment(
        self, key, increment
    ) -> Tuple[Union[int, float], Union[int, float]]:
        direction_map = {
            Qt.Key.Key_W: (0, -1),
            Qt.Key.Key_A: (-1, 0),
            Qt.Key.Key_S: (0, 1),
            Qt.Key.Key_D: (1, 0),
        }
        dx, dy = direction_map.get(key, (0, 0))
        if self.pictograph.letter == "P":
            dx, dy = self.adjust_direction_p(dx, dy)
        elif self.pictograph.letter == "Q":
            dx, dy = self.adjust_direction_q(dx, dy)
        elif (
            self.pictograph.letter in "ST"
            and self.pictograph.selected_arrow.lead_state in [LEADING, TRAILING]
        ):
            dy, dx = dx, dy
        return dx * increment, dy * increment

    def adjust_direction_p(self, dx, dy):
        # Specific logic for letter "P"
        if self.pictograph.selected_arrow.motion.prop_rot_dir == COUNTER_CLOCKWISE:
            return -dx, dy
        elif self.pictograph.selected_arrow.motion.prop_rot_dir == CLOCKWISE:
            return -dy, dx
        return dx, dy

    def adjust_direction_q(self, dx, dy):
        # Specific logic for letter "Q"
        if self.pictograph.selected_arrow.motion.prop_rot_dir == COUNTER_CLOCKWISE:
            return -dy, dx
        elif self.pictograph.selected_arrow.motion.prop_rot_dir == CLOCKWISE:
            return dy, -dx
        return dx, dy

    def get_default_adjustment(self, key, increment):
        adjustment_map = {
            Qt.Key.Key_W: (0, -increment),
            Qt.Key.Key_A: (-increment, 0),
            Qt.Key.Key_S: (0, increment),
            Qt.Key.Key_D: (increment, 0),
        }
        return adjustment_map.get(key, (0, 0))
