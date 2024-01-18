from typing import TYPE_CHECKING, Dict, List
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
)
from utilities.TypeChecking.letter_lists import all_letters
from PyQt6.QtGui import QResizeEvent
from constants import (
    DIAMOND,
    STAFF,
)
from utilities.TypeChecking.TypeChecking import Letters
from widgets.image_cache_manager import ImageCacheManager
from widgets.main_tab_widget import MainTabWidget
from widgets.main_widget_layout_manager import MainWidgetLayoutManager
from widgets.main_widget_letter_loader import MainLetterLoader
from objects.pictograph.pictograph import Pictograph
from .sequence_widget.sequence_widget import MainSequenceWidget

if TYPE_CHECKING:
    from main import MainWindow


class MainWidget(QWidget):
    layout: QVBoxLayout

    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self._setup_default_modes()
        self._setup_letters()
        self._setup_components()
        self._setup_layouts()

    def _setup_components(self) -> None:
        self.main_sequence_widget = MainSequenceWidget(self)
        self.main_tab_widget = MainTabWidget(self)
        self.image_cache_manager = ImageCacheManager(self)
        self.layout_manager = MainWidgetLayoutManager(self)

    def _setup_layouts(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout_manager.configure_layouts()

    def _setup_default_modes(self) -> None:
        self.prop_type = STAFF
        self.grid_mode = DIAMOND

    def _setup_letters(self) -> None:
        self.all_pictographs: Dict[Letters, Dict[str, Pictograph]] = {
            letter: {} for letter in all_letters
        }
        self.letter_loader = MainLetterLoader(self)
        self.letters: Dict[Letters, List[Dict]] = self.letter_loader.load_all_letters()

    ### EVENT HANDLERS ###

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.main_sequence_widget.resize_sequence_widget()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.main_window._set_dimensions()
