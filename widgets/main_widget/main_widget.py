import json
from PyQt6.QtWidgets import QTabWidget, QWidget, QHBoxLayout
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from Enums.Enums import Letter
from Enums.PropTypes import PropType
from path_helpers import get_images_and_data_path
from widgets.base_tab_widget import BaseTabWidget
from widgets.factories.button_factory.button_factory import ButtonFactory
from widgets.json_manager import JSON_Manager
from widgets.letterbook.letterbook import LetterBook
from widgets.main_builder_widget.sequence_recorder_container import (
    SequenceRecorderContainer,
)
from widgets.main_widget.letter_loader import LetterLoader
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
from ..main_builder_widget.main_builder_widget import MainBuilderWidget
from widgets.sequence_widget.sequence_widget import SequenceWidget

if TYPE_CHECKING:
    from main import MainWindow


class MainWidget(BaseTabWidget):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self._setup_pictograph_cache()
        self._set_prop_type()
        self._setup_default_modes()
        self._setup_letters()
        self._setup_components()
        self.currentChanged.connect(self.on_tab_changed)

    def _setup_pictograph_cache(self) -> None:
        self.all_pictographs: dict[str, dict[str, "Pictograph"]] = {}
        for letter in Letter:
            self.all_pictographs[letter] = {}

    def _set_prop_type(self) -> None:
        user_settings_path = get_images_and_data_path("user_settings.json")
        with open(user_settings_path, "r", encoding="utf-8") as file:
            user_settings: dict = json.load(file)
        prop_type_value = user_settings.get("prop_type")
        self.prop_type = PropType.get_prop_type(prop_type_value)

    def _setup_components(self) -> None:
        self.button_factory = ButtonFactory()
        self.json_manager = JSON_Manager(self)
        self.graphical_object_svg_manager = GraphicalObjectSvgManager()
        self.prop_type_selector = PropTypeSelector(self)
        self.turns_tuple_generator = TurnsTupleGenerator()
        self.pictograph_key_generator = PictographKeyGenerator()
        self.image_cache_manager = ImageCacheManager(self)
        self.preferences_dialog = PreferencesDialog(self)
        self.special_placement_loader = SpecialPlacementLoader(self)
        self._setup_special_placements()

        builder_widget = QWidget()
        builder_layout = QHBoxLayout(builder_widget)
        self.main_builder_widget = MainBuilderWidget(self)
        self.sequence_widget = SequenceWidget(self)
        self.letterbook = LetterBook(self)
        builder_layout.addWidget(self.sequence_widget, 1)
        builder_layout.addWidget(self.main_builder_widget, 1)
        self.addTab(builder_widget, "Builder")

        self.sequence_recorder_container = SequenceRecorderContainer(self)
        self.addTab(self.sequence_recorder_container, "Recorder")
        self.addTab(self.letterbook, "LetterBook")

    def _setup_special_placements(self) -> None:
        self.special_placements: dict[
            str, dict[str, dict[str, dict[str, list[int]]]]
        ] = self.special_placement_loader.load_special_placements()

    def _setup_default_modes(self) -> None:
        self.grid_mode = DIAMOND

    def _setup_letters(self) -> None:
        self.letter_loader = LetterLoader(self)
        self.letters: dict[Letter, list[dict]] = self.letter_loader.load_all_letters()

    ### EVENT HANDLERS ###

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Q or event.key() == Qt.Key.Key_F5:
            self.special_placement_loader.refresh_placements()
        else:
            super().keyPressEvent(event)

    def on_tab_changed(self) -> None:
        self.resize_visible_tab()

    def resize_visible_tab(self) -> None:
        current_widget = self.currentWidget()
        if current_widget == self.sequence_widget:
            self.sequence_widget.resize_sequence_widget()
        elif current_widget == self.sequence_recorder_container:
            self.sequence_recorder_container.sequence_recorder_widget.resize_sequence_recorder_widget()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.main_window.window_manager.set_dimensions()
        self.main_builder_widget.on_tab_changed()
        self.sequence_widget.resize_sequence_widget()
