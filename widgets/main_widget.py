from typing import TYPE_CHECKING, Dict, List, Optional
from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
    QTabWidget,
)
from utilities.TypeChecking.letter_lists import all_letters
from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QResizeEvent
import pandas as pd
from constants import (
    BLUE_END_LOC,
    BLUE_MOTION_TYPE,
    BLUE_PROP_ROT_DIR,
    BLUE_START_LOC,
    BLUE_START_ORI,
    BLUE_TURNS,
    DIAMOND,
    END_POS,
    IN,
    LETTER,
    RED_END_LOC,
    RED_MOTION_TYPE,
    RED_PROP_ROT_DIR,
    RED_START_LOC,
    RED_START_ORI,
    RED_TURNS,
    STAFF,
    START_POS,
)
from utilities.TypeChecking.TypeChecking import Letters
from widgets.image_cache_manager import ImageCacheManager
from widgets.main_tab_widget import MainTabWidget
from widgets.main_widget_layout_manager import MainWidgetLayoutManager
from widgets.main_widget_letter_loader import MainWidgetLetterLoader
from .ig_tab.ig_tab import IGTab
from .option_picker_tab.option_picker_tab import OptionPickerTab
from .graph_editor_tab.graph_editor_tab import GraphEditorTab
from .graph_editor_tab.graph_editor_key_event_handler import KeyEventHandler
from objects.pictograph.pictograph import Pictograph
from .sequence_widget.sequence_widget import SequenceWidget

if TYPE_CHECKING:
    from main import MainWindow


class MainWidget(QWidget):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self.prop_type = STAFF
        self.grid_mode = DIAMOND
        
        self._setup_letters()
        
        self.layout:QHBoxLayout = QHBoxLayout(self)
        
        self.sequence_widget = SequenceWidget(self)
        self.main_tab_widget = MainTabWidget(self)
        self.ig_tab, self.option_picker_tab, self.graph_editor_tab = self.main_tab_widget.tabs
        self.image_cache_manager = ImageCacheManager(self)
        self.layout_manager = MainWidgetLayoutManager(self)
        self.layout_manager.configure_layouts()
        
        self.pixmap_cache = {}
        # self.resize(int(self.main_window.width()), int(self.main_window.height()))

    def _setup_letters(self) -> None:
        self.all_pictographs: Dict[Letters, Dict[str, Pictograph]] = {
            letter: {} for letter in all_letters
        }
        self.letter_loader = MainWidgetLetterLoader(self)
        self.letters: Dict[Letters, List[Dict]] = self.letter_loader.load_all_letters()

    ### EVENT HANDLERS ###


    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.sequence_widget.resize_sequence_widget()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.main_window._set_dimensions()
