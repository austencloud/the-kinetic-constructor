from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QStackedWidget, QSplitter
from PyQt6.QtCore import Qt
from main_window.main_widget.construct_tab.construct_tab import ConstructTab
from main_window.main_widget.generate_tab.generate_tab import GenerateTab
from main_window.main_widget.write_tab.write_tab import WriteTab
from main_window.main_widget.browse_tab.browse_tab import BrowseTab
from main_window.main_widget.learn_tab.learn_tab import LearnTab
from main_window.main_widget.main_background_widget import MainBackgroundWidget
from main_window.main_widget.tab_fade_manager import TabFadeManager
from main_window.settings_manager.global_settings.main_widget_font_color_updater import (
    MainWidgetFontColorUpdater,
)
from ..menu_bar_widget.menu_bar_widget import MenuBarWidget
from .navigation_widget import NavigationWidget
from .sequence_widget.sequence_widget import SequenceWidget


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
        mw.content_stack = QStackedWidget()  # <--- NEW

        mw.fade_manager = TabFadeManager(mw)
        mw.background_widget = MainBackgroundWidget(mw)
        mw.background_widget.lower()
        mw.font_color_updater = MainWidgetFontColorUpdater(mw)

        splash = self.splash_screen
        splash.updater.update_progress("MenuBarWidget")
        mw.menu_bar_widget = MenuBarWidget(mw)
        splash.updater.update_progress("NavigationWidget")
        mw.navigation_widget = NavigationWidget(mw)
        splash.updater.update_progress("SequenceWidget")
        mw.sequence_widget = SequenceWidget(mw)
        splash.updater.update_progress("ConstructTab")
        mw.construct_tab = ConstructTab(mw)
        splash.updater.update_progress("GenerateTab")
        mw.generate_tab = GenerateTab(mw)
        splash.updater.update_progress("BrowseTab")
        mw.brwose_tab = BrowseTab(mw)
        splash.updater.update_progress("LearnTab")
        mw.learn_tab = LearnTab(mw)
        splash.updater.update_progress("WriteTab")
        mw.write_tab = WriteTab(mw)
        splash.updater.update_progress("Finalizing")

        mw.content_stack.addWidget(mw.construct_tab)  # index 0: Construct
        mw.content_stack.addWidget(mw.generate_tab)  # index 1: Generate
        mw.content_stack.addWidget(mw.brwose_tab)  # index 2: Browse
        mw.content_stack.addWidget(mw.learn_tab)  # index 3: Learn
        mw.content_stack.addWidget(mw.write_tab)  # index 4: Write

    def _setup_layout(self):
        mw = self.main_widget

        mw.main_layout = QVBoxLayout(mw)
        mw.main_layout.setContentsMargins(0, 0, 0, 0)
        mw.main_layout.setSpacing(0)
        mw.setLayout(mw.main_layout)

        top_layout = QHBoxLayout()
        top_layout.addWidget(mw.menu_bar_widget, 1)
        top_layout.addWidget(mw.navigation_widget, 1)

        content_splitter = QSplitter()
        content_splitter.addWidget(mw.sequence_widget)
        content_splitter.addWidget(mw.content_stack)
        mw.main_layout.addLayout(top_layout)
        mw.main_layout.addWidget(content_splitter)

    def _setup_indices(self):
        self.main_widget.build_tab_index = 0
        self.main_widget.generate_tab_index = 1
        self.main_widget.dictionary_tab_index = 2
        self.main_widget.learn_tab_index = 3
        self.main_widget.act_tab_index = 4

    def load_current_tab(self):
        mw = self.main_widget
        mw.current_tab = mw.settings_manager.global_settings.get_current_tab()
        mw.tabs_handler.update_tab_based_on_settings()
