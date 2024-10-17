import json

from PyQt6.QtGui import QKeyEvent, QCursor, QCloseEvent, QPainter, QPaintEvent
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QStackedWidget,
    QTabBar,
    QWidget,
    QPushButton,
)

from typing import TYPE_CHECKING, Union
from Enums.Enums import Letter
from Enums.PropTypes import PropType
from letter_determiner.letter_determiner import LetterDeterminer
from main_window.main_widget.navigation_widget import NavigationWidget


from main_window.main_widget.sequence_builder.auto_builder.sequence_generator import SequenceGeneratorWidget
from main_window.main_widget.sequence_builder.manual_builder import ManualBuilderWidget
from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget
from main_window.menu_bar_widget.menu_bar_widget import MenuBarWidget
from .grid_mode_checker import GridModeChecker
from .learn_widget.learn_widget import LearnWidget
from .pcitograph_dict_loader import PictographDictLoader
from .sequence_properties_manager.sequence_properties_manager import (
    SequencePropertiesManager,
)
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


class MainWidget(QWidget):
    def __init__(self, main_window: "MainWindow", splash_screen: "SplashScreen" = None):
        super().__init__(main_window)
        self.main_window = main_window
        self.main_window.main_widget = self
        self.background_manager = None
        self.settings_manager = main_window.settings_manager
        self.initialized = False
        self.splash_screen = splash_screen

        self._setup_pictograph_cache()
        self._set_prop_type()

        self._setup_letters()
        self._initialize_managers()

        self._setup_ui_components()
        self.apply_background()

        self.setAttribute(Qt.WidgetAttribute.WA_OpaquePaintEvent, False)

        self.splash_screen.update_progress(100, "Initialization complete!")
        QTimer.singleShot(0, self.load_state)
        self.paint_timer = QTimer(self)
        self.paint_timer.timeout.connect(
            lambda: self.paintEvent(QPaintEvent(self.rect()))
        )

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

        self.stacked_widget.setCurrentIndex(index)
        # if index in [0, 1]:  # Build or Generate tab indices
        #     self.sequence_widget.show()
        # else:
        #     self.sequence_widget.hide()

        if index == self.build_tab_index:
            self.main_window.settings_manager.global_settings.set_current_tab("build")
            self.manual_builder.resize_manual_builder()

        elif index == self.generate_tab_index:
            self.main_window.settings_manager.global_settings.set_current_tab(
                "generate"
            )
            self.sequence_generator.resize_sequence_generator()

        elif index == self.dictionary_tab_index:
            self.main_window.settings_manager.global_settings.set_current_tab(
                "dictionary"
            )
            if not self.dictionary_widget.initialized:
                self.dictionary_widget.initialized = True
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

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)
        self.menu_bar_widget = MenuBarWidget(self)

        self.main_layout.addWidget(self.menu_bar_widget)
        self.navigation_widget = NavigationWidget(self)
        self.navigation_widget.tab_changed.connect(self.on_tab_changed)
        self.main_layout.addWidget(self.navigation_widget)

        self.content_layout = QHBoxLayout()
        self.main_layout.addLayout(self.content_layout)

        self.sequence_widget = SequenceWidget(self)
        self.content_layout.addWidget(self.sequence_widget, 1)

        self.stacked_widget = QStackedWidget()
        self.content_layout.addWidget(self.stacked_widget, 1)

        self.manual_builder = ManualBuilderWidget(self)
        self.sequence_generator = SequenceGeneratorWidget(self)
        self.dictionary_widget = DictionaryWidget(self)
        self.learn_widget = LearnWidget(self)

        self.stacked_widget.addWidget(self.manual_builder)
        self.stacked_widget.addWidget(self.sequence_generator)
        self.stacked_widget.addWidget(self.dictionary_widget)
        self.stacked_widget.addWidget(self.learn_widget)

        self.build_tab_index = 0
        self.generate_tab_index = 1
        self.dictionary_tab_index = 2
        self.learn_tab_index = 3

    def _setup_special_placements(self) -> None:
        self.special_placements: dict[
            str, dict[str, dict[str, dict[str, list[int]]]]
        ] = self.special_placement_loader.load_special_placements()

    def set_grid_mode(self, grid_mode: str) -> None:
        self.main_window.settings_manager.global_settings.set_grid_mode(grid_mode)

        self.main_window.settings_manager.save_settings()
        self.special_placement_loader.refresh_placements()
        self.pictograph_dicts = self.pictograph_dict_loader.load_all_pictograph_dicts()
        self.manual_builder = self.manual_builder
        start_pos_manager = self.manual_builder.start_pos_picker.start_pos_manager
        start_pos_manager.clear_start_positions()
        start_pos_manager.setup_start_positions()

        sequence_clearer = self.sequence_widget.sequence_clearer
        sequence_clearer.clear_sequence(show_indicator=False)

        pictograph_container = self.sequence_widget.graph_editor.pictograph_container

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

    def paintEvent(self, event):
        painter = QPainter(self)
        self.background_manager.paint_background(self, painter)

    def showEvent(self, event):
        super().showEvent(event)
        if self.background_manager is None:
            self.background_manager = (
                self.settings_manager.global_settings.setup_background_manager(self)
            )
        self.background_manager.start_animation()

    def hideEvent(self, event):
        super().hideEvent(event)
        if self.background_manager:
            self.background_manager.stop_animation()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.setStyleSheet(self.tab_bar_styler.get_tab_stylesheet())
        self.navigation_widget.resize_navigation_widget()

    def apply_background(self):
        self.background_manager = (
            self.main_window.settings_manager.global_settings.setup_background_manager(
                self
            )
        )
        self.background_manager.update_required.connect(self.update)

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
            self.manual_builder.transition_to_sequence_building()
            self.sequence_widget.beat_frame.populator.populate_beat_frame_from_json(
                current_sequence, is_dictionary_entry=False
            )
            self.manual_builder.option_picker.update_option_picker()

    def get_tab_bar_height(self):
        return self.tab_bar_styler.tab_height
