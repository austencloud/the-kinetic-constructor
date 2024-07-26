import json
import threading
from PyQt6.QtGui import QKeyEvent
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from Enums.Enums import Letter
from Enums.PropTypes import PropType


from metadata_updater import MetaDataUpdater
from objects.graphical_object.graphical_object_svg_manager import (
    GraphicalObjectSvgManager,
)
from widgets.path_helpers.path_helpers import get_images_and_data_path
from styles.get_tab_stylesheet import get_tab_stylesheet
from widgets.dictionary_widget.dictionary_widget import DictionaryWidget
from widgets.dictionary_widget.thumbnail_box.metadata_extractor import MetaDataExtractor
from widgets.factories.button_factory.button_factory import ButtonFactory
from widgets.json_manager import JSON_Manager
from widgets.main_widget.top_builder_widget import TopBuilderWidget

from widgets.main_widget.letter_loader import LetterLoader
from widgets.menu_bar.main_settings_dialog import MainSettingsDialog
from widgets.menu_bar.prop_type_selector import PropTypeSelector
from widgets.pictograph.pictograph import Pictograph
from widgets.scroll_area.components.pictograph_key_generator import (
    PictographKeyGenerator,
)
from data.constants import DIAMOND
from widgets.sequence_recorder.sequence_recorder import (
    SequenceRecorder,
)
from ..main_widget.special_placement_loader import SpecialPlacementLoader
from ..pictograph.components.placement_managers.arrow_placement_manager.components.turns_tuple_generator.turns_tuple_generator import (
    TurnsTupleGenerator,
)
from PyQt6.QtWidgets import QTabWidget

if TYPE_CHECKING:
    from main import MainWindow
import json

from widgets.path_helpers.path_helpers import get_images_and_data_path


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
        # self.initialize_webcam_async()  # Start webcam initialization
        self.initialized = True
        metadata_updater = MetaDataUpdater(self)


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
        prop_type_value = settings.get("global_settings", {}).get("prop_type", "staff")
        self.prop_type = PropType.get_prop_type(prop_type_value)

    def _setup_components(self) -> None:
        self.button_factory = ButtonFactory()
        self.json_manager = JSON_Manager(self)
        self.graphical_object_svg_manager = GraphicalObjectSvgManager()
        self.prop_type_selector = PropTypeSelector(self)
        self.turns_tuple_generator = TurnsTupleGenerator()
        self.pictograph_key_generator = PictographKeyGenerator()
        self.main_settings_dialog = MainSettingsDialog(self)
        self.special_placement_loader = SpecialPlacementLoader(self)
        self.metadata_extractor = MetaDataExtractor(self)

        self._setup_special_placements()

        self.top_builder_widget = TopBuilderWidget(self)
        self.dictionary = DictionaryWidget(self)
        self.sequence_recorder = SequenceRecorder(self)

        self.addTab(self.top_builder_widget, "Builder")
        self.addTab(self.dictionary, "Dictionary")
        self.addTab(self.sequence_recorder, "Recorder")

        self.builder_tab_index = 0
        self.dictionary_tab_index = 1
        self.recorder_tab_index = 2

        self.setCurrentIndex(self.dictionary_tab_index)
        self.initialized = True

        # Apply the initial background

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

        elif event.key() == 96:
            current_widget = self.currentWidget()
            if current_widget == self.top_builder_widget:
                self.setCurrentWidget(self.sequence_recorder)
            elif current_widget == self.sequence_recorder:
                self.setCurrentWidget(self.top_builder_widget)
        else:
            super().keyPressEvent(event)

    def resize_widget(self, widget):
        if widget == self.top_builder_widget:
            if not self.top_builder_widget.initialized:
                self.top_builder_widget.initialized = True
                self.top_builder_widget.sequence_widget.resize_sequence_widget()
                self.top_builder_widget.sequence_builder.resize_sequence_builder()
        elif widget == self.sequence_recorder:
            if not self.sequence_recorder.initialized:
                self.sequence_recorder.resize_sequence_recorder()
                self.initialized = True
            SW_beat_frame = self.top_builder_widget.sequence_widget.beat_frame
            if SW_beat_frame.sequence_changed:
                SW_beat_frame.sequence_changed = False
                self.sequence_recorder.capture_frame.SR_beat_frame.populate_beat_frame_scenes_from_json()
            else:
                for view in SW_beat_frame.beats:
                    if view.is_filled:
                        view.resize_beat_view()
        elif widget == self.dictionary:
            self.dictionary.browser.resize_dictionary_browser()

    def resize_all_widgets(self):
        starting_widget = self.currentWidget()
        for i in range(self.count()):
            self.setCurrentIndex(i)
            self.resize_widget(self.currentWidget())
        self.setCurrentWidget(starting_widget)

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
