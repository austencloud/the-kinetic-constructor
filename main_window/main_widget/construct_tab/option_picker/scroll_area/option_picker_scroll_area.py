from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt6.QtCore import Qt

from Enums.letters import LetterType
from data.constants import BLUE, RED

from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.sequence_widget.beat_frame.reversal_detector import (
    ReversalDetector,
)
from .section_manager.option_picker_section_manager import OptionPickerSectionManager
from .option_picker_display_manager import OptionPickerDisplayManager


if TYPE_CHECKING:
    from .section_manager.option_picker_section_widget import OptionPickerSectionWidget

    from ..option_picker import OptionPicker


class OptionPickerScrollArea(QScrollArea):
    MAX_COLUMN_COUNT: int = 8
    MIN_COLUMN_COUNT: int = 3
    spacing = 3
    COLUMN_COUNT = 8

    def __init__(self, option_picker: "OptionPicker") -> None:
        super().__init__(option_picker)
        self.option_picker: "OptionPicker" = option_picker
        self.construct_tab = option_picker.construct_tab
        self.option_manager = self.option_picker.option_getter
        self.setContentsMargins(0, 0, 0, 0)
        self.container = QWidget()
        self.container.setAutoFillBackground(True)
        self.container.setStyleSheet("background: transparent;")
        self.container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        self.main_widget = option_picker.main_widget
        self.layout: Union[QVBoxLayout, QHBoxLayout] = None
        self.setWidgetResizable(True)
        self.setup_ui()

        self.ori_calculator = self.main_widget.json_manager.ori_calculator
        self.json_manager = self.main_widget.json_manager
        self.pictograph_cache: dict[str, BasePictograph] = {}
        self.stretch_index: int = -1
        self.disabled = False
        self.viewport().setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: transparent; border: none;")

        self.set_layout("VBox")  # Ensure correct layout
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.section_manager = OptionPickerSectionManager(self)
        self.display_manager = OptionPickerDisplayManager(self)

    def setup_ui(self):
        self.setWidget(self.container)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def set_layout(self, layout_type: str):
        if layout_type == "VBox":
            new_layout = QVBoxLayout()
        elif layout_type == "HBox":
            new_layout = QHBoxLayout()
        else:
            raise ValueError("Invalid layout type specified.")

        self.layout = new_layout
        self.container.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

    def fix_stretch(self) -> None:
        if self.stretch_index >= 0:
            item = self.layout.takeAt(self.stretch_index)
            del item
        self.layout.addStretch(1)
        self.stretch_index = self.layout.count()

    def hide_all_pictographs(self) -> None:
        for pictograph in self.pictograph_cache.values():
            pictograph.view.hide()

    def add_and_display_relevant_pictographs(self, next_options: list[dict]):
        for section in self.section_manager.sections.values():
            section.clear_pictographs()
        for i, pictograph_dict in enumerate(next_options):
            if i >= len(self.option_picker.option_pool):
                break
            pictograph = self.option_picker.option_pool[i]
            pictograph.updater.update_pictograph(pictograph_dict)
            sequence_so_far = (
                self.json_manager.loader_saver.load_current_sequence_json()
            )
            reversal_info = ReversalDetector.detect_reversal(
                sequence_so_far, pictograph.pictograph_dict
            )
            pictograph.blue_reversal = reversal_info.get("blue_reversal", False)
            pictograph.red_reversal = reversal_info.get("red_reversal", False)

            self.display_manager.add_pictograph_to_section_layout(pictograph)
            pictograph.view.update_borders()
            pictograph.elemental_glyph.update_elemental_glyph()
            pictograph.view.show()

    def set_pictograph_orientations(self, pictograph_dict: dict, sequence) -> None:
        last_pictograph_dict = (
            sequence[-1]
            if sequence[-1].get("is_placeholder", "") != True
            else sequence[-2]
        )
        pictograph_dict["red_attributes"]["start_ori"] = last_pictograph_dict[
            "red_attributes"
        ]["end_ori"]
        pictograph_dict["blue_attributes"]["start_ori"] = last_pictograph_dict[
            "blue_attributes"
        ]["end_ori"]
        pictograph_dict["red_attributes"]["end_ori"] = (
            self.ori_calculator.calculate_end_orientation(pictograph_dict, RED)
        )
        pictograph_dict["red_attributes"]["blue_ori"] = (
            self.ori_calculator.calculate_end_orientation(pictograph_dict, BLUE)
        )

    def set_disabled(self, disabled: bool) -> None:
        self.disabled = disabled
        for section in self.section_manager.sections.values():
            for pictograph in section.pictographs.values():
                pictograph.view.set_enabled(not disabled)

    def add_section_to_layout(
        self, section: "OptionPickerSectionWidget", section_index: int = None
    ):
        if section_index == 0 or section_index:
            if section.__class__.__name__ == "OptionPickerSectionWidget":
                if section.letter_type == LetterType.Type1:
                    self.layout.insertWidget(section_index, section, 4)
                else:
                    self.layout.insertWidget(section_index, section, 4)
            elif section.__class__.__name__ == "OptionPickerSectionGroupWidget":
                self.layout.insertWidget(section_index, section, 4)

    def clear_pictographs(self) -> None:
        self.display_manager.clear_all_section_layouts()
        self.pictograph_cache.clear()

