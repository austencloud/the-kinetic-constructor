from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QStackedWidget, QWidget

from main_window.main_widget.background_widget import BackgroundWidget
from main_window.main_widget.browse_tab.browse_tab import BrowseTab
from main_window.main_widget.build_tab.build_tab import BuildTab
from main_window.main_widget.fade_manager import FadeManager
from main_window.main_widget.learn_tab.learn_widget import LearnTab
from main_window.main_widget.main_widget_background_handler import (
    MainWidgetBackgroundHandler,
)
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
        self.mw = main_widget
        self.splash_screen = main_widget.splash_screen
        self._setup_components()
        self._setup_layout()
        self._setup_indices()

    def _setup_components(self):
        self.mw.main_stacked_widget = QStackedWidget()
        self.mw.background_handler = MainWidgetBackgroundHandler(self.mw)
        self.mw.font_color_updater = MainWidgetFontColorUpdater(self.mw)
        self.mw.menu_bar_widget = MenuBarWidget(self.mw)
        self.mw.navigation_widget = NavigationWidget(self.mw)
        
        self.mw.build_tab = BuildTab(self.mw)
        self.mw.browse_tab = BrowseTab(self.mw)
        self.mw.learn_tab = LearnTab(self.mw)
        self.mw.write_tab = WriteTab(self.mw)

        self.mw.main_stacked_widget.addWidget(self.mw.build_tab)
        self.mw.main_stacked_widget.addWidget(self.mw.browse_tab)
        self.mw.main_stacked_widget.addWidget(self.mw.learn_tab)
        self.mw.main_stacked_widget.addWidget(self.mw.write_tab)

        self.mw.fade_manager = FadeManager(self.mw)
        self.mw.background_widget = BackgroundWidget(self.mw)

    def _setup_layout(self):
        self.mw.main_layout = QVBoxLayout(self.mw)
        self.mw.main_layout.setContentsMargins(0, 0, 0, 0)
        self.mw.main_layout.setSpacing(0)
        self.mw.setLayout(self.mw.main_layout)

        self.mw.main_layout.addWidget(self.mw.background_widget)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.mw.menu_bar_widget)
        top_layout.addWidget(self.mw.navigation_widget)

        self.mw.content_container = QWidget()
        self.mw.content_layout = QVBoxLayout(self.mw.content_container)
        self.mw.content_layout.setContentsMargins(0, 0, 0, 0)
        self.mw.content_layout.setSpacing(0)
        self.mw.content_container.setLayout(self.mw.content_layout)

        self.mw.content_layout.addLayout(top_layout)
        self.mw.content_layout.addWidget(self.mw.main_stacked_widget)

        self.mw.main_layout.addWidget(self.mw.content_container)

    def _setup_indices(self):
        self.mw.build_tab_index = 0
        self.mw.browse_tab_index = 1
        self.mw.learn_tab_index = 2
        self.mw.write_tab_index = 3

    def load_current_tab(self):
        self.mw.current_tab = self.mw.settings_manager.global_settings.get_current_tab()
        if self.mw.current_tab == "construct":
            index = self.mw.build_tab_index
        elif self.mw.current_tab == "generate":
            index = self.mw.build_tab_index
        elif self.mw.current_tab == "browse":
            index = self.mw.browse_tab_index
        elif self.mw.current_tab == "learn":
            index = self.mw.learn_tab_index
        elif self.mw.current_tab == "write":
            index = self.mw.write_tab_index
        self.mw.fade_manager.fade_to_tabs(index)
