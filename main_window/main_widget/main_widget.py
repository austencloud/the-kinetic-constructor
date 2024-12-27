from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget

from typing import TYPE_CHECKING
from Enums.PropTypes import PropType
from main_window.main_widget.browse_tab.browse_tab import BrowseTab
from main_window.main_widget.construct_tab.construct_tab import ConstructTab
from main_window.main_widget.generate_tab.generate_tab import GenerateTab
from main_window.main_widget.learn_tab.learn_tab import LearnTab
from main_window.main_widget.write_tab.write_tab import WriteTab
from main_window.main_widget.main_background_widget import MainBackgroundWidget
from main_window.main_widget.main_widget_tabs import MainWidgetTabs
from main_window.main_widget.tab_fade_manager import TabFadeManager
from main_window.settings_manager.global_settings.main_widget_font_color_updater import (
    MainWidgetFontColorUpdater,
)


from .main_widget_manager import MainWidgetManager
from .main_widget_ui import MainWidgetUI
from .main_widget_events import MainWidgetEvents
from .main_widget_state import MainWidgetState
from .main_widget_background_handler import MainWidgetBackgroundHandler

if TYPE_CHECKING:
    from main_window.settings_manager.settings_manager import SettingsManager
    from .navigation_widget import NavigationWidget
    from main_window.menu_bar_widget.menu_bar_widget import MenuBarWidget
    from splash_screen.splash_screen import SplashScreen
    from ..main_window import MainWindow
    from main_window.menu_bar_widget.background_selector.backgrounds.base_background import (
        BaseBackground,
    )
    from .json_manager.json_manager import JsonManager
    from .sequence_widget.sequence_widget import SequenceWidget

    from objects.graphical_object.svg_manager.graphical_object_svg_manager import (
        SvgManager,
    )
    from .turns_tuple_generator.turns_tuple_generator import TurnsTupleGenerator
    from .pictograph_key_generator import PictographKeyGenerator
    from .special_placement_loader import SpecialPlacementLoader
    from .metadata_extractor import MetaDataExtractor
    from .sequence_level_evaluator import SequenceLevelEvaluator
    from .sequence_properties_manager.sequence_properties_manager import (
        SequencePropertiesManager,
    )
    from .thumbnail_finder import ThumbnailFinder
    from .grid_mode_checker import GridModeChecker
    from base_widgets.base_pictograph.base_pictograph import BasePictograph
    from .pcitograph_dict_loader import PictographDictLoader
    from Enums.Enums import Letter
    from letter_determiner.letter_determiner import LetterDeterminer


class MainWidget(QWidget):

    main_window: "MainWindow"
    settings_manager: "SettingsManager"
    splash_screen: "SplashScreen"

    # Sub-widgets
    constructor_tab: "ConstructTab"
    generator_tab: "GenerateTab"
    dictionary_widget: "BrowseTab"
    learn_widget: "LearnTab"
    act_tab: "WriteTab"

    # Handlers
    tabs_handler: "MainWidgetTabs"
    manager: "MainWidgetManager"
    ui_handler: "MainWidgetUI"
    event_handler: "MainWidgetEvents"
    state_handler: "MainWidgetState"
    background_handler: "MainWidgetBackgroundHandler"

    # Managers and Helpers
    svg_manager: "SvgManager"
    turns_tuple_generator: "TurnsTupleGenerator"
    pictograph_key_generator: "PictographKeyGenerator"
    special_placement_loader: "SpecialPlacementLoader"
    metadata_extractor: "MetaDataExtractor"
    sequence_level_evaluator: "SequenceLevelEvaluator"
    sequence_properties_manager: "SequencePropertiesManager"
    thumbnail_finder: "ThumbnailFinder"
    grid_mode_checker: "GridModeChecker"
    fade_manager: TabFadeManager
    font_color_updater: "MainWidgetFontColorUpdater"

    # Layouts and Widgets
    top_layout: QHBoxLayout
    main_layout: QVBoxLayout
    # central_layout: QHBoxLayout
    # content_layout: QHBoxLayout
    # right_stacked_widget: QStackedWidget
    # main_stacked_widget: QStackedWidget
    # dictionary_learn_widget: QStackedWidget
    # build_generate_widget: QWidget
    # build_generate_layout: QHBoxLayout
    menu_bar_widget: "MenuBarWidget"
    navigation_widget: "NavigationWidget"
    sequence_widget: "SequenceWidget"
    background_widget: "MainBackgroundWidget"
    content_stack: QStackedWidget

    # Indices for tabs
    build_tab_index: int = 0
    generate_tab_index: int = 1
    dictionary_tab_index: int = 2
    learn_tab_index: int = 3
    act_tab_index: int = 4

    # Current state
    current_tab: str
    background: "BaseBackground"
    json_manager: "JsonManager"

    # Other attributes
    pictograph_cache: dict[str, dict[str, "BasePictograph"]]
    prop_type: PropType
    pictograph_dict_loader: "PictographDictLoader"
    pictograph_dicts: dict["Letter", list[dict]]
    letter_determiner: "LetterDeterminer"
    special_placements: dict[str, dict[str, dict[str, dict[str, list[int]]]]]

    def __init__(self, main_window: "MainWindow", splash_screen: "SplashScreen" = None):
        super().__init__(main_window)
        self.main_window = main_window
        self.main_window.main_widget = self
        self.settings_manager = main_window.settings_manager
        self.splash_screen = splash_screen

        self.tabs_handler = MainWidgetTabs(self)
        self.manager = MainWidgetManager(self)
        self.ui_handler = MainWidgetUI(self)
        self.event_handler = MainWidgetEvents(self)
        self.state_handler = MainWidgetState(self)
        self.background_handler = MainWidgetBackgroundHandler(self)

        QTimer.singleShot(0, self.state_handler.load_state)

    def paintEvent(self, a0):
        return super().paintEvent(a0)

    def showEvent(self, event):
        self.event_handler.showEvent(event)

    def resizeEvent(self, event) -> None:
        self.event_handler.resizeEvent(event)
