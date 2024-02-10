from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication, QVBoxLayout
from PyQt6.QtCore import Qt
import pandas as pd
from data.rules import get_next_letters
from widgets.scroll_area.components.section_manager.section_widget.section_widget import (
    SectionWidget,
)
from widgets.scroll_area.components.option_picker_display_manager import OptionPickerDisplayManager
from ....pictograph.pictograph import Pictograph
from .option_picker_section_manager import (
    OptionPickerSectionsManager,
)
from ....scroll_area.base_scroll_area import BasePictographScrollArea

if TYPE_CHECKING:
    from .option_picker import OptionPicker


class OptionPickerScrollArea(BasePictographScrollArea):
    def __init__(self, option_picker: "OptionPicker"):
        super().__init__(option_picker)
        self.option_picker = option_picker
        self.sequence_builder = option_picker.sequence_builder
        self.clickable_option_handler = self.sequence_builder.clickable_option_handler
        self.letters = self.sequence_builder.letters
        self.pictographs = {}
        self.set_layout("VBox")
        self.sections_manager = OptionPickerSectionsManager(self)
        self.display_manager = OptionPickerDisplayManager(self)


    def initialize_with_options(self):
        """Initialize scroll area with options after a start pictograph is selected."""
        start_pictograph = self.option_picker.sequence_builder.current_pictograph
        end_pos, end_red_ori, end_blue_ori = (
            start_pictograph.end_pos,
            start_pictograph.red_motion.end_ori,
            start_pictograph.blue_motion.end_ori,
        )
        next_options = self.get_next_options(start_pictograph)

        for option_dict in next_options:
            self.sequence_builder.render_and_store_pictograph(option_dict)

    def get_next_options(self, pictograph: Pictograph) -> list[pd.Series]:
        """Fetch next options logic specific to sequence builder's needs."""
        matching_rows: pd.DataFrame = self.letters[
            self.letters["start_pos"] == pictograph.end_pos
        ]
        next_options = []
        for _, row in matching_rows.iterrows():
            pictograph_key = f"{row['letter']}_{row['start_pos']}→{row['end_pos']}"
            if pictograph_key not in self.option_picker.sequence_builder.main_widget.all_pictographs:
                next_options.append(row)
        return next_options

    def adjust_sections_size(self):
        """Adjust the size of sections, specific to sequence builder."""

        for section in self.sections_manager.sections.values():
            section.adjust_size()

    def resize_option_picker_scroll_area(self) -> None:
        self.setMinimumWidth(
            self.option_picker.sequence_builder.width()
            - self.option_picker.letter_button_frame.width()
        )
