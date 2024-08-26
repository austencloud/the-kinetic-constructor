import json
import threading
from PyQt6.QtGui import QKeyEvent, QCursor
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from Enums.Enums import Letter
from Enums.PropTypes import PropType


from main_window.main_widget.letter_loader import LetterLoader
from main_window.main_widget.sequence_properties_manager.sequence_properties_manager import (
    SequencePropertiesManager,
)
from main_window.main_widget.top_builder_widget.top_builder_widget import TopBuilderWidget
from objects.graphical_object.svg_manager.graphical_object_svg_manager import (
    SvgManager,
)
from widgets.pictograph.components.placement_managers.arrow_placement_manager.components.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)
from widgets.sequence_difficulty_evaluator import SequenceLevelEvaluator
from main_window.main_widget.dictionary_widget.dictionary_browser.thumbnail_box.thumbnail_finder import ThumbnailFinder
from utilities.path_helpers import get_images_and_data_path
from styles.get_tab_stylesheet import get_tab_stylesheet
from main_window.main_widget.dictionary_widget.dictionary_widget import DictionaryWidget
from main_window.main_widget.dictionary_widget.dictionary_browser.thumbnail_box.metadata_extractor import MetaDataExtractor
from main_window.main_widget.json_manager.json_manager import JSON_Manager

from widgets.pictograph.pictograph import Pictograph
from main_window.main_widget.pictograph_key_generator import (
    PictographKeyGenerator,
)
from data.constants import DIAMOND

from ..main_widget.special_placement_loader import SpecialPlacementLoader

from PyQt6.QtWidgets import QTabWidget

if TYPE_CHECKING:
    from main import MainWindow
import json

from utilities.path_helpers import get_images_and_data_path


class MainWidget(QTabWidget):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self._setup_pictograph_cache()
        self._set_prop_type()
        self._setup_default_modes()
        self._setup_letters()
        self._setup_components()
        self.setStyleSheet(get_tab_stylesheet())
        self.webcam_initialized = False  # Add an initialization flag
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
        elif index == self.sequence_card_tab_index:
            self.main_window.settings_manager.global_settings.set_current_tab(
                "sequence_cards"
            )

    def initialize_webcam_async(self):
        """Start the webcam initialization in a separate thread to avoid blocking the UI."""
        thread = threading.Thread(target=self.init_webcam, daemon=True)
        print("Starting webcam initialization thread")
        thread.start()

    def init_webcam(self):
        """Method to request webcam initialization via signal."""
        self.sequence_recorder.capture_frame.video_display_frame.request_init_webcam()
        print("Webcam initialization requested")

    def _setup_pictograph_cache(self) -> None:
        self.pictograph_cache: dict[str, dict[str, "Pictograph"]] = {}
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
        self.special_placement_loader = SpecialPlacementLoader(self)
        self.metadata_extractor = MetaDataExtractor(self)
        self.sequence_level_evaluator = SequenceLevelEvaluator()
        self.sequence_properties_manager = SequencePropertiesManager(self)
        self.thumbnail_finder = ThumbnailFinder(self)
        self._setup_special_placements()

        self.top_builder_widget = TopBuilderWidget(self)
        self.dictionary_widget = DictionaryWidget(self)
        # self.sequence_recorder = SequenceRecorder(self)
        # self.sequence_card_tab = SequenceCardTab(self)

        self.addTab(self.top_builder_widget, "Builder")
        self.addTab(self.dictionary_widget, "Dictionary")

        self.builder_tab_index = 0
        self.dictionary_tab_index = 1
        self.recorder_tab_index = 2
        self.sequence_card_tab_index = 3

        current_tab = (
            self.main_window.settings_manager.global_settings.get_current_tab()
        )

        tab_mapping = {
            "sequence_builder": self.builder_tab_index,
            "dictionary": self.dictionary_tab_index,
            "recorder": self.recorder_tab_index,
            "sequence_cards": self.sequence_card_tab_index,
        }
        self.setCurrentIndex(tab_mapping.get(current_tab, 0))

        self.initialized = True

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

    def resize_starting_widget(self, starting_widget):
        if starting_widget == self.top_builder_widget:
            self.top_builder_widget.sequence_widget.resize_sequence_widget()
            self.top_builder_widget.sequence_builder.resize_sequence_builder()
        elif starting_widget == self.dictionary_widget:
            self.dictionary_widget.browser.resize_dictionary_browser()

    def resize_all_widgets(self):
        self.currentChanged.disconnect(self.on_tab_changed)
        self.resize_starting_widget(self.currentWidget())
        self.currentChanged.connect(self.on_tab_changed)
        self.main_window.menu_bar_widget.resize_menu_bar_widget()

    def showEvent(self, event):
        super().showEvent(event)
        self.load_state()
        self.resize_all_widgets()
        self.apply_background()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.main_window.window_manager.set_dimensions()

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
            self.top_builder_widget.sequence_builder.transition_to_sequence_building()
            self.top_builder_widget.sequence_widget.beat_frame.populate_beat_frame_from_json(
                current_sequence
            )
            self.top_builder_widget.sequence_builder.option_picker.update_option_picker()
