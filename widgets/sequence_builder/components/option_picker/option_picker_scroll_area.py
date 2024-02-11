from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QWheelEvent
import pandas as pd
from widgets.scroll_area.components.scroll_area_pictograph_factory import (
    ScrollAreaPictographFactory,
)
from ....scroll_area.components.option_picker_display_manager import (
    OptionPickerDisplayManager,
)
from ....pictograph.pictograph import Pictograph
from .option_picker_section_manager import OptionPickerSectionsManager
from ....scroll_area.base_scroll_area import BasePictographScrollArea

if TYPE_CHECKING:
    from .option_picker import OptionPicker
    from widgets.sequence_builder.sequence_builder import SequenceBuilder


class OptionPickerScrollArea(BasePictographScrollArea):
    MAX_COLUMN_COUNT: int = 8
    MIN_COLUMN_COUNT: int = 3

    def __init__(self, option_picker: "OptionPicker"):
        super().__init__(option_picker)
        self.option_picker: "OptionPicker" = option_picker
        self.sequence_builder: "SequenceBuilder" = option_picker.sequence_builder
        self.clickable_option_handler = self.sequence_builder.clickable_option_handler
        self.letters: pd.DataFrame = self.sequence_builder.letters_df
        self.pictographs: dict[str, Pictograph] = {}
        self.stretch_index: int = -1

        self.set_layout("VBox")
        self.sections_manager = OptionPickerSectionsManager(self)
        self.display_manager = OptionPickerDisplayManager(self)
        self.pictograph_factory = ScrollAreaPictographFactory(
            self, self.sequence_builder.pictograph_cache
        )

    def fix_stretch(self):
        if self.stretch_index >= 0:
            item = self.layout.takeAt(self.stretch_index)
            del item
        self.layout.addStretch(1)
        self.stretch_index = self.layout.count()

    def update_pictographs(self):
        current_pictograph = self.option_picker.sequence_builder.current_pictograph
        next_options = self.get_next_options(current_pictograph)
        self._hide_all_pictographs()
        self._add_and_display_relevant_pictographs(next_options)

    def _add_and_display_relevant_pictographs(self, next_options: list[pd.Series]):
        for option_dict in next_options:
            pictograph_key = self.sequence_builder.generate_pictograph_key(option_dict)
            pictograph = self._get_or_create_pictograph(pictograph_key, option_dict)
            self.display_manager.add_pictograph_to_section_layout(pictograph)
        self.display_manager.order_and_display_pictographs()

    def _get_or_create_pictograph(
        self, pictograph_key: str, option_dict: pd.Series
    ) -> Pictograph:
        pictograph = self.pictographs.get(pictograph_key)
        if not pictograph:
            pictograph = self.sequence_builder.render_and_store_pictograph(option_dict)
            self.pictographs[pictograph_key] = pictograph
        return pictograph

    def get_next_options(self, pictograph: Pictograph) -> list[pd.Series]:
        return [
            row
            for _, row in self.letters[
                self.letters["start_pos"] == pictograph.end_pos
            ].iterrows()
            if f"{row['letter']}_{row['start_pos']}→{row['end_pos']}"
            not in self.option_picker.sequence_builder.pictograph_cache
        ]

    def _hide_all_pictographs(self):
        for pictograph in self.pictographs.values():
            pictograph.view.hide()

    def get_next_options(self, pictograph: Pictograph) -> list[pd.Series]:
        """Fetch next options logic specific to sequence builder's needs."""
        matching_rows: pd.DataFrame = self.letters[
            self.letters["start_pos"] == pictograph.end_pos
        ]
        next_options = []
        for _, row in matching_rows.iterrows():
            pictograph_key = f"{row['letter']}_{row['start_pos']}→{row['end_pos']}"
            if (
                pictograph_key
                not in self.option_picker.sequence_builder.pictograph_cache
            ):
                next_options.append(row)
        return next_options

    def adjust_sections_size(self):
        """Adjust the size of sections, specific to sequence builder."""
        for section in self.sections_manager.sections.values():
            section.adjust_size()

    def resize_option_picker_scroll_area(self) -> None:
        self.setMinimumWidth(self.option_picker.sequence_builder.width())

    def wheelEvent(self, event: QWheelEvent) -> None:
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.change_pictograph_size(increase=True)
            elif delta < 0:
                self.change_pictograph_size(increase=False)
            event.accept()
        else:
            super().wheelEvent(event)

    def change_pictograph_size(self, increase: bool) -> None:
        MAX_COLUMN_COUNT = 8
        MIN_COLUMN_COUNT = 3
        current_size = self.display_manager.COLUMN_COUNT

        if increase and current_size > MIN_COLUMN_COUNT:
            self.display_manager.COLUMN_COUNT -= 1
        elif not increase and current_size < MAX_COLUMN_COUNT:
            self.display_manager.COLUMN_COUNT += 1
        self.display_manager.order_and_display_pictographs()

    def clear_layout(self):
        """Clears all widgets from the layout."""
        while self.layout.count():
            item = self.layout.takeAt(0)
            if item.widget():
                item.widget().hide()
