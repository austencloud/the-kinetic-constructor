from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QStackedWidget
from .construct_tab.construct_tab import ConstructTab
from .generate_tab.generate_tab import GenerateTab
from .write_tab.write_tab import WriteTab
from .browse_tab.browse_tab import BrowseTab
from .learn_tab.learn_tab import LearnTab
from .main_background_widget.main_background_widget import MainBackgroundWidget
from .main_widget_fade_manager import MainWidgetFadeManager
from ..settings_manager.global_settings.main_widget_font_color_updater import (
    MainWidgetFontColorUpdater,
)
from ..menu_bar_widget.menu_bar_widget import MenuBarWidget
from .navigation_widget import NavigationWidget
from .sequence_widget.sequence_widget import SequenceWidget


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
        self.mw.content_stack = QStackedWidget()  # <--- NEW

        self.mw.stack_fade_manager = MainWidgetFadeManager(self.mw)
        self.mw.background_widget = MainBackgroundWidget(self.mw)
        self.mw.background_widget.lower()
        self.mw.font_color_updater = MainWidgetFontColorUpdater(self.mw)

        splash = self.splash_screen
        splash.updater.update_progress("MenuBarWidget")
        self.mw.menu_bar_widget = MenuBarWidget(self.mw)
        splash.updater.update_progress("NavigationWidget")
        self.mw.navigation_widget = NavigationWidget(self.mw)
        splash.updater.update_progress("SequenceWidget")
        self.mw.sequence_widget = SequenceWidget(self.mw)
        splash.updater.update_progress("ConstructTab")
        self.mw.construct_tab = ConstructTab(self.mw)
        splash.updater.update_progress("GenerateTab")
        self.mw.generate_tab = GenerateTab(self.mw)
        splash.updater.update_progress("BrowseTab")
        self.mw.browse_tab = BrowseTab(self.mw)
        splash.updater.update_progress("LearnTab")
        self.mw.learn_tab = LearnTab(self.mw)
        splash.updater.update_progress("WriteTab")
        self.mw.write_tab = WriteTab(self.mw)
        splash.updater.update_progress("Finalizing")

        self.mw.content_stack.addWidget(self.mw.construct_tab)
        self.mw.content_stack.addWidget(self.mw.generate_tab)
        self.mw.content_stack.addWidget(self.mw.browse_tab)
        self.mw.content_stack.addWidget(self.mw.learn_tab)
        self.mw.content_stack.addWidget(self.mw.write_tab)

    def _setup_layout(self):
        self.mw.main_layout = QVBoxLayout(self.mw)
        self.mw.main_layout.setContentsMargins(0, 0, 0, 0)
        self.mw.main_layout.setSpacing(0)
        self.mw.setLayout(self.mw.main_layout)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.mw.menu_bar_widget, 1)
        top_layout.addWidget(self.mw.navigation_widget, 1)

        content_layout = QHBoxLayout()
        content_layout.addWidget(self.mw.sequence_widget, 1)
        content_layout.addWidget(self.mw.content_stack, 1)

        self.mw.main_layout.addLayout(top_layout)
        self.mw.main_layout.addLayout(content_layout)

    def _setup_indices(self):
        self.mw.construct_tab_index = 0
        self.mw.generate_tab_index = 1
        self.mw.browse_tab_index = 2
        self.mw.learn_tab_index = 3
        self.mw.write_tab_index = 4

    def load_current_tab(self):
        mw = self.mw
        mw.current_tab = mw.settings_manager.global_settings.get_current_tab()
        mw.tabs_handler.update_tab_based_on_settings()
