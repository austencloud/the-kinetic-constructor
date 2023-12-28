from typing import TYPE_CHECKING, Dict, Union
from Enums import Orientation
from widgets.filter_frame import FilterFrame
from utilities.TypeChecking.TypeChecking import Turns

if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_tab import IGTab


class IGFilterFrame(FilterFrame):
    def __init__(self, ig_tab: "IGTab") -> None:
        super().__init__(ig_tab)
        self.ig_tab = ig_tab
        self.apply_filters()

        self.left_end_or_combobox.currentTextChanged.connect(self.apply_filters)

    def apply_filters(self) -> None:
        selected_blue_turns = self.left_turns_combobox.currentText()
        selected_red_turns = self.right_turns_combobox.currentText()
        selected_left_end_or = self.left_end_or_combobox.currentText()
        selected_right_end_or = self.right_end_or_combobox.currentText()

        self.filters: Dict[str, Union[Turns, Orientation]] = {
            "blue_turns": selected_blue_turns,
            "red_turns": selected_red_turns,
            "left_end_or": selected_left_end_or,
            "right_end_or": selected_right_end_or,
        }

        self.ig_tab.ig_scroll_area.apply_turn_filters(self.filters)
