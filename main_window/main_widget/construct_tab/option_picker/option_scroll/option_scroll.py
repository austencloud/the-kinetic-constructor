from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.construct_tab.option_picker.option_scroll.section_widget.option_picker_section_widget import OptionPickerSectionWidget

from .option_scroll_layout_manager import OptionScrollLayoutManager
from Enums.Enums import LetterType

if TYPE_CHECKING:
    from ..option_picker import OptionPicker


class OptionScroll(QScrollArea):
    spacing = 3
    layout: QVBoxLayout
    container: QWidget
    sections: dict["LetterType", "OptionPickerSectionWidget"] = {}
    ordered_section_types: list["LetterType"] = []

    def __init__(self, option_picker: "OptionPicker") -> None:
        super().__init__(option_picker)
        self.option_picker = option_picker
        self.main_widget = option_picker.main_widget
        self.construct_tab = option_picker.construct_tab
        self.ori_calculator = self.main_widget.json_manager.ori_calculator
        self.json_manager = self.main_widget.json_manager
        self.json_loader = self.json_manager.loader_saver
        self.pictograph_cache: dict[str, BasePictograph] = {}

        self.layout_manager = OptionScrollLayoutManager(self)
