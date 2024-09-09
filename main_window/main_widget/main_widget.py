import json
import threading
from PyQt6.QtGui import QKeyEvent, QCursor
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from Enums.Enums import Letter
from Enums.PropTypes import PropType
from letter_determiner.letter_determiner import LetterDeterminer
from main_window.main_widget.sequence_recorder.sequence_recorder import SequenceRecorder
from .letter_loader import LetterLoader
from .sequence_properties_manager.sequence_properties_manager import (
    SequencePropertiesManager,
)
from .top_builder_widget.top_builder_widget import TopBuilderWidget
from objects.graphical_object.svg_manager.graphical_object_svg_manager import SvgManager

from .sequence_level_evaluator import SequenceLevelEvaluator
from .thumbnail_finder import (
    ThumbnailFinder,
)
from utilities.path_helpers import get_images_and_data_path
from styles.get_tab_stylesheet import get_tab_stylesheet
from .dictionary_widget.dictionary_widget import DictionaryWidget
from .metadata_extractor import MetaDataExtractor
from .json_manager.json_manager import JSON_Manager
from .turns_tuple_generator.turns_tuple_generator import TurnsTupleGenerator
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from .pictograph_key_generator import PictographKeyGenerator
from data.constants import DIAMOND

from ..main_widget.special_placement_loader import SpecialPlacementLoader

from PyQt6.QtWidgets import QTabWidget

if TYPE_CHECKING:
    from splash_screen import SplashScreen
    from main_window.main_window import MainWindow
import json

from utilities.path_helpers import get_images_and_data_path


