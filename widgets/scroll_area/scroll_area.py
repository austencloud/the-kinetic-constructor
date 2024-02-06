from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QTimer


from .components.scroll_area_pictograph_factory import ScrollAreaPictographFactory
from .components.section_manager.section_manager import ScrollAreaSectionManager
from .components.scroll_area_display_manager import ScrollAreaDisplayManager
from utilities.TypeChecking.TypeChecking import LetterTypes, Letters
from ..pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from ..codex.codex import Codex


class CodexScrollArea(QScrollArea):
    def __init__(self, codex: "Codex") -> None:
        super().__init__(codex)
        self.main_widget = codex.main_widget
        self.codex = codex
        self.letters = self.main_widget.letters
        self.pictographs: dict[Letters, Pictograph] = {}
        self.stretch_index = -1  # Initialize stretch index
        self._setup_ui()
        self._setup_managers()

    def _setup_managers(self) -> None:
        self.display_manager = ScrollAreaDisplayManager(self)
        self.sections_manager = ScrollAreaSectionManager(self)
        self.pictograph_factory = ScrollAreaPictographFactory(self)

    def _setup_ui(self) -> None:
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.layout: QVBoxLayout = QVBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.container.setStyleSheet("background-color: #f2f2f2;")
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setWidget(self.container)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def fix_stretch(self):
        if self.stretch_index >= 0:
            item = self.layout.takeAt(self.stretch_index)
            del item
        self.layout.addStretch(1)
        self.stretch_index = self.layout.count()

    def insert_widget_at_index(self, widget: QWidget, index: int) -> None:
        self.layout.insertWidget(index, widget)

    def update_pictographs(self, letter_type: LetterTypes = None) -> None:
        deselected_letters = self.pictograph_factory.get_deselected_letters()
        selected_letters = set(self.codex.selected_letters)

        if self._only_deselection_occurred(deselected_letters, selected_letters):
            for letter in deselected_letters:
                self.pictograph_factory.remove_deselected_letter_pictographs(letter)
        else:
            for letter in deselected_letters:
                self.pictograph_factory.remove_deselected_letter_pictographs(letter)
            self.pictograph_factory.process_selected_letters()
        if letter_type:
            self.display_manager.order_and_display_pictographs(letter_type)

    def _only_deselection_occurred(self, deselected_letters, selected_letters) -> bool:
        if not deselected_letters:
            return False
        if not selected_letters:
            return True

        current_pictograph_letters = {key.split("_")[0] for key in self.pictographs}

        return (
            len(deselected_letters) > 0
            and len(selected_letters) == len(current_pictograph_letters) - 1
        )

    def update_arrow_placements(self) -> None:
        for pictograph in self.pictographs.values():
            pictograph.arrow_placement_manager.update_arrow_placements()
