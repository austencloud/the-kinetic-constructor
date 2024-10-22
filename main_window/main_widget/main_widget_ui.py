from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QStackedWidget, QSizePolicy

from main_window.main_widget.learn_widget.sequence_tab_container import (
    SequenceTabContainer,
)
from main_window.menu_bar_widget.menu_bar_widget import MenuBarWidget
from main_window.main_widget.navigation_widget import NavigationWidget
from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget
from main_window.main_widget.sequence_builder.auto_builder.sequence_generator_widget import (
    SequenceGeneratorWidget,
)
from main_window.main_widget.sequence_builder.manual_builder import ManualBuilderWidget
from main_window.main_widget.dictionary_widget.dictionary_widget import DictionaryWidget
from main_window.main_widget.learn_widget.learn_widget import LearnWidget

if TYPE_CHECKING:
    from .main_widget import MainWidget


class MainWidgetUI:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget
        self._setup_components()
        self._setup_layout()
        self._setup_indices()
        self._load_current_tab()

    def _load_current_tab(self):
        self.main_widget.current_tab = (
            self.main_widget.settings_manager.global_settings.get_current_tab()
        )
        self.main_widget.tabs_handler.update_tab_based_on_settings()

    def _setup_components(self):
        self.main_widget.menu_bar_widget = MenuBarWidget(self.main_widget)
        self.main_widget.navigation_widget = NavigationWidget(self.main_widget)
        self.main_widget.sequence_widget = SequenceWidget(self.main_widget)
        self.main_widget.manual_builder = ManualBuilderWidget(self.main_widget)
        self.main_widget.sequence_generator = SequenceGeneratorWidget(self.main_widget)
        self.main_widget.dictionary_widget = DictionaryWidget(self.main_widget)
        self.main_widget.learn_widget = LearnWidget(self.main_widget)

        # Initialize the stacked widget with tabs (build, generate, etc.)
        self.main_widget.stacked_widget = QStackedWidget()
        self.main_widget.stacked_widget.addWidget(self.main_widget.manual_builder)
        self.main_widget.stacked_widget.addWidget(self.main_widget.sequence_generator)
        self.main_widget.stacked_widget.addWidget(self.main_widget.dictionary_widget)
        self.main_widget.stacked_widget.addWidget(self.main_widget.learn_widget)

        # Initialize the container that holds both sequence_widget and stacked_widget
        self.sequence_tab_container = SequenceTabContainer(
            self.main_widget.sequence_widget, self.main_widget.stacked_widget
        )

    def _setup_layout(self):
        self.main_widget.main_layout = QVBoxLayout(self.main_widget)
        self.main_widget.setLayout(self.main_widget.main_layout)

        # Add navigation and menu bar widgets to the main layout
        self.main_widget.main_layout.addWidget(self.main_widget.navigation_widget)
        self.main_widget.main_layout.addWidget(self.main_widget.menu_bar_widget)

        # Add the sequence_tab_container to the main layout
        self.main_widget.main_layout.addWidget(self.sequence_tab_container)

    def _setup_indices(self):
        self.main_widget.build_tab_index = 0
        self.main_widget.generate_tab_index = 1
        self.main_widget.dictionary_tab_index = 2
        self.main_widget.learn_tab_index = 3
