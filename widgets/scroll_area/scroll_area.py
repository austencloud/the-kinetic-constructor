from typing import TYPE_CHECKING, Dict
from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt


from .scroll_area_pictograph_factory import ScrollAreaPictographFactory
from .scroll_area_section_manager import ScrollAreaSectionManager
from .scroll_area_display_manager import ScrollAreaDisplayManager
from utilities.TypeChecking.TypeChecking import Letters
from ..pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from ..codex.codex import Codex


class ScrollAreaUpdater:
    def __init__(self, scroll_area: "ScrollArea") -> None:
        self.scroll_area = scroll_area

    def update_pictographs(self) -> None:
        deselected_letters = self.scroll_area.pictograph_factory.get_deselected_letters()
        selected_letters = set(self.scroll_area.codex.selected_letters)

        if self._only_deselection_occurred(deselected_letters, selected_letters):
            for letter in deselected_letters:
                self.scroll_area.pictograph_factory.remove_deselected_letter_pictographs(letter)
        else:
            for letter in deselected_letters:
                self.scroll_area.pictograph_factory.remove_deselected_letter_pictographs(letter)
            self.scroll_area.pictograph_factory.process_selected_letters()
        self.scroll_area.display_manager.order_and_display_pictographs()

    def _only_deselection_occurred(self, deselected_letters, selected_letters) -> bool:
        if not deselected_letters:
            return False
        if not selected_letters:
            return True

        current_pictograph_letters = {key.split("_")[0] for key in self.scroll_area.pictographs}

        return (
            len(deselected_letters) > 0
            and len(selected_letters) == len(current_pictograph_letters) - 1
        )




class ScrollArea(QScrollArea):
    def __init__(self, codex: "Codex") -> None:
        super().__init__(codex)
        self.main_widget = codex.main_tab_widget.main_widget
        self.codex = codex
        self.letters = self.main_widget.letters
        self.pictographs: Dict[Letters, Pictograph] = {}
        self._setup_ui()
        self._setup_managers()
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addStretch(1)
        self.updater = ScrollAreaUpdater(self)

    def _setup_managers(self) -> None:
        self.display_manager = ScrollAreaDisplayManager(self)
        self.section_manager = ScrollAreaSectionManager(self)
        self.pictograph_factory = ScrollAreaPictographFactory(self)

    def _setup_ui(self) -> None:
        self.setWidgetResizable(True)
        self.container = QWidget()
        self.layout: QVBoxLayout = QVBoxLayout(self.container)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.container.setStyleSheet("background-color: #f2f2f2;")
        self.setWidget(self.container)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

