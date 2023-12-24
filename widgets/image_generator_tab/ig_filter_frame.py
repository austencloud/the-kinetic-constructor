from typing import TYPE_CHECKING, Dict, Union
from Enums import Orientation
from filter_frame import FilterFrame
from utilities.TypeChecking.TypeChecking import Turns

if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_tab import IGTab


class IGFilterFrame(FilterFrame):
    def __init__(self, ig_tab: "IGTab") -> None:
        super().__init__(ig_tab)
        self.ig_tab = ig_tab
        self.apply_filters()

        self.left_end_orientation_combobox.currentTextChanged.connect(
            self.apply_filters
        )

    def apply_filters(self) -> None:
        selected_blue_turns = [
            turn
            for turn, checkbox in self.blue_turn_checkboxes.items()
            if checkbox.isChecked()
        ][
            0
        ]  # Access the first element of the list
        selected_red_turns = [
            turn
            for turn, checkbox in self.red_turn_checkboxes.items()
            if checkbox.isChecked()
        ][
            0
        ]  # Access the first element of the list
        selected_left_end_orientation = self.left_end_orientation_combobox.currentText()
        selected_right_end_orientation = (
            self.right_end_orientation_combobox.currentText()
        )

        self.filters: Dict[str, Union[Turns, Orientation]] = {
            "blue_turns": selected_blue_turns,
            "red_turns": selected_red_turns,
            "left_end_orientation": selected_left_end_orientation,
            "right_end_orientation": selected_right_end_orientation,
        }

        self.ig_tab.ig_scroll_area.apply_turn_filters(self.filters)
