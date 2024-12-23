from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QStackedWidget, QWidget

from main_window.main_widget.background_widget import BackgroundWidget
from main_window.main_widget.browse_tab.browse_tab import BrowseTab
from main_window.main_widget.build_tab.build_tab import BuildTab
from main_window.main_widget.build_tab.sequence_constructor import SequenceConstructor
from main_window.main_widget.build_tab.sequence_generator.sequence_generator import (
    SequenceGenerator,
)
from main_window.main_widget.build_tab.sequence_widget.sequence_widget import (
    SequenceWidget,
)
from main_window.main_widget.learn_tab.learn_widget import LearnTab
from main_window.main_widget.main_widget_background_handler import (
    MainWidgetBackgroundHandler,
)
from main_window.main_widget.tab_fade_manager import TabFadeManager
from main_window.main_widget.write_tab.act_tab import WriteTab
from main_window.settings_manager.global_settings.main_widget_font_color_updater import (
    MainWidgetFontColorUpdater,
)
from ..menu_bar_widget.menu_bar_widget import MenuBarWidget
from .navigation_widget import NavigationWidget

if TYPE_CHECKING:
    from .main_widget import MainWidget


class MainWidgetUI:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget
        self.splash_screen = main_widget.splash_screen
        self._setup_components()
        self._setup_layout()
        self._setup_indices()

    def _setup_components(self):
        mw = self.main_widget

        # Initialize the main stacked widget
        mw.main_stacked_widget = QStackedWidget()

        # Initialize fade manager
        mw.fade_manager = TabFadeManager(mw)

        # Initialize background handler
        mw.background_handler = MainWidgetBackgroundHandler(mw)
        mw.background_handler.setup_background()

        # Initialize font color updater
        mw.font_color_updater = MainWidgetFontColorUpdater(mw)

        # Initialize all tabs
        mw.menu_bar_widget = MenuBarWidget(mw)
        mw.navigation_widget = NavigationWidget(mw)

        mw.build_tab = BuildTab(mw)  # Unified Build and Generate
        mw.browse_tab = BrowseTab(mw)
        mw.learn_tab = LearnTab(mw)
        mw.write_tab = WriteTab(mw)

        # Add tabs to the main stacked widget
        mw.main_stacked_widget.addWidget(mw.build_tab)  # Index 0
        mw.main_stacked_widget.addWidget(mw.browse_tab)  # Index 1
        mw.main_stacked_widget.addWidget(mw.learn_tab)  # Index 2
        mw.main_stacked_widget.addWidget(mw.write_tab)  # Index 3

    def _setup_layout(self):
        mw = self.main_widget

        mw.main_layout = QVBoxLayout(mw)
        mw.main_layout.setContentsMargins(0, 0, 0, 0)
        mw.main_layout.setSpacing(0)
        mw.setLayout(mw.main_layout)

        top_layout = QHBoxLayout()
        top_layout.addWidget(mw.menu_bar_widget)
        top_layout.addWidget(mw.navigation_widget)

        mw.main_layout.addLayout(top_layout)
        mw.main_layout.addWidget(mw.main_stacked_widget)

    def _setup_indices(self):
        self.main_widget.construct_tab_index = 0
        self.main_widget.browse_tab_index = 1
        self.main_widget.learn_tab_index = 2
        self.main_widget.write_tab_index = 3

    def load_current_tab(self):
        mw = self.main_widget
        mw.current_tab = mw.settings_manager.global_settings.get_current_tab()
        # get the index of the tab
        if mw.current_tab == "construct":
            index = mw.construct_tab_index
        elif mw.current_tab == "generate":
            index = mw.construct_tab_index
        elif mw.current_tab == "browse":
            index = mw.browse_tab_index
        elif mw.current_tab == "learn":
            index = mw.learn_tab_index
        elif mw.current_tab == "write":
            index = mw.write_tab_index
        mw.fade_manager.fade_to_tab(index)
