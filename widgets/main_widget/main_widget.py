import json
from PyQt6.QtWidgets import QHBoxLayout, QApplication
from PyQt6.QtGui import QKeyEvent, QResizeEvent
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
from widgets.main_widget.top_builder_widget import TopBuilderWidget

from widgets.main_widget.letter_loader import LetterLoader
from widgets.menu_bar.preferences_dialog import PreferencesDialog
from widgets.menu_bar.prop_type_selector import PropTypeSelector
from widgets.pictograph.pictograph import Pictograph
from widgets.scroll_area.components.pictograph_key_generator import (
    PictographKeyGenerator,
)
from constants import DIAMOND
from widgets.sequence_recorder.sequence_recorder import (
    SequenceRecorder,
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
        self.initialized = False

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

        self.top_builder_widget = TopBuilderWidget(self)
        self.sequence_recorder = SequenceRecorder(self)
        self.addTab(self.top_builder_widget, "Builder")
        self.addTab(self.sequence_recorder, "Recorder")
        # self.addTab(self.letterbook, "LetterBook")
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

        elif event.key() == 96:
            current_widget = self.currentWidget()
            if current_widget == self.top_builder_widget:
                self.setCurrentWidget(self.sequence_recorder)
            elif current_widget == self.sequence_recorder:
                self.setCurrentWidget(self.top_builder_widget)
        else:
            super().keyPressEvent(event)

    def on_tab_changed(self) -> None:
        current_widget = self.currentWidget()
        if current_widget == self.top_builder_widget:
            if not self.top_builder_widget.initialized:
                self.top_builder_widget.initialized = True
                self.top_builder_widget.sequence_widget.resize_sequence_widget()
                self.top_builder_widget.builder_toolbar.resize_current_tab()
        elif current_widget == self.sequence_recorder:
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
                    QApplication.processEvents()

            QApplication.processEvents()
            if not self.webcam_initialized:
                self.sequence_recorder.capture_frame.video_display_frame.init_webcam()
                self.webcam_initialized = True

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.main_window.window_manager.set_dimensions()
        self.on_tab_changed()

    def resizeEvent(self, event: QKeyEvent):
        # resize the scroll area of the builder tab
        current_widget = self.currentWidget()
        if current_widget == self.top_builder_widget:
            self.top_builder_widget.sequence_widget.resize_sequence_widget()
            self.top_builder_widget.builder_toolbar.resize_current_tab()
        elif current_widget == self.sequence_recorder:
            self.sequence_recorder.resize_sequence_recorder()
