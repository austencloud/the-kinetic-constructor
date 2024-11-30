from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QStackedWidget, QWidget

from main_window.main_widget.act_tab.act_tab import ActTab
from ..menu_bar_widget.menu_bar_widget import MenuBarWidget
from .navigation_widget import NavigationWidget
from .sequence_widget.sequence_widget import SequenceWidget
from .sequence_builder.auto_builder.sequence_generator_widget import (
    SequenceGeneratorWidget,
)
from .sequence_builder.manual_builder import ManualBuilder
from .dictionary_widget.dictionary_widget import DictionaryWidget
from .learn_widget.learn_widget import LearnWidget

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
        splash = self.splash_screen
        splash.updater.update_progress("MenuBarWidget")
        mw.menu_bar_widget = MenuBarWidget(mw)
        splash.updater.update_progress("NavigationWidget")
        mw.navigation_widget = NavigationWidget(mw)
        splash.updater.update_progress("SequenceWidget")
        mw.sequence_widget = SequenceWidget(mw)
        splash.updater.update_progress("ManualBuilderWidget")
        mw.manual_builder = ManualBuilder(mw)
        splash.updater.update_progress("SequenceGeneratorWidget")
        mw.sequence_generator = SequenceGeneratorWidget(mw)
        splash.updater.update_progress("DictionaryWidget")
        mw.dictionary_widget = DictionaryWidget(mw)
        splash.updater.update_progress("LearnWidget")
        mw.learn_widget = LearnWidget(mw)
        splash.updater.update_progress("ActTab")
        mw.act_tab = ActTab(mw)
        splash.updater.update_progress("Finalizing")

        # Create stacked widgets and primary layouts
        mw.right_stacked_widget = QStackedWidget()
        mw.right_stacked_widget.addWidget(mw.manual_builder)
        mw.right_stacked_widget.addWidget(mw.sequence_generator)

        mw.build_generate_widget = QWidget()
        build_generate_layout = QHBoxLayout(mw.build_generate_widget)
        build_generate_layout.addWidget(mw.sequence_widget)
        build_generate_layout.addWidget(mw.right_stacked_widget)

        # Set equal stretch factors
        build_generate_layout.setStretch(0, 1)  # Index 0 corresponds to sequence_widget
        build_generate_layout.setStretch(1, 1)  # Index 1 corresponds to builder_stacked_widget

        mw.dictionary_learn_widget = QStackedWidget()
        mw.dictionary_learn_widget.addWidget(mw.dictionary_widget)
        mw.dictionary_learn_widget.addWidget(mw.learn_widget)

        mw.main_stacked_widget = QStackedWidget()
        mw.main_stacked_widget.addWidget(mw.build_generate_widget)
        mw.main_stacked_widget.addWidget(mw.dictionary_learn_widget)
        mw.main_stacked_widget.addWidget(mw.act_tab)

    def _setup_layout(self):
        mw = self.main_widget

        mw.main_layout = QVBoxLayout(mw)
        mw.main_layout.setContentsMargins(0, 0, 0, 0)
        mw.main_layout.setSpacing(0)
        mw.setLayout(mw.main_layout)

        top_layout = QHBoxLayout()
        top_layout.addWidget(mw.menu_bar_widget, 1)
        top_layout.addWidget(mw.navigation_widget, 1)

        mw.main_layout.addLayout(top_layout)
        mw.main_layout.addWidget(mw.main_stacked_widget)

    def _setup_indices(self):
        self.main_widget.build_tab_index = 0
        self.main_widget.generate_tab_index = 1
        self.main_widget.dictionary_tab_index = 2
        self.main_widget.learn_tab_index = 3
        self.main_widget.act_tab_index = 4

    def on_splitter_moved(self):
        self.main_widget.manual_builder.resize_manual_builder()

    def load_current_tab(self):
        mw = self.main_widget
        mw.current_tab = mw.settings_manager.global_settings.get_current_tab()
        mw.tabs_handler.update_tab_based_on_settings()
