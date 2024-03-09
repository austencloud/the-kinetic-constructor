from PyQt6.QtWidgets import QFrame, QHBoxLayout, QApplication
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from Enums.Enums import LetterType, Letter

import pandas as pd
from constants import BLUE_START_ORI, BLUE_TURNS, RED_START_ORI, RED_TURNS
from Enums.Enums import LetterType


from widgets.pictograph.components.add_to_sequence_manager import (
    AddToSequenceManager,
)
from .components.start_position_picker.start_pos_picker import StartPosPicker
from ..pictograph.pictograph import Pictograph
from .components.option_picker.option_picker_click_handler import (
    OptionPickerClickHandler,
)
from .components.option_picker.option_picker import OptionPicker

if TYPE_CHECKING:
    from ..main_widget.main_widget import MainWidget


class SequenceBuilder(QFrame):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.current_pictograph: Pictograph = None
        self.letters_df = pd.read_csv("PictographDataframe.csv")
        self.start_position_picked = False
        self._setup_components()
        self.pictograph_cache: dict[Letter, dict[str, Pictograph]] = {
            letter: {} for letter in Letter
        }
        self.start_pos_picker = StartPosPicker(self)
        self.option_picker = OptionPicker(self)
        self.add_to_sequence_manager = AddToSequenceManager(self)
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.start_pos_picker)

    def _setup_components(self) -> None:
        self.option_click_handler = OptionPickerClickHandler(self)

    def transition_to_sequence_building(self):
        self.start_position_picked = True
        self._hide_start_pos_picker()
        self._show_option_picker()
        QApplication.restoreOverrideCursor()

    def _hide_start_pos_picker(self):
        self.start_pos_picker.hide()
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.layout().removeWidget(self.start_pos_picker)

    def _show_option_picker(self):
        self.layout().addWidget(self.option_picker)
        self.option_picker.show()
        self.option_picker.scroll_area.sections_manager.show_all_sections()
        self.option_picker.update_option_picker()
        self.option_picker.scroll_area.display_manager.order_and_display_pictographs()

    def render_and_store_pictograph(self, pictograph_dict: dict) -> Pictograph:
        pictograph_dict = self._add_turns_and_start_ori(pictograph_dict)
        letter_str = pictograph_dict["letter"]
        letter = Letter.get_letter(letter_str)
        letter_type = LetterType.get_letter_type(letter)
        pictograph_key = (
            self.main_widget.pictograph_key_generator.generate_pictograph_key(
                pictograph_dict
            )
        )

        scroll_area = self.option_picker.scroll_area
        if pictograph_key in scroll_area.pictograph_cache:
            return scroll_area.pictograph_cache[pictograph_key]

        new_pictograph = scroll_area.pictograph_factory.get_or_create_pictograph(
            pictograph_key, pictograph_dict
        )
        scroll_area.pictograph_cache[pictograph_key] = new_pictograph
        self.main_widget.all_pictographs[new_pictograph.letter][
            pictograph_key
        ] = new_pictograph
        if pictograph_key not in self.pictograph_cache[letter]:
            self.pictograph_cache[letter][pictograph_key] = new_pictograph
        section = scroll_area.sections_manager.get_section(letter_type)
        section.pictographs[pictograph_key] = new_pictograph
        scroll_area.pictograph_cache[pictograph_key] = new_pictograph
        self.main_widget.all_pictographs[new_pictograph.letter][
            pictograph_key
        ] = new_pictograph
        return new_pictograph

    def _add_turns_and_start_ori(self, pictograph_dict):
        self.current_end_red_ori = (
            self.main_widget.json_manager.current_sequence_json_handler.get_red_end_ori()
        )
        self.current_end_blue_ori = (
            self.main_widget.json_manager.current_sequence_json_handler.get_blue_end_ori()
        )

        pictograph_dict[RED_START_ORI] = self.current_end_red_ori
        pictograph_dict[BLUE_START_ORI] = self.current_end_blue_ori
        pictograph_dict[RED_TURNS] = 0
        pictograph_dict[BLUE_TURNS] = 0
        return pictograph_dict

    def reset_to_start_pos_picker(self):
        self.start_position_picked = False
        self.option_picker.hide()
        self.layout().removeWidget(self.option_picker)
        self.layout().addWidget(self.start_pos_picker)
        self.start_pos_picker.show()

    def resize_sequence_builder(self) -> None:
        self.setMinimumWidth(int(self.main_widget.width() / 2))
        self.start_pos_picker.resize_start_position_picker()
        # self.option_picker.scroll_area.resize_option_picker_scroll_area()

    def get_last_added_pictograph(self):
        return self.main_widget.json_manager.current_sequence_json_handler.load_current_sequence_json()[
            -1
        ]
