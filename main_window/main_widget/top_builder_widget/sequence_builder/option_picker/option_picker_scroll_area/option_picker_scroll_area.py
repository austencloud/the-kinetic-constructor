from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QWheelEvent

from Enums.letters import LetterType
from data.constants import BLUE, RED
from main_window.main_widget.top_builder_widget.sequence_builder.option_picker.option_picker_pictograph_factory import (
    OptionPickerPictographFactory,
)
from main_window.main_widget.top_builder_widget.sequence_builder.option_picker.option_picker_scroll_area.option_picker_section_manager import (
    OptionPickerSectionManager,
)
from base_widgets.base_picker_scroll_area import BasePickerScrollArea
from base_widgets.base_pictograph.base_pictograph import BasePictograph


from .option_picker_display_manager import (
    OptionPickerDisplayManager,
)


if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_builder.sequence_builder import (
        SequenceBuilder,
    )
    from ..option_picker import OptionPicker


class OptionPickerScrollArea(BasePickerScrollArea):
    MAX_COLUMN_COUNT: int = 8
    MIN_COLUMN_COUNT: int = 3

    def __init__(self, option_picker: "OptionPicker") -> None:
        super().__init__(option_picker)
        self.option_picker: "OptionPicker" = option_picker
        self.sequence_builder: "SequenceBuilder" = option_picker.sequence_builder
        self.option_manager = self.option_picker.option_getter
        self.option_click_handler = self.sequence_builder.option_click_handler
        self.ori_calculator = self.main_widget.json_manager.ori_calculator
        self.json_manager = self.main_widget.json_manager
        self.pictograph_cache: dict[str, BasePictograph] = {}
        self.stretch_index: int = -1
        self.disabled = False

        self.set_layout("VBox")  # Ensure correct layout
        self.section_manager = OptionPickerSectionManager(self)
        self.display_manager = OptionPickerDisplayManager(self)
        self.pictograph_factory = OptionPickerPictographFactory(
            self, self.sequence_builder.pictograph_cache
        )
        self.setStyleSheet("background-color: transparent; border: none;")
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def fix_stretch(self) -> None:
        if self.stretch_index >= 0:
            item = self.layout.takeAt(self.stretch_index)
            del item
        self.layout.addStretch(1)
        self.stretch_index = self.layout.count()

    def remove_irrelevant_pictographs(self) -> None:
        for pictograph in self.pictograph_cache.values():
            pictograph.view.hide()

    def add_and_display_relevant_pictographs(self, next_options: list[dict]) -> None:
        if self.disabled:
            return
        if QApplication.overrideCursor() is None:
            QApplication.setOverrideCursor(Qt.CursorShape.WaitCursor)
        valid_next_options = []

        sequence = self.json_manager.loader_saver.load_current_sequence_json()
        for pictograph_dict in next_options:
            valid_next_options.append(pictograph_dict)

        for pictograph_dict in valid_next_options:
            self.set_pictograph_orientations(pictograph_dict, sequence)
            pictograph = self._get_or_create_pictograph(pictograph_dict, sequence)
            pictograph.updater.update_pictograph(pictograph_dict)

        self.display_manager.order_and_display_pictographs()
        self.layout.update()
        QApplication.restoreOverrideCursor()

    def set_pictograph_orientations(self, pictograph_dict: dict, sequence) -> None:
        last_pictograph = sequence[-1]
        pictograph_dict["red_attributes"]["start_ori"] = last_pictograph[
            "red_attributes"
        ]["end_ori"]
        pictograph_dict["blue_attributes"]["start_ori"] = last_pictograph[
            "blue_attributes"
        ]["end_ori"]
        pictograph_dict["red_attributes"]["end_ori"] = (
            self.ori_calculator.calculate_end_orientation(pictograph_dict, RED)
        )
        pictograph_dict["red_attributes"]["blue_ori"] = (
            self.ori_calculator.calculate_end_orientation(pictograph_dict, BLUE)
        )

    def _get_or_create_pictograph(
        self, pictograph_dict: dict, sequence
    ) -> BasePictograph:
        modified_key = self.sequence_builder.main_widget.pictograph_key_generator.generate_pictograph_key(
            pictograph_dict
        )
        if modified_key in self.pictograph_cache:
            return self.pictograph_cache[modified_key]
        else:
            pictograph = self.sequence_builder.render_and_store_pictograph(
                pictograph_dict, sequence
            )
            self.pictograph_cache[modified_key] = pictograph
            self.main_widget.pictograph_cache[pictograph.letter][
                modified_key
            ] = pictograph
        return pictograph

    def _hide_all_pictographs(self) -> None:
        for pictograph in self.pictograph_cache.values():
            pictograph.view.hide()

    def resize_option_picker_scroll_area(self) -> None:
        for section in self.section_manager.sections.values():
            section.resize_option_picker_section_widget()

    def wheelEvent(self, event: QWheelEvent) -> None:
        if self.disabled:
            return
        modifiers = QApplication.keyboardModifiers()
        if modifiers == Qt.KeyboardModifier.ControlModifier:
            delta = event.angleDelta().y()
            if delta > 0:
                self.change_pictograph_size(increase=True)
            elif delta < 0:
                self.change_pictograph_size(increase=False)
            event.accept()
        else:
            event.ignore()

    def change_pictograph_size(self, increase: bool) -> None:
        if self.disabled:
            return
        MAX_COLUMN_COUNT = 8
        MIN_COLUMN_COUNT = 3
        current_size = self.display_manager.COLUMN_COUNT

        if increase and current_size > MIN_COLUMN_COUNT:
            self.display_manager.COLUMN_COUNT -= 1
        elif not increase and current_size < MAX_COLUMN_COUNT:
            self.display_manager.COLUMN_COUNT += 1
        # self.display_manager.order_and_display_pictographs()

    def set_disabled(self, disabled: bool) -> None:
        self.disabled = disabled
        for section in self.section_manager.sections.values():
            for pictograph in section.pictographs.values():
                pictograph.view.set_enabled(not disabled)

    def add_section_to_layout(self, section: QWidget, section_index: int = None):
        if section_index == 0 or section_index:  # widget is a section
            if section.__class__.__name__ == "OptionPickerSectionWidget":
                if section.letter_type == LetterType.Type1:
                    self.layout.insertWidget(section_index, section, 6)
                else:
                    self.layout.insertWidget(section_index, section, 4)
            elif section.__class__.__name__ == "OptionPickerSectionGroupWidget":
                self.layout.insertWidget(section_index, section, 4)
