import json
import os
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtGui import QResizeEvent, QKeyEvent
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from widgets.graphical_object_svg_manager import GraphicalObjectSvgManager
from utilities.TypeChecking.letter_lists import all_letters
from utilities.TypeChecking.TypeChecking import Letters
from constants import DIAMOND, STAFF
from utilities.TypeChecking.prop_types import PropTypes
from widgets.main_widget.special_placement_loader import SpecialPlacementLoader
from widgets.pictograph.components.placement_managers.arrow_placement_manager.components.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)

from widgets.pictograph.pictograph import Pictograph
from ..image_cache_manager import ImageCacheManager
from ..main_tab_widget.main_tab_widget import MainTabWidget
from .main_widget_layout_manager import MainWidgetLayoutManager
from .letter_loader import LetterLoader
from ..sequence_widget.sequence_widget import MainSequenceWidget

if TYPE_CHECKING:
    from main import MainWindow


class MainWidget(QWidget):
    prop_type: PropTypes = STAFF

    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self._setup_default_modes()
        self._setup_letters()
        self._setup_components()
        self._setup_layouts()

    def _setup_components(self) -> None:
        self._setup_special_placements()
        self.svg_manager = GraphicalObjectSvgManager()
        self.turns_tuple_generator = TurnsTupleGenerator()
        self.sequence_widget = MainSequenceWidget(self)
        self.main_tab_widget = MainTabWidget(self)
        self.image_cache_manager = ImageCacheManager(self)

    def _setup_special_placements(self):
        self.special_placement_loader = SpecialPlacementLoader(self)
        self.special_placements: dict[
            str, dict[str, dict[str, dict[str, list[int]]]]
        ] = self.special_placement_loader.load_special_placements()

    def _setup_layouts(self) -> None:
        self.layout_manager = MainWidgetLayoutManager(self)
        self.layout_manager.configure_layouts()

    def _setup_default_modes(self) -> None:
        self.grid_mode = DIAMOND

    def _setup_letters(self) -> None:
        self.all_pictographs: dict[Letters, dict[str, Pictograph]] = {
            letter: {} for letter in all_letters
        }
        self.letter_loader = LetterLoader(self)
        self.letters: dict[Letters, list[dict]] = self.letter_loader.load_all_letters()

    ### EVENT HANDLERS ###

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.sequence_widget.resize_sequence_widget()
        self.main_tab_widget.codex.resize_codex()

    layout: QHBoxLayout

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Q or event.key() == Qt.Key.Key_F5:
            self.special_placement_loader.refresh_placements()
        else:
            super().keyPressEvent(event)

    def toggle_main_sequence_widget(self):
        if self.sequence_widget.isHidden():
            self.sequence_widget.show()
        else:
            self.sequence_widget.hide()
            self.main_tab_widget.setGeometry(0, 0, self.width(), self.height())

    def resize_sequence_widget(self):
        self.sequence_widget.resize_sequence_widget()

    def resize_codex(self):
        if not self.sequence_widget.isHidden():
            self.main_tab_widget.setGeometry(
                self.width() // 2, 0, self.width() // 2, self.height()
            )

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.main_window.window_manager.set_dimensions()
        self.resize_sequence_widget()
        self.resize_codex()
