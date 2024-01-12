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
from objects.arrow.arrow_placement_manager.special_arrow_placement_manager import (
    SpecialArrowPlacementManager,
)

from objects.pictograph.pictograph import Pictograph
import codecs
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
        if new_turns in [0.0, 1.0, 2.0, 3.0]:
            new_turns = int(new_turns)
        pictograph_dict = {f"{self.pictograph.selected_arrow.color}_turns": new_turns}
        self.pictograph.update_pictograph(pictograph_dict)

    def handle_arrow_movement(self, key, shift_held) -> None:
        if not self.pictograph.selected_arrow:
            return

        adjustment_increment = 15 if shift_held else 5
        adjustment = self.get_adjustment(key, adjustment_increment)
        self.update_arrow_adjustments_in_json(
            adjustment,
            self.pictograph.arrow_placement_manager.special_placement_manager,
        )

    def handle_rotation_angle_override(self) -> None:
        if (
            not self.pictograph.selected_arrow
            or self.pictograph.selected_arrow.motion.motion_type != STATIC
        ):
            return

        data = self.load_json_data("arrow_placement/special_placements.json")
        adjustment_key = (
            self.pictograph.arrow_placement_manager.generate_adjustment_key()
        )

        # Update the JSON data with the rotation angle override
        letter_data = data.get(self.pictograph.letter, {})
        if adjustment_key in letter_data:
            turn_data = letter_data.get(adjustment_key, {})
            turn_data["static_rot_angle"] = 0
            letter_data[adjustment_key] = turn_data
            data[self.pictograph.letter] = letter_data
            self.write_json_data(data, "arrow_placement/special_placements.json")

    def update_arrow_adjustments_in_json(
        self, adjustment, placement_manager: SpecialArrowPlacementManager
    ) -> None:
        if not self.pictograph.selected_arrow:
            return
        data = placement_manager.special_placements
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
        if handler(data, adjustment):
            placement_manager.data_modified = True
        placement_manager.update_specific_placement()

    def handle_non_hybrid_letters(self, data: Dict[Letters, Dict], adjustment) -> None:
        red_turns = self.red_motion.turns
        blue_turns = self.blue_motion.turns

        if blue_turns in [0.0, 1.0, 2.0, 3.0]:
            blue_turns = int(blue_turns)
        if red_turns in [0.0, 1.0, 2.0, 3.0]:
            red_turns = int(red_turns)

        adjustment_key = (blue_turns, red_turns)

        if data.get(self.pictograph.letter, {}) is None:
            data[self.pictograph.letter] = {}

        turn_data = data.get(self.pictograph.letter, {}).get(str(adjustment_key), {})

        if turn_data:
            letter_data = data.get(self.pictograph.letter)
            turn_data[self.pictograph.selected_arrow.color][0] += adjustment[0]
            turn_data[self.pictograph.selected_arrow.color][1] += adjustment[1]
            letter_data[str(adjustment_key)] = turn_data
            data[self.pictograph.letter] = letter_data
            return True
        elif data.get(self.pictograph.letter, {}) is not None and not turn_data:
            letter_data = data.get(self.pictograph.letter, {})
            default_data = self.load_json_data(
                "arrow_placement/default_placements.json"
            )
            default_turn_data_for_selected_arrow = default_data.get(
                self.pictograph.selected_arrow.motion_type
            ).get(str(self.pictograph.selected_arrow.turns))

            other_arrow = (
                self.red_motion
                if self.pictograph.selected_arrow == self.blue_motion.arrow
                else self.blue_motion.arrow
            )

            default_turn_data_for_other_arrow = default_data.get(
                other_arrow.motion_type
            ).get(str(other_arrow.turns))

            if self.pictograph.selected_arrow.color == BLUE:
                if default_turn_data_for_selected_arrow:
                    turn_data = {
                        BLUE: [
                            default_turn_data_for_selected_arrow[0] + adjustment[0],
                            default_turn_data_for_selected_arrow[1] + adjustment[1],
                        ],
                        RED: [
                            default_turn_data_for_other_arrow[0],
                            default_turn_data_for_other_arrow[1],
                        ],
                    }
            elif self.pictograph.selected_arrow.color == RED:
                if default_turn_data_for_selected_arrow:
                    turn_data = {
                        BLUE: [
                            default_turn_data_for_other_arrow[0],
                            default_turn_data_for_other_arrow[1],
                        ],
                        RED: [
                            default_turn_data_for_selected_arrow[0] + adjustment[0],
                            default_turn_data_for_selected_arrow[1] + adjustment[1],
                        ],
                    }
            letter_data[str(adjustment_key)] = turn_data
            data[self.pictograph.letter] = letter_data
            placement_manager = (
                self.pictograph.arrow_placement_manager.special_placement_manager
            )
            placement_manager.add_and_sort_new_entry(
                self.pictograph.letter, str(adjustment_key), turn_data
            )
            return True  # Indicates the data was modified
        return False  # No new entry was added, so data was not modified

    def handle_pro_anti_hybrid_letters(self, data: Dict, adjustment) -> None:
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
            default_turn_data_for_selected_arrow = default_data.get(
                self.pictograph.selected_arrow.motion_type
            ).get(str(self.pictograph.selected_arrow.turns))

            other_arrow = (
                self.red_motion
                if self.pictograph.selected_arrow == self.blue_motion.arrow
                else self.blue_motion.arrow
            )

            default_turn_data_for_other_arrow = default_data.get(
                other_arrow.motion_type
            ).get(str(other_arrow.turns))

            if self.pictograph.selected_arrow.motion_type == PRO:
                if default_turn_data_for_selected_arrow:
                    turn_data = {
                        self.pro_motion.motion_type: [
                            default_turn_data_for_selected_arrow[0] + adjustment[0],
                            default_turn_data_for_selected_arrow[1] + adjustment[1],
                        ],
                        self.anti_motion.motion_type: [
                            default_turn_data_for_other_arrow[0],
                            default_turn_data_for_other_arrow[1],
                        ],
                    }
            elif self.pictograph.selected_arrow.motion_type == ANTI:
                if default_turn_data_for_selected_arrow:
                    turn_data = {
                        self.pro_motion.motion_type: [
                            default_turn_data_for_other_arrow[0],
                            default_turn_data_for_other_arrow[1],
                        ],
                        self.anti_motion.motion_type: [
                            default_turn_data_for_selected_arrow[0] + adjustment[0],
                            default_turn_data_for_selected_arrow[1] + adjustment[1],
                        ],
                    }
            letter_data[str(adjustment_key)] = turn_data
            data[self.pictograph.letter] = letter_data

    def handle_shift_static_hybrid_letters(self, data: Dict, adjustment) -> None:
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
        if shift_motion.turns in [0.0, 1.0, 2.0, 3.0]:
            shift_motion.turns = int(shift_motion.turns)
        if static_motion.turns in [0.0, 1.0, 2.0, 3.0]:
            static_motion.turns = int(static_motion.turns)

        if static_motion.turns > 0:
            if static_motion.prop_rot_dir != shift_motion.prop_rot_dir:
                direction = "opp"
            elif static_motion.prop_rot_dir == shift_motion.prop_rot_dir:
                direction = "same"
            direction_prefix = direction[0]
            adjustment_key_str = (
                f"({direction_prefix}, {shift_motion.turns}, {static_motion.turns})"
            )
        elif static_motion.turns == 0:
            adjustment_key_str = f"({shift_motion.turns}, {static_motion.turns})"

        # Use adjustment_key_str in the rest of your code
        letter_data = data.get(self.pictograph.letter, {})
        turn_data = letter_data.get(adjustment_key_str)

        if turn_data and self.pictograph.selected_arrow.motion_type in [
            PRO,
            ANTI,
            FLOAT,
        ]:
            turn_data[self.pictograph.selected_arrow.motion_type][0] += adjustment[0]
            turn_data[self.pictograph.selected_arrow.motion_type][1] += adjustment[1]
            letter_data[adjustment_key_str] = turn_data
            data[self.pictograph.letter] = letter_data

        elif turn_data and self.pictograph.selected_arrow.motion_type == STATIC:
            turn_data[static_motion.motion_type][0] += adjustment[0]
            turn_data[static_motion.motion_type][1] += adjustment[1]
            letter_data[adjustment_key_str] = turn_data
            data[self.pictograph.letter] = letter_data
            self.pictograph.arrow_placement_manager.special_placement_manager.data_modified = (
                True
            )

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

            if self.pictograph.selected_arrow.motion.is_shift():
                turn_data = {
                    shift_motion.motion_type: [
                        default_turn_data_for_selected_arrow[0] + adjustment[0],
                        default_turn_data_for_selected_arrow[1] + adjustment[1],
                    ],
                    static_motion.motion_type: [
                        default_turn_data_for_other_arrow[0],
                        default_turn_data_for_other_arrow[1],
                    ],
                }
                letter_data[adjustment_key_str] = turn_data
                data[self.pictograph.letter] = letter_data

            elif self.pictograph.selected_arrow.motion.is_static():
                turn_data = {
                    shift_motion.motion_type: [
                        default_turn_data_for_other_arrow[0],
                        default_turn_data_for_other_arrow[1],
                    ],
                    static_motion.motion_type: [
                        default_turn_data_for_selected_arrow[0] + adjustment[0],
                        default_turn_data_for_selected_arrow[1] + adjustment[1],
                    ],
                }
                letter_data[adjustment_key_str] = turn_data
                data[self.pictograph.letter] = letter_data
                self.pictograph.arrow_placement_manager.special_placement_manager.data_modified = (
                    True
                )

    def handle_S_T(self, data: Dict, adjustment) -> None:
        self.leading_motion = self.pictograph.get_leading_motion()
        self.trailing_motion = (
            self.blue_motion
            if self.leading_motion == self.red_motion
            else self.red_motion
        )

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
            if self.pictograph.selected_arrow.motion_type == LEADING:
                turn_data = {
                    self.leading_motion.arrow.lead_state: [
                        default_leading_pos[0] + adjustment[0],
                        default_leading_pos[1] + adjustment[1],
                    ],
                    self.trailing_motion.arrow.lead_state: [
                        default_trailing_pos[0],
                        default_trailing_pos[1],
                    ],
                }
            elif self.pictograph.selected_arrow.motion_type == TRAILING:
                turn_data = {
                    self.leading_motion.arrow.lead_state: [
                        default_leading_pos[0],
                        default_leading_pos[1],
                    ],
                    self.trailing_motion.arrow.lead_state: [
                        default_trailing_pos[0] + adjustment[0],
                        default_trailing_pos[1] + adjustment[1],
                    ],
                }
        else:
            if self.pictograph.selected_arrow.motion_type == LEADING:
                turn_data[self.leading_motion.arrow.lead_state][0] += adjustment[0]
                turn_data[self.leading_motion.arrow.lead_state][1] += adjustment[1]
            elif self.pictograph.selected_arrow.motion_type == TRAILING:
                turn_data[self.trailing_motion.arrow.lead_state][0] += adjustment[0]
                turn_data[self.trailing_motion.arrow.lead_state][1] += adjustment[1]

        letter_data[str(adjustment_key)] = turn_data
        data[self.pictograph.letter] = letter_data

    def load_json_data(self, file_path) -> Dict:
        with codecs.open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    def write_json_data(self, data, file_path) -> None:
        if self.data_modified:
            json_str = json.dumps(data, indent=2)
            compact_json_str = re.sub(
                r'": \[\s+(-?\d+),\s+(-?\d+)\s+\]', r'": [\1, \2]', json_str
            )
            with codecs.open(file_path, "w", encoding="utf-8") as file:
                file.write(compact_json_str)
            self.data_modified = False

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
            dx, dy = self.adjust_direction_P(dx, dy)
        elif self.pictograph.letter == "Q":
            dx, dy = self.adjust_direction_Q(dx, dy)
        elif (
            self.pictograph.letter in "ST"
            and self.pictograph.selected_arrow.lead_state in [LEADING, TRAILING]
        ):
            dy, dx = dx, dy
        return dx * increment, dy * increment

    def adjust_direction_P(self, dx, dy) -> Tuple[int, int]:
        # Specific logic for letter "P"
        if self.pictograph.selected_arrow.motion.prop_rot_dir == COUNTER_CLOCKWISE:
            return -dx, dy
        elif self.pictograph.selected_arrow.motion.prop_rot_dir == CLOCKWISE:
            return -dy, dx
        return dx, dy

    def adjust_direction_Q(self, dx, dy) -> Tuple[int, int]:
        # Specific logic for letter "Q"
        if self.pictograph.selected_arrow.motion.prop_rot_dir == COUNTER_CLOCKWISE:
            return -dy, dx
        elif self.pictograph.selected_arrow.motion.prop_rot_dir == CLOCKWISE:
            return dy, -dx
        return dx, dy

    def get_default_adjustment(self, key, increment) -> Tuple[int, int]:
        adjustment_map = {
            Qt.Key.Key_W: (0, -increment),
            Qt.Key.Key_A: (-increment, 0),
            Qt.Key.Key_S: (0, increment),
            Qt.Key.Key_D: (increment, 0),
        }
        return adjustment_map.get(key, (0, 0))
