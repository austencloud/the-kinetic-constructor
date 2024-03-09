from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QWheelEvent

from constants import BLUE, RED
from widgets.scroll_area.components.option_picker_pictograph_factory import (
    OptionPickerPictographFactory,
)
from widgets.sequence_builder.components.option_picker.option_picker_section_manager import (
    OptionPickerSectionsManager,
)

from ....scroll_area.components.option_picker_display_manager import (
    OptionPickerDisplayManager,
)
from ....pictograph.pictograph import Pictograph
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
        self.option_manager = self.option_picker.option_manager
        self.option_click_handler = self.sequence_builder.option_click_handler
        self.ori_calculator = (
            self.main_widget.json_manager.current_sequence_json_handler.ori_calculator
        )

        self.pictograph_cache: dict[str, Pictograph] = {}
        self.stretch_index: int = -1

        self.set_layout("VBox")
        self.sections_manager = OptionPickerSectionsManager(self)
        self.display_manager = OptionPickerDisplayManager(self)
        self.pictograph_factory = OptionPickerPictographFactory(
            self, self.sequence_builder.pictograph_cache
        )

    def fix_stretch(self):
        if self.stretch_index >= 0:
            item = self.layout.takeAt(self.stretch_index)
            del item
        self.layout.addStretch(1)
        self.stretch_index = self.layout.count()

    def _add_and_display_relevant_pictographs(self, next_options: list[dict]) -> None:
        QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        valid_next_options = []

        for pictograph_dict in next_options:
            valid_next_options.append(pictograph_dict)

        for pictograph_dict in valid_next_options:
            self.set_pictograph_orientations(pictograph_dict)
            pictograph = self._get_or_create_pictograph(pictograph_dict)
            pictograph.updater._update_from_pictograph_dict(pictograph_dict)
            self.display_manager.add_pictograph_to_section_layout(pictograph)
        self.display_manager.order_and_display_pictographs()
        QApplication.restoreOverrideCursor()

    def set_pictograph_orientations(self, pictograph_dict: dict) -> None:
        last_pictograph = self.sequence_builder.get_last_added_pictograph()
        pictograph_dict["red_start_ori"] = last_pictograph["red_end_ori"]
        pictograph_dict["blue_start_ori"] = last_pictograph["blue_end_ori"]
        pictograph_dict["red_end_ori"] = self.ori_calculator.calculate_end_orientation(
            pictograph_dict, RED
        )
        pictograph_dict["blue_end_ori"] = self.ori_calculator.calculate_end_orientation(
            pictograph_dict, BLUE
        )

    def _get_or_create_pictograph(self, pictograph_dict: dict) -> Pictograph:
        modified_key = self.sequence_builder.main_widget.pictograph_key_generator.generate_pictograph_key(
            pictograph_dict
        )
        if modified_key in self.pictograph_cache:
            return self.pictograph_cache[modified_key]
        else:
            pictograph = self.sequence_builder.render_and_store_pictograph(
                pictograph_dict
            )
            self.pictograph_cache[modified_key] = pictograph
            self.main_widget.all_pictographs[pictograph.letter][
                modified_key
            ] = pictograph
        return pictograph

    def _hide_all_pictographs(self):
        for pictograph in self.pictograph_cache.values():
            pictograph.view.hide()

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
            # ignore
            event.ignore()

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