class MainWidget(QTabWidget):
    def __init__(
        self, main_window: "MainWindow", splash_screen: "SplashScreen" = None
    ) -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self.settings_manager = main_window.settings_manager

        # Pass the splash_screen reference
        self.splash_screen = splash_screen

        self.splash_screen.update_progress(5, "Setting up pictograph cache...")
        self._setup_pictograph_cache()

        self.splash_screen.update_progress(15, "Setting prop type...")
        self._set_prop_type()

        self.splash_screen.update_progress(25, "Setting up default modes...")
        self._setup_default_modes()

        self.splash_screen.update_progress(35, "Loading letters...")
        self._setup_letters()

        self.splash_screen.update_progress(
            50, "Setting up JSON manager and components..."
        )
        self.splash_screen.update_progress(55, "Loading JSON Manager...")
        self.json_manager = JSON_Manager(self)

        self.splash_screen.update_progress(60, "Loading SVG Manager...")
        self.svg_manager = SvgManager()

        self.splash_screen.update_progress(65, "Loading Turns Tuple Generator...")
        self.turns_tuple_generator = TurnsTupleGenerator()

        self.splash_screen.update_progress(70, "Loading Pictograph Key Generator...")
        self.pictograph_key_generator = PictographKeyGenerator(self)

        self.splash_screen.update_progress(75, "Setting up special placements...")
        self.special_placement_loader = SpecialPlacementLoader(self)
        self._setup_special_placements()

        self.splash_screen.update_progress(80, "Loading Metadata Extractor...")
        self.metadata_extractor = MetaDataExtractor(self)

        self.splash_screen.update_progress(85, "Loading other components...")
        self.sequence_level_evaluator = SequenceLevelEvaluator()
        self.sequence_properties_manager = SequencePropertiesManager(self)
        self.thumbnail_finder = ThumbnailFinder(self)

        self._setup_ui_components()

        self.splash_screen.update_progress(100, "Initialization complete.")
        self.setStyleSheet(get_tab_stylesheet())
        self.webcam_initialized = False
        self.initialized = True
        self.currentChanged.connect(self.on_tab_changed)
        self.tabBar().setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def on_tab_changed(self, index):
        if index == self.builder_tab_index:
            self.main_window.settings_manager.global_settings.set_current_tab(
                "sequence_builder"
            )
            if not self.top_builder_widget.initialized:
                self.top_builder_widget.initialized = True
                self.top_builder_widget.resize_top_builder_widget()
        elif index == self.dictionary_tab_index:
            self.main_window.settings_manager.global_settings.set_current_tab(
                "dictionary"
            )
            if not self.dictionary_widget.initialized:
                self.dictionary_widget.initialized = True
                self.dictionary_widget.resize_dictionary_widget()
        elif index == self.recorder_tab_index:
            self.main_window.settings_manager.global_settings.set_current_tab(
                "recorder"
            )
        # elif index == self.sequence_card_tab_index:
        #     self.main_window.settings_manager.global_settings.set_current_tab(
        #         "sequence_cards"
        #     )

    # def initialize_webcam_async(self):
    #     """Start the webcam initialization in a separate thread to avoid blocking the UI."""
    #     thread = threading.Thread(target=self.init_webcam, daemon=True)
    #     print("Starting webcam initialization thread")
    #     thread.start()

    # def init_webcam(self):
    #     """Method to request webcam initialization via signal."""
    #     self.sequence_recorder.capture_frame.video_display_frame.request_init_webcam()
    #     print("Webcam initialization requested")
    def _setup_pictograph_cache(self) -> None:
        self.pictograph_cache: dict[str, dict[str, "BasePictograph"]] = {}
        for letter in Letter:
            self.pictograph_cache[letter] = {}

    def _set_prop_type(self) -> None:
        settings_path = get_images_and_data_path("settings.json")
        with open(settings_path, "r", encoding="utf-8") as file:
            settings: dict[str, dict[str, str | bool]] = json.load(file)
        prop_type_value = settings.get("global", {}).get("prop_type", "staff")
        self.prop_type = PropType.get_prop_type(prop_type_value)

    def _setup_components(self) -> None:
        self.json_manager = JSON_Manager(self)
        self.svg_manager = SvgManager()
        self.turns_tuple_generator = TurnsTupleGenerator()
        self.pictograph_key_generator = PictographKeyGenerator(self)

        self.metadata_extractor = MetaDataExtractor(self)
        self.sequence_level_evaluator = SequenceLevelEvaluator()
        self.sequence_properties_manager = SequencePropertiesManager(self)
        self.thumbnail_finder = ThumbnailFinder(self)

    def _setup_ui_components(self):
        # Initialize special_placement_loader here
        self.splash_screen.update_progress(90, "Loading Builder...")
        self.top_builder_widget = TopBuilderWidget(self)
        self.splash_screen.update_progress(95, "Loading Dictionary...")
        self.dictionary_widget = DictionaryWidget(self)
        # self.sequence_recorder = SequenceRecorder(self)

        self.addTab(self.top_builder_widget, "Builder")
        self.addTab(self.dictionary_widget, "Dictionary")
        # Add more tabs as necessary

        self.builder_tab_index = 0
        self.dictionary_tab_index = 1
        self.recorder_tab_index = 2

        # Setup the current tab based on settings
        current_tab = (
            self.main_window.settings_manager.global_settings.get_current_tab()
        )
        tab_mapping = {
            "sequence_builder": self.builder_tab_index,
            "dictionary": self.dictionary_tab_index,
            "recorder": self.recorder_tab_index,
        }
        self.setCurrentIndex(tab_mapping.get(current_tab, 0))

    def _setup_special_placements(self) -> None:
        self.special_placements: dict[
            str, dict[str, dict[str, dict[str, list[int]]]]
        ] = self.special_placement_loader.load_special_placements()

    def _setup_default_modes(self) -> None:
        self.grid_mode = DIAMOND

    def _setup_letters(self) -> None:
        self.letter_loader = LetterLoader(self)
        self.letters: dict[Letter, list[dict]] = self.letter_loader.load_all_letters()
        self.letter_determiner = LetterDeterminer(self)

    ### EVENT HANDLERS ###

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Q or event.key() == Qt.Key.Key_F5:
            self.special_placement_loader.refresh_placements()
        else:
            super().keyPressEvent(event)

    def resize_current_widget(self, starting_widget):
        if starting_widget == self.top_builder_widget:
            self.top_builder_widget.resize_top_builder_widget()
        elif starting_widget == self.dictionary_widget:
            self.dictionary_widget.browser.resize_dictionary_browser()

    def showEvent(self, event):
        super().showEvent(event)
        self.main_window.menu_bar_widget.resize_menu_bar_widget()
        self.resize_current_widget(self.currentWidget())
        self.apply_background()
        self.load_state()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        # self.main_window.geometry_manager.set_dimensions()
        # self.main_window.showMaximized()

    def apply_background(self):
        self.background_manager = (
            self.main_window.settings_manager.global_settings.setup_background_manager(
                self
            )
        )
        self.background_manager.update_required.connect(self.update)

    def update_background(self, bg_type: str):
        self.apply_background()
        self.update()  # Ensure the widget is redrawn with the new background

    def closeEvent(self, event):
        self.save_state()
        event.accept()

    def save_state(self):
        self.json_manager.loader_saver.save_current_sequence(
            self.json_manager.loader_saver.load_current_sequence_json()
        )
        self.main_window.settings_manager.save_settings()

    def load_state(self):
        self.main_window.settings_manager.load_settings()
        current_sequence = self.json_manager.loader_saver.load_current_sequence_json()
        if len(current_sequence) > 1:
            self.top_builder_widget.sequence_builder.manual_builder.transition_to_sequence_building()
            self.top_builder_widget.sequence_widget.beat_frame.populate_beat_frame_from_json(
                current_sequence
            )
            self.top_builder_widget.sequence_builder.manual_builder.option_picker.update_option_picker()

    def get_tab_bar_height(self):
        return self.tabBar().height()
