from PyQt6.QtWidgets import QFrame, QHBoxLayout, QApplication
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from Enums import LetterType
from utilities.TypeChecking.letter_lists import all_letters
import pandas as pd
from constants import BLUE_START_ORI, BLUE_TURNS, RED_START_ORI, RED_TURNS
from utilities.TypeChecking.TypeChecking import Letters
from widgets.pictograph.components.add_to_sequence_manager import (
    AddToSequenceManager,
)
from .components.start_position_picker.start_position_picker import StartPosPicker
from ..pictograph.pictograph import Pictograph
from .components.option_picker.option_picker_click_handler import (
    OptionPickerClickHandler,
)
from .components.option_picker.option_picker import OptionPicker

if TYPE_CHECKING:
    from ..main_widget.main_widget import MainWidget


class SequenceBuilder(QFrame):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.current_pictograph: Pictograph = None
        self.letters_df = pd.read_csv("PictographDataframe.csv")  # Load the dataframe
        self.selected_letters = None
        self.start_position_picked = False
        self._setup_components()
        self.pictograph_cache: dict[Letters, dict[str, Pictograph]] = {
            letter: {} for letter in all_letters
        }
        self.start_position_picker = StartPosPicker(self)
        self.option_picker = OptionPicker(self)
        self.add_to_sequence_manager = AddToSequenceManager(self)
        self.setLayout(QHBoxLayout())
        self.layout().addWidget(self.start_position_picker)

    def update_current_pictograph(self, pictograph: Pictograph):
        self.current_pictograph = pictograph
        self.current_end_red_ori = pictograph.red_motion.end_ori
        self.current_end_blue_ori = pictograph.blue_motion.end_ori
        self.render_next_options(pictograph.end_pos)

    def render_next_options(self, end_pos):
        """Fetches and renders next options based on the end position."""
        pictograph_dfs: pd.DataFrame = self.letters_df[
            self.letters_df["start_pos"] == end_pos
        ]
        for _, pictograph_df in pictograph_dfs.iterrows():
            pictograph_key = f"{pictograph_df['letter']}_{pictograph_df['start_pos']}→{pictograph_df['end_pos']}"
            if pictograph_key not in self.pictograph_cache[pictograph_df["letter"]]:
                self.render_and_store_pictograph(pictograph_df)

    def _setup_components(self):
        self.clickable_option_handler = OptionPickerClickHandler(self)

    def transition_to_sequence_building(self, start_pictograph: Pictograph):
        self.start_position_picked = True
        self.start_position_picker.hide()
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        self.update_current_pictograph(start_pictograph)
        self.layout().removeWidget(self.start_position_picker)
        self.layout().addWidget(self.option_picker)

        self.option_picker.show()
        self.option_picker.scroll_area.resize_option_picker_scroll_area()
        self.option_picker.scroll_area.sections_manager.show_all_sections()
        self.option_picker.scroll_area.update_pictographs()
        self.option_picker.scroll_area.display_manager.order_and_display_pictographs()
        QApplication.restoreOverrideCursor()

    def render_and_store_pictograph(self, pictograph_df: pd.Series):
        pictograph_dict = pictograph_df.to_dict()
        pictograph_dict = self._add_turns_and_start_ori(pictograph_dict)
        pictograph_key = self.generate_pictograph_key(pictograph_dict)

        if pictograph_key in self.option_picker.scroll_area.pictographs:
            return self.option_picker.scroll_area.pictographs[pictograph_key]

        new_pictograph = (
            self.option_picker.scroll_area.pictograph_factory.get_or_create_pictograph(
                pictograph_key, pictograph_dict
            )
        )
        self.option_picker.scroll_area.pictographs[pictograph_key] = new_pictograph
        if pictograph_key not in self.pictograph_cache[pictograph_dict["letter"]]:
            self.pictograph_cache[pictograph_dict["letter"]][
                pictograph_key
            ] = new_pictograph
        section = self.option_picker.scroll_area.sections_manager.get_section(
            LetterType.get_letter_type(pictograph_dict["letter"])
        )
        section.pictographs[pictograph_key] = new_pictograph
        self.option_picker.scroll_area.pictographs[pictograph_key] = new_pictograph
        return new_pictograph

    def _add_turns_and_start_ori(self, pictograph_dict):
        pictograph_dict[RED_START_ORI] = self.current_end_red_ori
        pictograph_dict[BLUE_START_ORI] = self.current_end_blue_ori
        pictograph_dict[RED_TURNS] = 0
        pictograph_dict[BLUE_TURNS] = 0
        return pictograph_dict

    def generate_pictograph_key(self, pictograph_dict):
        return (
            f"{pictograph_dict['letter']}_{pictograph_dict['start_pos']}→{pictograph_dict['end_pos']}"
            f"_red_{pictograph_dict['red_motion_type']}_{pictograph_dict['red_start_loc']}→{pictograph_dict['red_end_loc']}"
            f"_blue_{pictograph_dict['blue_motion_type']}_{pictograph_dict['blue_start_loc']}→{pictograph_dict['blue_end_loc']}"
        )

    def resize_sequence_builder(self) -> None:
        self.setMinimumWidth(int(self.main_widget.width() * 3 / 5))
        self.start_position_picker.resize_start_position_picker()
        self.option_picker.scroll_area.resize_option_picker_scroll_area()
