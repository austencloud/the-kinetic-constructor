import json
import re
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView
from constants import ANTI, BLUE, PRO, RED
from objects.pictograph.pictograph import Pictograph
from PyQt6.QtCore import Qt


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
        adjustment = (0, 0)

        if self.letter == "P":
            adjustment = self._get_P_letter_adjustment(key, adjustment_increment)
        elif self.letter == "Q":
            adjustment = self.get_Q_letter_adjustment(key, adjustment_increment)
        elif self.letter == "R":
            adjustment = self._get_R_letter_adjustment(key, adjustment_increment)
        elif self.letter == "S":
            adjustment = self._get_S_letter_adjustment(key, adjustment_increment)
        else:
            adjustment_map = {
                Qt.Key.Key_W: (0, -adjustment_increment),
                Qt.Key.Key_A: (-adjustment_increment, 0),
                Qt.Key.Key_S: (0, adjustment_increment),
                Qt.Key.Key_D: (adjustment_increment, 0),
            }
            adjustment = adjustment_map.get(key, (0, 0))

        self.update_arrow_adjustments_in_json(adjustment)

    def _get_S_letter_adjustment(self, key, increment):
        if self.selected_arrow.color == BLUE:
            # Special mapping for blue arrow when letter is S
            return {
                Qt.Key.Key_W: (increment, 0),
                Qt.Key.Key_A: (0, -increment),
                Qt.Key.Key_S: (-increment, 0),
                Qt.Key.Key_D: (0, increment),
            }.get(key, (0, 0))
        elif self.selected_arrow.color == RED:
            # Special mapping for red arrow when letter is S
            return {
                Qt.Key.Key_W: (0, -increment),
                Qt.Key.Key_A: (increment, 0),
                Qt.Key.Key_S: (0, increment),
                Qt.Key.Key_D: (-increment, 0),
            }.get(key, (0, 0))
        return (0, 0)

    def _get_R_letter_adjustment(self, key, increment):
        if self.selected_arrow.color == BLUE:
            # Special mapping for blue arrow when letter is R
            return {
                Qt.Key.Key_W: (increment, 0),
                Qt.Key.Key_A: (0, -increment),
                Qt.Key.Key_S: (-increment, 0),
                Qt.Key.Key_D: (0, increment),
            }.get(key, (0, 0))
        elif self.selected_arrow.color == RED:
            # Special mapping for red arrow when letter is R
            return {
                Qt.Key.Key_W: (0, -increment),
                Qt.Key.Key_A: (increment, 0),
                Qt.Key.Key_S: (0, increment),
                Qt.Key.Key_D: (-increment, 0),
            }.get(key, (0, 0))
        return (0, 0)

    def get_Q_letter_adjustment(self, key, increment):
        if self.selected_arrow.color == BLUE:
            # Special mapping for blue arrow when letter is Q
            return {
                Qt.Key.Key_W: (increment, 0),
                Qt.Key.Key_A: (0, -increment),
                Qt.Key.Key_S: (-increment, 0),
                Qt.Key.Key_D: (0, increment),
            }.get(key, (0, 0))
        elif self.selected_arrow.color == RED:
            # Special mapping for red arrow when letter is Q
            return {
                Qt.Key.Key_W: (0, -increment),
                Qt.Key.Key_A: (increment, 0),
                Qt.Key.Key_S: (0, increment),
                Qt.Key.Key_D: (-increment, 0),
            }.get(key, (0, 0))
        return (0, 0)

    def _get_P_letter_adjustment(self, key, increment):
        if self.selected_arrow.color == BLUE:
            # Special mapping for blue arrow when letter is P
            return {
                Qt.Key.Key_W: (increment, 0),
                Qt.Key.Key_A: (0, -increment),
                Qt.Key.Key_S: (-increment, 0),
                Qt.Key.Key_D: (0, increment),
            }.get(key, (0, 0))
        elif self.selected_arrow.color == RED:
            # Special mapping for red arrow when letter is P
            return {
                Qt.Key.Key_W: (0, -increment),
                Qt.Key.Key_A: (increment, 0),
                Qt.Key.Key_S: (0, increment),
                Qt.Key.Key_D: (-increment, 0),
            }.get(key, (0, 0))
        return (0, 0)

    def update_arrow_adjustments_in_json(self, adjustment) -> None:
        if not self.selected_arrow:
            return

        red_motion = self.motions[RED]
        blue_motion = self.motions[BLUE]
        if blue_motion.turns in [0.0, 1.0, 2.0, 3.0]:
            blue_motion.turns = int(blue_motion.turns)
        if red_motion.turns in [0.0, 1.0, 2.0, 3.0]:
            red_motion.turns = int(red_motion.turns)
        pro_motion = red_motion if red_motion.motion_type == PRO else blue_motion
        anti_motion = blue_motion if blue_motion.motion_type == ANTI else red_motion
        with open("arrow_placement/arrow_placements.json", "r") as file:
            data = json.load(file)
        if self.letter in ["E", "F", "G", "H", "P", "Q"]:
            adjustment_key = (blue_motion.turns, red_motion.turns)
            letter_data = data.get(self.letter, {})
            turn_data = letter_data.get(str(adjustment_key))
            turn_data[self.selected_arrow.color][0] += adjustment[0]
            turn_data[self.selected_arrow.color][1] += adjustment[1]
            letter_data[str(adjustment_key)] = turn_data
            data[self.letter] = letter_data
        elif self.letter in ["I", "R"]:
            adjustment_key = (pro_motion.turns, anti_motion.turns)
            letter_data = data.get(self.letter, {})
            turn_data = letter_data.get(str(adjustment_key))
            turn_data[self.selected_arrow.motion_type][0] += adjustment[0]
            turn_data[self.selected_arrow.motion_type][1] += adjustment[1]
            letter_data[str(adjustment_key)] = turn_data
            data[self.letter] = letter_data
        elif self.letter in ["S", "T"]:
            adjustment_key = (pro_motion.turns, anti_motion.turns)
            letter_data = data.get(self.letter, {})
            turn_data = letter_data.get(str(adjustment_key))
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
        view_width = int(
            self.ig_pictograph.ig_scroll_area.width() / 4
        ) - self.ig_pictograph.ig_scroll_area.SPACING * (
            self.ig_pictograph.ig_scroll_area.COLUMN_COUNT - 1
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
