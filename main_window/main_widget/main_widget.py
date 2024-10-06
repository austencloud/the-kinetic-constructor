import json

from PyQt6.QtGui import QKeyEvent, QCursor, QCloseEvent
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTabWidget

from typing import TYPE_CHECKING
from Enums.Enums import Letter
from Enums.PropTypes import PropType
from letter_determiner.letter_determiner import LetterDeterminer
from main_window.main_widget.grid_mode_checker import GridModeChecker
from main_window.main_widget.learn_widget.learn_widget import LearnWidget
from .pcitograph_dict_loader import PictographDictLoader
from .sequence_properties_manager.sequence_properties_manager import (
    SequencePropertiesManager,
)
from .top_builder_widget.top_builder_widget import TopBuilderWidget
from objects.graphical_object.svg_manager.graphical_object_svg_manager import SvgManager
from .sequence_level_evaluator import SequenceLevelEvaluator
from .thumbnail_finder import ThumbnailFinder
from utilities.path_helpers import get_images_and_data_path
from styles.main_widget_tab_bar_styler import MainWidgetTabBarStyler
from .dictionary_widget.dictionary_widget import DictionaryWidget
from .metadata_extractor import MetaDataExtractor
from .json_manager.json_manager import JsonManager
from .turns_tuple_generator.turns_tuple_generator import TurnsTupleGenerator
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from .pictograph_key_generator import PictographKeyGenerator
from ..main_widget.special_placement_loader import SpecialPlacementLoader

if TYPE_CHECKING:
    from splash_screen import SplashScreen
    from main_window.main_window import MainWindow

from utilities.path_helpers import get_images_and_data_path
from PyQt6.QtCore import QTimer


