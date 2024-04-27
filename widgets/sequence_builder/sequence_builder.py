from PyQt6.QtWidgets import QFrame, QHBoxLayout, QApplication
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING
from Enums.Enums import LetterType, Letter
import pandas as pd
from constants import BLUE_START_ORI, BLUE_TURNS, RED_START_ORI, RED_TURNS
from Enums.Enums import LetterType

from path_helpers import get_images_and_data_path
from widgets.pictograph.components.add_to_sequence_manager import (
    AddToSequenceManager,
)
from widgets.sequence_builder.advanced_start_pos_picker.advanced_start_pos_picker import (
    AdvancedStartPosPicker,
)
from widgets.sequence_builder.components.start_pos_picker.start_pos_picker import (
    StartPosPicker,
)
from ..pictograph.pictograph import Pictograph
from .components.option_picker.option_picker_click_handler import (
    OptionPickerClickHandler,
)
from .components.option_picker.option_picker import OptionPicker

if TYPE_CHECKING:
    from widgets.main_builder_widget.builder_toolbar import BuilderToolbar
    from ..main_widget.main_widget import MainWidget


class SequenceBuilder(QFrame):
    def __init__(self, builder_toolbar: "BuilderToolbar"):
        super().__init__(builder_toolbar)
        self.builder_toolbar = builder_toolbar
        self.main_widget: "MainWidget" = builder_toolbar.main_widget
        self.current_pictograph: Pictograph = None

        csv_path = get_images_and_data_path("PictographDataframe.csv")
        self.letters_df = pd.read_csv(csv_path)
        self.start_position_picked = False
        self.pictograph_cache: dict[Letter, dict[str, Pictograph]] = {
            letter: {} for letter in Letter
        }
        self.option_click_handler = OptionPickerClickHandler(self)
        self.start_pos_picker = StartPosPicker(self)
        self.option_picker = OptionPicker(self)
        self.add_to_sequence_manager = AddToSequenceManager(self)
        self.advanced_start_pos_picker = AdvancedStartPosPicker(self)
        self.setLayout(QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout().addWidget(self.start_pos_picker)

        self.layout().addWidget(self.advanced_start_pos_picker)
        self.advanced_start_pos_picker.hide()  # Initially hidden

    def transition_to_sequence_building(self) -> None:
        self.start_position_picked = True
        self._hide_start_pos_picker()
        self._hide_advanced_start_pos_picker()
        self._show_option_picker()

    def transition_to_advanced_start_pos_picker(self) -> None:
        self._hide_start_pos_picker()
        self.show_advanced_start_pos_picker()

    def _hide_advanced_start_pos_picker(self) -> None:
        self.advanced_start_pos_picker.hide()
        self.layout().removeWidget(self.advanced_start_pos_picker)

    def _hide_start_pos_picker(self) -> None:
        self.start_pos_picker.hide()
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.layout().removeWidget(self.start_pos_picker)

    def show_advanced_start_pos_picker(self) -> None:
        self.start_pos_picker.hide()
        self.layout().addWidget(self.advanced_start_pos_picker)
        self.advanced_start_pos_picker.show()
        self.advanced_start_pos_picker.init_ui()

    def _show_option_picker(self) -> None:
        self.layout().addWidget(self.option_picker)
        self.option_picker.show()
        self.option_picker.scroll_area.sections_manager.show_all_sections()
        self.option_picker.update_option_picker()
        self.option_picker.resize_option_picker()

    def render_and_store_pictograph(
        self, pictograph_dict: dict, sequence
    ) -> Pictograph:
        pictograph_dict = self._add_turns_and_start_ori(pictograph_dict, sequence)
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
        self.main_widget.pictograph_cache[new_pictograph.letter][
            pictograph_key
        ] = new_pictograph
        if pictograph_key not in self.pictograph_cache[letter]:
            self.pictograph_cache[letter][pictograph_key] = new_pictograph
        section = scroll_area.sections_manager.get_section(letter_type)
        section.pictographs[pictograph_key] = new_pictograph
        scroll_area.pictograph_cache[pictograph_key] = new_pictograph
        return new_pictograph

    def _add_turns_and_start_ori(self, pictograph_dict, sequence):
        json_handler = self.main_widget.json_manager.current_sequence_json_handler
        self.current_end_red_ori = json_handler.get_red_end_ori(sequence)
        self.current_end_blue_ori = json_handler.get_blue_end_ori(sequence)

        pictograph_dict[RED_START_ORI] = self.current_end_red_ori
        pictograph_dict[BLUE_START_ORI] = self.current_end_blue_ori
        pictograph_dict[RED_TURNS] = 0
        pictograph_dict[BLUE_TURNS] = 0
        return pictograph_dict

    def reset_to_start_pos_picker(self) -> None:
        self.start_position_picked = False
        self.option_picker.hide()
        self.advanced_start_pos_picker.hide()
        self.layout().removeWidget(self.option_picker)
        self.layout().addWidget(self.start_pos_picker)
        self.start_pos_picker.show()

    def resize_sequence_builder(self) -> None:
        self.setMinimumWidth(int(self.builder_toolbar.width()))
        # self.setMinimumHeight(int(self.builder_toolbar.height()))
        # if the start pos picker is visible, resize it
        if self.start_pos_picker.isVisible():
            self.start_pos_picker.resize_start_pos_picker()
        elif self.advanced_start_pos_picker.isVisible():
            self.advanced_start_pos_picker.resize_advanced_start_pos_picker()
        elif self.option_picker.isVisible():
            self.option_picker.resize_option_picker()

    def get_last_added_pictograph(self, sequence):
        """Returns the last pictograph in the sequence. Assumes the sequence is not empty."""
        return sequence[-1]
