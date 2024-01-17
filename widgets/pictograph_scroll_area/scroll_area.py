from typing import TYPE_CHECKING, Dict, List, Union
from PyQt6.QtWidgets import (
    QScrollArea,
    QWidget,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt, QTimer
from utilities.TypeChecking.TypeChecking import LetterTypeNums, Letters
from widgets.filter_frame.filter_tab.filter_tab import FilterTab
from widgets.ig_tab.ig_scroll.ig_pictograph import IGPictograph
from widgets.pictograph_scroll_area.scroll_area_section_manager import (
    ScrollAreaSectionManager,
)
from .scroll_area_display_manager import ScrollAreaDisplayManager
from .scroll_area_filter_manager import ScrollAreaFilterTabManager
from .scroll_area_pictograph_factory import ScrollAreaPictographFactory

if TYPE_CHECKING:
    from widgets.ig_tab.ig_tab import IGTab
    from widgets.option_picker_tab.option_picker_tab import OptionPickerTab
    from ..main_widget import MainWidget


class ScrollArea(QScrollArea):
    def __init__(
        self, main_widget: "MainWidget", parent_tab: Union["IGTab", "OptionPickerTab"]
    ) -> None:
        super().__init__(parent_tab)
        self.main_widget = main_widget
        self.parent_tab = parent_tab
        self.letters = self.main_widget.letters
        self.pictographs: Dict[Letters, IGPictograph] = {}
        self.pictograph_factory = ScrollAreaPictographFactory(self)
        self.display_manager = ScrollAreaDisplayManager(self)
        self.filter_frame_manager = ScrollAreaFilterTabManager(self)
        self.section_manager = ScrollAreaSectionManager(self)
        self.letters_by_type: Dict[
            LetterTypeNums, List[Letters]
        ] = self.section_manager.setup_letters_by_type()
        self._setup_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_arrow_placements)
        self.timer.start(1000)
        self.pictographs_by_type = {type: [] for type in self.letters_by_type.keys()}
        for letter_type, pictographs in self.pictographs_by_type.items():
            filter_tab = FilterTab(self, letter_type)
            self.section_manager.create_section(letter_type, filter_tab)

    def _setup_ui(self) -> None:
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.layout: QVBoxLayout = QVBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.container.setStyleSheet("background-color: #f2f2f2;")
        self.setWidget(self.container)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def organize_pictographs_by_type(self) -> None:
        # self.section_manager.clear_sections()
        for key, pictograph in self.pictographs.items():
            letter_type = self.section_manager.get_pictograph_letter_type(key)
            self.pictographs_by_type[letter_type].append(pictograph)

        for letter_type, pictographs in self.pictographs_by_type.items():
            for index, pictograph in enumerate(pictographs):
                self.display_manager.add_pictograph_to_layout(pictograph, index)

    def update_pictographs(self) -> None:
        deselected_letters = self.pictograph_factory.get_deselected_letters()
        for letter in deselected_letters:
            self.pictograph_factory.remove_deselected_letter_pictographs(letter)
        self.pictograph_factory.process_selected_letters()
        self.display_manager.cleanup_unused_pictographs()
        self.organize_pictographs_by_type()

    def update_arrow_placements(self) -> None:
        for pictograph in self.pictographs.values():
            pictograph.arrow_placement_manager.update_arrow_placement()

    def resize_scroll_area(self) -> None:
        for section in self.section_manager.sections.values():
            section.resize_scroll_area_section()