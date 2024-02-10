from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from data.rules import get_next_letters
from widgets.scroll_area.components.scroll_area_display_manager import (
    ScrollAreaDisplayManager,
)
from widgets.sequence_builder.components.option_picker.option_picker_section_manager import (
    OptionPickerSectionsManager,
)

from ....pictograph.pictograph import Pictograph
from widgets.scroll_area.base_scroll_area import BasePictographScrollArea

if TYPE_CHECKING:
    from widgets.sequence_builder.components.start_position_picker.start_position_picker import (
        StartPosPicker,
    )


class StartPosPickerScrollArea(BasePictographScrollArea):
    def __init__(self, start_pos_picker: "StartPosPicker"):
        super().__init__(start_pos_picker)
        self.start_pos_picker = start_pos_picker
        self.sequence_builder = start_pos_picker.sequence_builder
        self.clickable_option_handler = self.sequence_builder.clickable_option_handler
        self.display_manager = self.sequence_builder.display_manager
        self.letters = self.sequence_builder.main_widget.letters
        self.pictographs = {}
        self.set_layout("HBox")
        self.sections_manager = OptionPickerSectionsManager(self)
        self.COLUMN_COUNT = 5

    def _update_pictographs(self, clicked_option: "Pictograph"):
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        current_letter = clicked_option.letter
        next_possible_letters = get_next_letters(current_letter)
        specific_end_pos = clicked_option.end_pos

        filtered_data = self.filter_next_options(
            next_possible_letters, specific_end_pos
        )
        self.clear_layout()
        for motion_dict in filtered_data:
            self.add_pictograph(motion_dict)
        QApplication.restoreOverrideCursor()

    def filter_next_options(
        letters_data: dict[str, list[dict]],
        next_possible_letters: list[str],
        specific_end_pos: str,
    ) -> list[dict]:
        return [
            motion_dict
            for letter, motion_dicts in letters_data.items()
            if letter in next_possible_letters
            for motion_dict in motion_dicts
            if motion_dict["end_pos"] == specific_end_pos
        ]

    def add_pictograph(self, motion_dict):
        """Create and add pictograph widget to layout based on motion_dict."""
        pictograph_key = f"{motion_dict['letter']}_{motion_dict['start_pos']}→{motion_dict['end_pos']}"
        if pictograph_key not in self.pictographs:
            pictograph: Pictograph = (
                self.start_pos_picker.pictograph_factory.create_pictograph(motion_dict)
            )
            self.pictographs[pictograph_key] = pictograph
            pictograph.view.mousePressEvent = (
                self.clickable_option_handler.get_click_handler(pictograph)
            )
            self.add_widget_to_layout(pictograph.view)

    def initialize_with_options(self):
        """Initialize scroll area with options after a start pictograph is selected."""
        self.replace_layout_with_vbox()
        start_pictograph = self.start_pos_picker.sequence_builder.current_pictograph
        end_pos, end_red_ori, end_blue_ori = (
            start_pictograph.end_pos,
            start_pictograph.red_motion.end_ori,
            start_pictograph.blue_motion.end_ori,
        )
        next_options = self.get_next_options(end_pos, end_red_ori, end_blue_ori)

        for option_data in next_options:
            self.add_pictograph(option_data)

    def replace_layout_with_vbox(self):
        new_layout = QVBoxLayout()
        new_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        new_layout.setContentsMargins(0, 0, 0, 0)

        old_layout = self.container.layout()
        while old_layout and old_layout.count():
            item = old_layout.takeAt(0)
            if item.widget():
                new_layout.addWidget(item.widget())

        self.container.setLayout(new_layout)
        self.container_layout = new_layout

    def get_next_options(self, end_pos, end_red_ori, end_blue_ori):
        """Fetch next options logic specific to sequence builder's needs."""
        return []

    def adjust_sections_size(self):
        """Adjust the size of sections, specific to sequence builder."""
        for section in self.sections_manager.sections.values():
            section.adjust_size()

    def _add_option_to_layout(self, option: Pictograph, is_start_pos: bool) -> None:
        option.view.mousePressEvent = self.clickable_option_handler.get_click_handler(
            option, is_start_pos
        )
        self.container_layout.addWidget(option.view)

    def resize_start_pos_picker_scroll_area(self) -> None:
        self.setMinimumHeight(self.start_pos_picker.height())
        self.setMinimumWidth(self.start_pos_picker.width())

    def replace_hbox_with_vbox(self):
        self.container_layout.removeItem(self.container_layout)
        self.set_layout("VBox")