class MainWidget(QTabWidget):
    def __init__(
        self, main_window: "MainWindow", splash_screen: "SplashScreen" = None
    ) -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self.settings_manager = main_window.settings_manager
        self.initialized = False
        # Pass the splash_screen reference
        self.splash_screen = splash_screen

        self._setup_pictograph_cache()
        self._set_prop_type()
        # self.set_grid_mode()

        self._setup_letters()
        self._initialize_managers()

        self._setup_ui_components()
        self.currentChanged.connect(self.on_tab_changed)
        self.tabBar().setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.splash_screen.update_progress(100, "Initialization complete!")
        QTimer.singleShot(0, self.load_state)

    def _initialize_managers(self):
        """Setup all the managers and helper components."""
        self.splash_screen.update_progress(20, "Loading JSON Manager...")
        self.json_manager = JsonManager(self)

        self.splash_screen.update_progress(30, "Loading SVG Manager...")
        self.svg_manager = SvgManager(self)

        self.splash_screen.update_progress(40, "Loading key generators...")
        self.turns_tuple_generator = TurnsTupleGenerator()
        self.pictograph_key_generator = PictographKeyGenerator(self)

        self.splash_screen.update_progress(50, "Loading special placements...")
        self.special_placement_loader = SpecialPlacementLoader(self)
        self._setup_special_placements()

        self.splash_screen.update_progress(60, "Loading Metadata Extractor...")
        self.metadata_extractor = MetaDataExtractor(self)
        self.tab_bar_styler = MainWidgetTabBarStyler(self)
        self.sequence_level_evaluator = SequenceLevelEvaluator()
        self.sequence_properties_manager = SequencePropertiesManager(self)
        self.thumbnail_finder = ThumbnailFinder(self)
        self.grid_mode_checker = GridModeChecker()

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
                # self.dictionary_widget.show_initial_section()
                self.dictionary_widget.resize_dictionary_widget()
        elif index == self.learn_tab_index:
            self.main_window.settings_manager.global_settings.set_current_tab("learn")
            self.learn_widget.resize_learn_widget()

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

    def _setup_ui_components(self):
        # Initialize special_placement_loader here
        self.splash_screen.update_progress(70, "Setting up build tab...")
        self.top_builder_widget = TopBuilderWidget(self)
        self.splash_screen.update_progress(80, "Setting up browse tab...")
        self.dictionary_widget = DictionaryWidget(self)
        self.splash_screen.update_progress(90, "Setting up learn tab...")
        self.learn_widget = LearnWidget(self)

        self.addTab(self.top_builder_widget, "Build")
        self.addTab(self.dictionary_widget, "Browse")
        self.addTab(self.learn_widget, "Learn")

        self.builder_tab_index = 0
        self.dictionary_tab_index = 1
        self.learn_tab_index = 2

        # Setup the current tab based on settings
        current_tab = (
            self.main_window.settings_manager.global_settings.get_current_tab()
        )
        tab_mapping = {
            "sequence_builder": self.builder_tab_index,
            "dictionary": self.dictionary_tab_index,
            "learn": self.learn_tab_index,
        }
        self.setCurrentIndex(tab_mapping.get(current_tab, 0))

    def _setup_special_placements(self) -> None:
        self.special_placements: dict[
            str, dict[str, dict[str, dict[str, list[int]]]]
        ] = self.special_placement_loader.load_special_placements()

    def set_grid_mode(self, grid_mode: str) -> None:
        self.main_window.settings_manager.global_settings.set_grid_mode(grid_mode)
        self.main_window.menu_bar_widget.menu_bar.grid_mode_menu.toggle_selected_grid_mode(
            grid_mode.capitalize()
        )
        self.main_window.settings_manager.save_settings()
        self.special_placement_loader.refresh_placements()
        self.pictograph_dicts = self.pictograph_dict_loader.load_all_pictograph_dicts()

        start_pos_manager = (
            self.top_builder_widget.sequence_builder.manual_builder.start_pos_picker.start_pos_manager
        )
        start_pos_manager.clear_start_positions()
        start_pos_manager.setup_start_positions()

        sequence_clearer = self.top_builder_widget.sequence_widget.sequence_clearer
        sequence_clearer.clear_sequence()

        pictograph_container = (
            self.top_builder_widget.sequence_widget.graph_editor.pictograph_container
        )

        pictograph_container.GE_pictograph_view.set_to_blank_grid()
        self._setup_special_placements()

    def _setup_letters(self) -> None:
        self.splash_screen.update_progress(10, "Loading pictograph dictionaries...")
        self.pictograph_dict_loader = PictographDictLoader(self)
        self.pictograph_dicts: dict[Letter, list[dict]] = (
            self.pictograph_dict_loader.load_all_pictograph_dicts()
        )
        self.letter_determiner = LetterDeterminer(self)

    ### EVENT HANDLERS ###

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Q or event.key() == Qt.Key.Key_F5:
            self.special_placement_loader.refresh_placements()
        else:
            super().keyPressEvent(event)

    def resize_widgets(self):
        self.top_builder_widget.resize_top_builder_widget()
        self.dictionary_widget.browser.resize_dictionary_browser()
        self.learn_widget.resize_learn_widget()

    def showEvent(self, event):
        super().showEvent(event)
        self.apply_background()
        self.main_window.geometry_manager.set_dimensions()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.setStyleSheet(self.tab_bar_styler.get_tab_stylesheet())

    def apply_background(self):
        self.background_manager = (
            self.main_window.settings_manager.global_settings.setup_background_manager(
                self
            )
        )
        self.background_manager.update_required.connect(self.update)

    def update_background(self, bg_type: str):
        self.apply_background()
        self.update()

    def closeEvent(self, event: QCloseEvent):
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
            self.top_builder_widget.sequence_widget.beat_frame.populator.populate_beat_frame_from_json(
                current_sequence
            )
            self.top_builder_widget.sequence_builder.manual_builder.option_picker.update_option_picker()

    def get_tab_bar_height(self):
        return self.tab_bar_styler.tab_height
