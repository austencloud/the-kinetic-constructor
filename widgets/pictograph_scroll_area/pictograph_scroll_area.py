from typing import TYPE_CHECKING, Dict, List
from PyQt6.QtWidgets import (
    QScrollArea,
    QWidget,
    QVBoxLayout,
    QLabel,
    QGraphicsView,
    QHBoxLayout,
    QGridLayout,
)
from PyQt6.QtCore import Qt, QTimer
from Enums import LetterNumberType
from utilities.TypeChecking.TypeChecking import Letters
from widgets.ig_tab.ig_scroll.ig_pictograph import IGPictograph
from .scroll_area_display_manager import ScrollAreaDisplayManager
from .scroll_area_filter_manager import ScrollAreaFilterFrameManager
from .scroll_area_pictograph_factory import ScrollAreaPictographFactory

if TYPE_CHECKING:
    from ..main_widget import MainWidget


class PictographScrollArea(QScrollArea):
    def __init__(self, main_widget: "MainWidget", parent_tab) -> None:
        super().__init__(parent_tab)
        self.main_widget = main_widget
        self.parent_tab = parent_tab
        self.letters = self.main_widget.letters
        self.pictographs: Dict[Letters, IGPictograph] = {}
        self.pictograph_factory = ScrollAreaPictographFactory(self)
        self.display_manager = ScrollAreaDisplayManager(self)
        self.filter_frame_manager = ScrollAreaFilterFrameManager(self)
        self.sections: Dict[str, QGridLayout] = {}
        self.letters_by_type: Dict[str, List[str]] = self.setup_letters_by_type()
        self._setup_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_arrow_placements)
        self.timer.start(1000)

    def setup_letters_by_type(self) -> Dict[str, List[str]]:
        letters_by_type = {}
        for letter_type in LetterNumberType:
            letters_by_type[letter_type.description] = letter_type.letters
        return letters_by_type

    def _setup_ui(self) -> None:
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.layout: QVBoxLayout = QVBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.container.setContentsMargins(10, 10, 10, 10)
        self.setWidget(self.container)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def get_pictograph_letter_type(self, pictograph_key: str) -> str:
        letter = pictograph_key.split("_")[0]
        for letter_type, letters in self.letters_by_type.items():
            if letter in letters:
                return letter_type
        return "Unknown"

    def organize_pictographs(self) -> None:
        # Clear previous sections before setting up new ones
        self.clear_sections()
        pictographs_by_type = {type: [] for type in self.letters_by_type.keys()}
        for key, pictograph in self.pictographs.items():
            letter_type = self.get_pictograph_letter_type(key)
            pictographs_by_type[letter_type].append(pictograph)

        # Create sections and add pictographs to them
        for letter_type, pictographs in pictographs_by_type.items():
            self.create_section(letter_type)
            for index, pictograph in enumerate(pictographs):
                self.display_manager.add_pictograph_to_layout(pictograph, index)

    def update_pictographs(self) -> None:
        deselected_letters = self.pictograph_factory.get_deselected_letters()
        for letter in deselected_letters:
            self.pictograph_factory.remove_deselected_letter_pictographs(letter)
        self.pictograph_factory.process_selected_letters()
        self.display_manager.cleanup_unused_pictographs()
        self.filter_frame_manager.update_filter_frame_if_needed()

        # Organize pictographs by their types after updates
        self.organize_pictographs()

    def organize_pictographs_by_type(self) -> Dict[str, List[IGPictograph]]:
        pictographs_by_type = {
            type_desc: [] for type_desc in LetterNumberType._member_names_
        }

        for key, ig_pictograph in self.pictographs.items():
            letter = key.split("_")[0]
            letter_type = ig_pictograph._get_letter_type(letter)
            if letter_type:
                pictographs_by_type[letter_type].append(ig_pictograph)

        return pictographs_by_type

    def clear_sections(self) -> None:
        """Clears all sections from the layout."""
        while self.layout.count():
            layout_item = self.layout.takeAt(0)
            if layout_item.widget():
                layout_item.widget().hide()
        self.sections.clear()

    def create_section(self, letter_type: str):
        """Creates a new section for a given letter type."""
        section_frame = QWidget()
        section_layout = QGridLayout(section_frame)
        section_label = QLabel(f"{letter_type} - Dual-Shifts")
        section_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        section_layout.addWidget(section_label)
        self.layout.addWidget(section_frame)
        self.sections[letter_type] = section_layout

    def add_pictograph_to_section(
        self, pictograph_view: QGraphicsView, letter_type: str
    ) -> None:
        """Adds a pictograph view to the section corresponding to its letter type."""
        section_layout = self.sections.get(letter_type)
        if section_layout:
            section_layout.addWidget(pictograph_view)

    def update_arrow_placements(self) -> None:
        for pictograph in self.pictographs.values():
            pictograph.arrow_placement_manager.update_arrow_placement()
