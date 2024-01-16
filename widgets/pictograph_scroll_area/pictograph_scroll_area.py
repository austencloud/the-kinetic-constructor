from typing import TYPE_CHECKING, Dict, List, Union
from PyQt6.QtWidgets import QScrollArea, QGridLayout, QWidget, QVBoxLayout, QFrame, QLabel
from PyQt6.QtCore import Qt, QTimer
from objects.pictograph.pictograph import Pictograph
from utilities.TypeChecking.TypeChecking import (
    Letters,
)
from widgets.ig_tab.ig_tab import IGTab
from widgets.option_picker_tab.option_picker_tab import OptionPickerTab
from .scroll_area_display_manager import ScrollAreaDisplayManager
from .scroll_area_filter_manager import ScrollAreaFilterFrameManager
from .scroll_area_pictograph_factory import ScrollAreaPictographFactory

if TYPE_CHECKING:
    from ..main_widget import MainWidget


class PictographScrollArea(QScrollArea):
    def __init__(self, main_widget: "MainWidget", parent_tab) -> None:
        super().__init__(parent_tab)
        self.main_widget = main_widget
        self.parent_tab: Union[
            "IGTab", "OptionPickerTab"
            ] = parent_tab
        self.letters: Dict[Letters, List[Dict[str, str]]] = self.main_widget.letters
        self.pictographs: Dict[Letters, Pictograph] = {}
        self.pictograph_factory = ScrollAreaPictographFactory(self)
        self.display_manager = ScrollAreaDisplayManager(self)
        self.filter_frame_manager = ScrollAreaFilterFrameManager(self)
        self.sections: Dict[Letters, QVBoxLayout] = {}
        self._setup_ui()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_arrow_placements)
        self.timer.start(1000)

    def _setup_ui(self) -> None:
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.layout:QVBoxLayout = QVBoxLayout(self.container)
        self.container.setContentsMargins(10, 10, 10, 10)
        self.setWidget(self.container)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def create_section(self, letter_type):
        section_layout = QVBoxLayout()
        section_label = QLabel(f"Type {letter_type} - Dual-Shifts")
        section_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        section_layout.addWidget(section_label)
        self.layout.addLayout(section_layout)
        self.sections[letter_type] = section_layout

    def add_pictograph_to_section(self, pictograph, letter_type):
        section_layout = self.sections.get(letter_type)
        if section_layout is not None:
            section_layout.addWidget(pictograph)

    def update_pictographs(self) -> None:
        deselected_letters = self.pictograph_factory.get_deselected_letters()
        for letter in deselected_letters:
            self.pictograph_factory.remove_deselected_letter_pictographs(letter)
        self.pictograph_factory.process_selected_letters()
        self.display_manager.order_and_display_pictographs()
        self.display_manager.cleanup_unused_pictographs()
        self.filter_frame_manager.update_filter_frame_if_needed()

        # Remove all previous sections
        while self.layout.count():
            widget_to_remove = self.layout.takeAt(0).widget()
            if widget_to_remove is not None:
                widget_to_remove.setParent(None)

        # Create and populate new sections based on the current selection
        for letter_type, pictographs in self.letters_by_type.items():
            self.create_section(letter_type)
            for pictograph_dict in pictographs:
                pictograph_widget = self.pictograph_factory.create_or_update_pictograph(pictograph_dict, letter_type)
                self.add_pictograph_to_section(pictograph_widget, letter_type)        

    def update_arrow_placements(self) -> None:
        for pictograph in self.pictographs.values():
            pictograph.arrow_placement_manager.update_arrow_placement()
