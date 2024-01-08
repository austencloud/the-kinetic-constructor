import json
import re
from typing import TYPE_CHECKING, Dict, Tuple, Union
from PyQt6.QtWidgets import QGraphicsView
from constants import ANTI, BLUE, LEADING, PRO, RED, TRAILING
from objects.pictograph.pictograph import Pictograph
from PyQt6.QtCore import Qt

from utilities.TypeChecking.TypeChecking import Colors


if TYPE_CHECKING:
    from widgets.ig_tab.ig_scroll.ig_scroll import IGScrollArea


class IGPictograph(Pictograph):
    def __init__(self, main_widget, ig_scroll_area: "IGScrollArea") -> None:
        super().__init__(main_widget, "ig_pictograph")
        self.view = IG_Pictograph_View(self)
        self.ig_scroll_area = ig_scroll_area
        self.selected_arrow = None

    def handle_arrow_movement(self, key, shift_held) -> None:
        if not self.selected_arrow:
            return

        adjustment_increment = 15 if shift_held else 5
        adjustment = self.get_adjustment(key, adjustment_increment)
        self.update_arrow_adjustments_in_json(adjustment)

    def get_adjustment(
        self, key, increment
    ) -> Tuple[Union[int, float], Union[int, float]]:
        if self.letter in "PQRST":
            return self.get_letter_specific_adjustment(key, increment)
        else:
            return self.get_default_adjustment(key, increment)

    def get_letter_specific_adjustment(self, key, increment):
        direction_map = {
            Qt.Key.Key_W: (-1, 1),
            Qt.Key.Key_A: (1, -1),
            Qt.Key.Key_S: (1, -1),
            Qt.Key.Key_D: (-1, 1),
        }

        dx, dy = direction_map.get(key, (0, 0))

        if self.letter in "PQR" and self.selected_arrow.color in [RED, BLUE]:
            dx, dy = dy, dx

        if self.letter in "ST" and self.selected_arrow.lead_state in [
            LEADING,
            TRAILING,
        ]:
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

    def determine_leading_color(
        self, red_start, red_end, blue_start, blue_end
    ) -> Colors:
        if red_start == blue_end:
            return RED
        elif blue_start == red_end:
            return BLUE
        return None

    def update_arrow_adjustments_in_json(self, adjustment) -> None:
        if not self.selected_arrow:
            return
        if self.letter in ["S", "T"]:
            leading_color = self.determine_leading_color(
                self.motions[RED].start_loc,
                self.motions[RED].end_loc,
                self.motions[BLUE].start_loc,
                self.motions[BLUE].end_loc,
            )
            leading_motion = self.motions[leading_color]
            trailing_motion = self.motions[BLUE if leading_color == RED else RED]

        red_motion = self.motions[RED]
        blue_motion = self.motions[BLUE]
        if blue_motion.turns in [0.0, 1.0, 2.0, 3.0]:
            blue_motion.turns = int(blue_motion.turns)
        if red_motion.turns in [0.0, 1.0, 2.0, 3.0]:
            red_motion.turns = int(red_motion.turns)
        pro_motion = red_motion if red_motion.motion_type == PRO else blue_motion
        anti_motion = blue_motion if blue_motion.motion_type == ANTI else red_motion
        with open("arrow_placement/arrow_placements.json", "r") as file:
            data: Dict = json.load(file)
        if self.letter in ["E", "G", "H", "P", "Q"]:
            adjustment_key = (blue_motion.turns, red_motion.turns)
            letter_data: Dict = data.get(self.letter, {})
            turn_data = letter_data.get(str(adjustment_key))
            if turn_data:
                turn_data[self.selected_arrow.color][0] += adjustment[0]
                turn_data[self.selected_arrow.color][1] += adjustment[1]
                letter_data[str(adjustment_key)] = turn_data
                data[self.letter] = letter_data
        elif self.letter in ["I", "R", "U", "V"]:
            adjustment_key = (pro_motion.turns, anti_motion.turns)
            letter_data = data.get(self.letter, {})
            turn_data = letter_data.get(str(adjustment_key))
            if turn_data:
                turn_data[self.selected_arrow.motion_type][0] += adjustment[0]
                turn_data[self.selected_arrow.motion_type][1] += adjustment[1]
                letter_data[str(adjustment_key)] = turn_data
                data[self.letter] = letter_data
        elif self.letter in ["S", "T"]:
            adjustment_key = (leading_motion.turns, trailing_motion.turns)
            letter_data = data.get(self.letter, {})
            turn_data = letter_data.get(str(adjustment_key))
            if turn_data:
                turn_data[self.selected_arrow.lead_state][0] += adjustment[0]
                turn_data[self.selected_arrow.lead_state][1] += adjustment[1]
                letter_data[str(adjustment_key)] = turn_data
                data[self.letter] = letter_data
        json_str = json.dumps(data, indent=2)

        compact_json_str = re.sub(
            r'": \[\s+(-?\d+),\s+(-?\d+)\s+\]', r'": [\1, \2]', json_str
        )
        with open("arrow_placement/arrow_placements.json", "w") as file:
            file.write(compact_json_str)

    def swap_selected_arrow(self):
        if self.selected_arrow == self.arrows[RED]:
            self.arrows[RED].setSelected(False)
            self.selected_arrow = self.arrows[BLUE]
            self.arrows[BLUE].setSelected(True)
        elif self.selected_arrow == self.arrows[BLUE]:
            self.arrows[BLUE].setSelected(False)
            self.selected_arrow = self.arrows[RED]
            self.arrows[RED].setSelected(True)
        else:
            print("No arrow selected")


class IG_Pictograph_View(QGraphicsView):
    def __init__(self, ig_pictograph: IGPictograph) -> None:
        super().__init__(ig_pictograph)
        self.ig_pictograph = ig_pictograph
        self.setScene(self.ig_pictograph)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def resize_for_scroll_area(self) -> None:
        view_width = (
            int(
                self.ig_pictograph.ig_scroll_area.width()
                / self.ig_pictograph.ig_scroll_area.COLUMN_COUNT
            )
            - self.ig_pictograph.ig_scroll_area.SPACING
        )

        self.setMinimumWidth(view_width)
        self.setMaximumWidth(view_width)
        self.setMinimumHeight(view_width)
        self.setMaximumHeight(view_width)

        self.view_scale = view_width / self.ig_pictograph.width()

        self.resetTransform()
        self.scale(self.view_scale, self.view_scale)
        self.ig_pictograph.view_scale = self.view_scale

    def wheelEvent(self, event) -> None:
        self.ig_pictograph.ig_scroll_area.wheelEvent(event)

    def keyPressEvent(self, event) -> None:
        shift_held = event.modifiers() & Qt.KeyboardModifier.ShiftModifier
        if event.key() == Qt.Key.Key_Q:
            self.ig_pictograph.swap_selected_arrow()
            event.accept()
        elif event.key() in [Qt.Key.Key_W, Qt.Key.Key_A, Qt.Key.Key_S, Qt.Key.Key_D]:
            self.ig_pictograph.handle_arrow_movement(event.key(), shift_held)
        else:
            super().keyPressEvent(event)
