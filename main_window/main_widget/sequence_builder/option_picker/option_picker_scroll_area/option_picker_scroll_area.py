from typing import TYPE_CHECKING

from Enums.letters import LetterType
from data.constants import BLUE, RED

from base_widgets.base_picker_scroll_area import BasePickerScrollArea
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.sequence_widget.beat_frame.reversal_detector import (
    ReversalDetector,
)
from .option_picker_pictograph_factory import OptionPickerPictographFactory
from .option_picker_section_manager import OptionPickerSectionManager
from .option_picker_display_manager import OptionPickerDisplayManager


if TYPE_CHECKING:
    from main_window.main_widget.sequence_builder.option_picker.option_picker_scroll_area.option_picker_section_widget import (
        OptionPickerSectionWidget,
    )

    from ..option_picker import OptionPicker


class OptionPickerScrollArea(BasePickerScrollArea):
    MAX_COLUMN_COUNT: int = 8
    MIN_COLUMN_COUNT: int = 3
    spacing = 3
    COLUMN_COUNT = 8

    def __init__(self, option_picker: "OptionPicker") -> None:
        super().__init__(option_picker)
        self.option_picker: "OptionPicker" = option_picker
        self.manual_builder = option_picker.manual_builder
        self.option_manager = self.option_picker.option_getter

        self.ori_calculator = self.main_widget.json_manager.ori_calculator
        self.json_manager = self.main_widget.json_manager
        self.pictograph_cache: dict[str, BasePictograph] = {}
        self.stretch_index: int = -1
        self.disabled = False

        self.set_layout("VBox")  # Ensure correct layout
        self.section_manager = OptionPickerSectionManager(self)
        self.display_manager = OptionPickerDisplayManager(self)
        self.pictograph_factory = OptionPickerPictographFactory(
            self, self.manual_builder.pictograph_cache
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

    def hide_all_pictographs(self) -> None:
        for pictograph in self.pictograph_cache.values():
            pictograph.view.hide()

    def add_and_display_relevant_pictographs(self, next_options: list[dict]):
        # Clear current pictographs from layout
        self.display_manager.clear_all_section_layouts()

        for i, pictograph_dict in enumerate(next_options):
            # Get a pictograph from our pool
            if i >= len(self.option_picker.option_pool):
                break
            p = self.option_picker.option_pool[i]

            p.updater.update_pictograph(pictograph_dict)
            sequence_so_far = (
                self.json_manager.loader_saver.load_current_sequence_json()
            )
            reversal_info = ReversalDetector.detect_reversal(
                sequence_so_far, p.pictograph_dict
            )
            p.blue_reversal = reversal_info.get("blue_reversal", False)
            p.red_reversal = reversal_info.get("red_reversal", False)

            # Insert into layout
            self.display_manager.add_pictograph_to_section_layout(p)
            p.view.update_borders()
            p.updater.update_pictograph(pictograph_dict)
            p.elemental_glyph.update_elemental_glyph()
            p.view.show()

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

    def _hide_all_pictographs(self) -> None:
        for pictograph in self.pictograph_cache.values():
            pictograph.view.hide()

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
