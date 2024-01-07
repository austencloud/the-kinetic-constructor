import json
import re
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView
from constants import BLUE, RED
from objects.pictograph.pictograph import Pictograph
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from widgets.ig_tab.ig_scroll.ig_scroll import IGScrollArea


class IGPictograph(Pictograph):
    def __init__(self, main_widget, ig_scroll_area: "IGScrollArea"):
        super().__init__(main_widget, "ig_pictograph")
        self.view = IG_Pictograph_View(self)
        self.ig_scroll_area = ig_scroll_area
        self.selected_arrow = None  # New attribute for the selected arrow
        self.last_key = None
        self.last_shift_state = None
    def handle_arrow_movement(self, key, shift_held):
        if not self.selected_arrow:
            return

        adjustment_increment = 10 if shift_held else 5
        adjustment_map = {
            Qt.Key.Key_W: (0, -adjustment_increment),
            Qt.Key.Key_A: (-adjustment_increment, 0),
            Qt.Key.Key_S: (0, adjustment_increment),
            Qt.Key.Key_D: (adjustment_increment, 0),
        }
        adjustment = adjustment_map.get(key, (0, 0))
        self.selected_arrow.adjust_position(adjustment)
        self.update_arrow_adjustments_in_json(adjustment)

        # Update last movement details
        self.last_key = key
        self.last_shift_state = shift_held

    def last_movement_matches(self, key, shift_held):
        # Check if the last movement matches the current event
        return self.last_key == key and self.last_shift_state == shift_held

    def update_arrow_adjustments_in_json(self, adjustment):
        if not self.selected_arrow:
            return

        # Ensure turns are integers if they are whole numbers
        if self.motions[BLUE].turns in [0.0, 1.0, 2.0, 3.0]:
            self.motions[BLUE].turns = int(self.motions[BLUE].turns)
        if self.motions[RED].turns in [0.0, 1.0, 2.0, 3.0]:
            self.motions[RED].turns = int(self.motions[RED].turns)
        adjustment_key = (self.motions[BLUE].turns, self.motions[RED].turns)

        # Load the existing JSON data
        with open("arrow_placement/arrow_placements.json", "r") as file:
            data = json.load(file)

        if self.letter in ["E", "F", "G", "H"]:
            # Update for specific letters
            letter_data = data.get(self.letter, {})
            turn_data = letter_data.get(
                str(adjustment_key), {"blue": [0, 0], "red": [0, 0]}
            )
            turn_data[self.selected_arrow.color][0] += adjustment[
                0
            ]  # Update X adjustment
            turn_data[self.selected_arrow.color][1] += adjustment[
                1
            ]  # Update Y adjustment
            letter_data[str(adjustment_key)] = turn_data
            data[self.letter] = letter_data
        elif self.letter in ["I", "R"]:
            # Apply changes to both the current key and its reversed counterpart
            letter_data = data.get(self.letter, {})
            turn_data_current = letter_data.get(
                str(adjustment_key), {"pro": [0, 0], "anti": [0, 0]}
            )
            turn_data_reversed = letter_data.get(
                str(adjustment_key[::-1]), {"pro": [0, 0], "anti": [0, 0]}
            )

            # Update the adjustments for both keys
            turn_data_current[self.selected_arrow.motion_type][0] += adjustment[
                0
            ]  # Update X adjustment
            turn_data_current[self.selected_arrow.motion_type][1] += adjustment[
                1
            ]  # Update Y adjustment
            turn_data_reversed[self.selected_arrow.motion_type][0] += adjustment[
                0
            ]  # Update X adjustment
            turn_data_reversed[self.selected_arrow.motion_type][1] += adjustment[
                1
            ]  # Update Y adjustment

            letter_data[str(adjustment_key)] = turn_data_current
            letter_data[str(adjustment_key[::-1])] = turn_data_reversed
            data[self.letter] = letter_data

        # Convert data to JSON string with specified indentation
        json_str = json.dumps(data, indent=2)

        # Adjust the formatting of arrays to be on a single line
        compact_json_str = re.sub(
            r'": \[\s+(-?\d+),\s+(-?\d+)\s+\]', r'": [\1, \2]', json_str
        )

        # Write the compacted JSON string back to the file
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

        # Set the focus policy to accept keyboard input
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

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
            event.accept()  # Accept the event to prevent further propagation
        elif event.key() in [Qt.Key.Key_W, Qt.Key.Key_A, Qt.Key.Key_S, Qt.Key.Key_D]:
            # Check if the selected arrow's last movement matches the current event
            # If not, proceed with handling the movement
            if not self.ig_pictograph.last_movement_matches(event.key(), shift_held):
                self.ig_pictograph.handle_arrow_movement(event.key(), shift_held)
        else:
            super().keyPressEvent(event)
