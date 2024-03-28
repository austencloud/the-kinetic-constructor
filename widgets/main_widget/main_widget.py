import json
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from Enums.Enums import Letter
from Enums.PropTypes import PropType
from objects.graphical_object.graphical_object_svg_manager import (
    GraphicalObjectSvgManager,
)
from path_helpers import get_images_and_data_path
from styles.get_tab_stylesheet import get_tab_stylesheet
from widgets.factories.button_factory.button_factory import ButtonFactory
from widgets.json_manager import JSON_Manager
from widgets.letterbook.letterbook import LetterBook
from widgets.main_widget.top_level_builder_widget import TopLevelBuilderWidget

from widgets.main_widget.letter_loader import LetterLoader
from widgets.menu_bar.preferences_dialog import PreferencesDialog
from widgets.menu_bar.prop_type_selector import PropTypeSelector
from widgets.pictograph.pictograph import Pictograph
from widgets.scroll_area.components.pictograph_key_generator import (
    PictographKeyGenerator,
)
from constants import DIAMOND
from widgets.sequence_recorder_widget.sequence_recorder_widget import (
    SequenceRecorderWidget,
)
from ..main_widget.special_placement_loader import SpecialPlacementLoader
from ..pictograph.components.placement_managers.arrow_placement_manager.components.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)
from ..main_builder_widget.builder_toolbar import (
    BuilderToolbar,
)
from widgets.sequence_widget.sequence_widget import SequenceWidget
from PyQt6.QtWidgets import QTabWidget

if TYPE_CHECKING:
    from main import MainWindow


class MainWidget(QTabWidget):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self._setup_pictograph_cache()
        self._set_prop_type()
        self._setup_default_modes()
        self._setup_letters()
        self._setup_components()
        self.currentChanged.connect(self.on_tab_changed)
        self.setStyleSheet(get_tab_stylesheet())
        self.webcam_initialized = False  # Add an initialization flag

    def _setup_pictograph_cache(self) -> None:
        self.pictograph_cache: dict[str, dict[str, "Pictograph"]] = {}
        for letter in Letter:
            self.pictograph_cache[letter] = {}

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
        self.preferences_dialog = PreferencesDialog(self)
        self.special_placement_loader = SpecialPlacementLoader(self)
        self._setup_special_placements()

        self.top_level_builder_widget = TopLevelBuilderWidget()

        builder_layout = QHBoxLayout(self.top_level_builder_widget)
        self.builder_toolbar = BuilderToolbar(self)
        self.sequence_widget = SequenceWidget(self)
        self.letterbook = LetterBook(self)

        builder_layout.addWidget(self.sequence_widget, 1)
        builder_layout.addWidget(self.builder_toolbar, 1)

        self.sequence_recorder_widget = SequenceRecorderWidget(self)
        self.addTab(self.top_level_builder_widget, "Builder")
        self.addTab(self.sequence_recorder_widget, "Recorder")
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

    def on_tab_changed(self):
        current_widget = self.currentWidget()
        if current_widget == self.top_level_builder_widget:
            self.sequence_widget.resize_sequence_widget()
            self.builder_toolbar.resize_current_tab()
        elif current_widget == self.sequence_recorder_widget:
            if not self.webcam_initialized:
                self.sequence_recorder_widget.video_display.init_webcam()
                self.webcam_initialized = True
            self.sequence_recorder_widget.resize_sequence_recorder_widget()

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.main_window.window_manager.set_dimensions()
        self.on_tab_changed()
