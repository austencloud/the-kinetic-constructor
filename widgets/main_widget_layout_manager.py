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
from .ig_tab.ig_tab import IGTab
from .option_picker_tab.option_picker_tab import OptionPickerTab
from .graph_editor_tab.graph_editor_tab import GraphEditorTab
from .graph_editor_tab.graph_editor_key_event_handler import KeyEventHandler
from objects.pictograph.pictograph import Pictograph
from .sequence_widget.sequence_widget import SequenceWidget

if TYPE_CHECKING:
    from main import MainWindow
    from widgets.main_widget import MainWidget


class MainWidgetLayoutManager:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget
        self.configure_layouts()

    def configure_layouts(self) -> None:
        left_frame = self._setup_left_frame()
        right_frame = self._setup_right_frame()
        self._setup_main_layout(left_frame, right_frame)

    def _setup_main_layout(self, left_frame, right_frame) -> None:
        self.main_widget.layout.addWidget(left_frame)
        self.main_widget.layout.addWidget(right_frame)

    def _setup_right_frame(self) -> QFrame:
        right_frame = QFrame()
        right_layout = QVBoxLayout(right_frame)
        right_layout.addWidget(self.main_widget.main_tab_widget)
        return right_frame

    def _setup_left_frame(self) -> QFrame:
        left_frame = QFrame()
        left_layout = QVBoxLayout(left_frame)
        left_layout.addWidget(self.main_widget.sequence_widget)
        return left_frame
