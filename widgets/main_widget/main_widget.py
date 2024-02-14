import json
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QResizeEvent, QKeyEvent
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from Enums.Enums import Letters
from Enums.PropTypes import PropTypes
from widgets.json_manager import JSON_Manager
from widgets.menu_bar.preferences_dialog import PreferencesDialog
from widgets.menu_bar.prop_type_selector import PropTypeSelector


from widgets.pictograph.pictograph import Pictograph
from widgets.scroll_area.components.pictograph_key_generator import (
    PictographKeyGenerator,
)
from ..graphical_object_svg_manager import GraphicalObjectSvgManager

from constants import DIAMOND
from ..main_widget.special_placement_loader import SpecialPlacementLoader
from ..pictograph.components.placement_managers.arrow_placement_manager.components.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)
from ..image_cache_manager import ImageCacheManager
from ..main_tab_widget.main_tab_widget import MainTabWidget
from .main_widget_layout_manager import MainWidgetLayoutManager
from .letter_loader import LetterLoader
from ..sequence_widget.sequence_widget import SequenceWidget

if TYPE_CHECKING:
    from main import MainWindow


class MainWidget(QWidget):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self._setup_pictograph_cache()
        self._set_prop_type()
        self._setup_default_modes()
        self._setup_letters()
        self._setup_components()
        self._setup_layouts()

    def _setup_pictograph_cache(self):
        self.all_pictographs: dict[str, dict[str, "Pictograph"]] = {}
        for letter in Letters:
            self.all_pictographs[letter.value] = {}

    def _set_prop_type(self):
        with open("user_settings.json", "r") as file:
            user_settings: dict = json.load(file)
        prop_type_value = user_settings.get("prop_type")
        self.prop_type = PropTypes.get_prop_type(prop_type_value)

    def _setup_components(self) -> None:
        self._setup_special_placements()
        self.json_manager = JSON_Manager(self)
        self.svg_manager = GraphicalObjectSvgManager()
        self.prop_type_selector = PropTypeSelector(self)
        self.turns_tuple_generator = TurnsTupleGenerator()
        self.pictograph_key_generator = PictographKeyGenerator()
        self.sequence_widget = SequenceWidget(self)
        self.main_tab_widget = MainTabWidget(self)
        self.preferences_dialog = PreferencesDialog(self)
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
        self.letter_loader = LetterLoader(self)
        self.letters: dict[Letters, list[dict]] = self.letter_loader.load_all_letters()

    ### EVENT HANDLERS ###

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Q or event.key() == Qt.Key.Key_F5:
            self.special_placement_loader.refresh_placements()
        else:
            super().keyPressEvent(event)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.main_window.window_manager.set_dimensions()
        self.main_tab_widget.resize_main_tab_widget()
        self.sequence_widget.resize_sequence_widget()

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.main_window.window_manager.set_dimensions()
