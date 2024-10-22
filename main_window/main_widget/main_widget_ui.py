from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QStackedWidget, QSizePolicy, QWidget

from main_window.main_widget.learn_widget.sequence_tab_container import (
    SequenceTabContainer,
)
from main_window.main_widget.sequence_widget.beat_frame.build_tab_widget import BuildTabWidget
from main_window.main_widget.sequence_widget.beat_frame.generate_tab_widget import GenerateTabWidget
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

    def _setup_components(self):
        self.main_widget.menu_bar_widget = MenuBarWidget(self.main_widget)
        self.main_widget.navigation_widget = NavigationWidget(self.main_widget)
        self.main_widget.sequence_widget = SequenceWidget(self.main_widget)
        self.main_widget.manual_builder = ManualBuilderWidget(self.main_widget)
        self.main_widget.sequence_generator = SequenceGeneratorWidget(self.main_widget)
        self.main_widget.dictionary_widget = DictionaryWidget(self.main_widget)
        self.main_widget.learn_widget = LearnWidget(self.main_widget)

        # Initialize builder_stacked_widget to switch between manual builder and sequence generator
        self.main_widget.builder_stacked_widget = QStackedWidget()
        self.main_widget.builder_stacked_widget.addWidget(self.main_widget.manual_builder)
        self.main_widget.builder_stacked_widget.addWidget(self.main_widget.sequence_generator)

        # Initialize main_stacked_widget to switch between Build/Generate and Dictionary/Learn
        self.main_widget.main_stacked_widget = QStackedWidget()

        # Create Build/Generate Widget
        self.main_widget.build_generate_widget = QWidget()
        self.main_widget.build_generate_layout = QHBoxLayout(self.main_widget.build_generate_widget)
        self.main_widget.build_generate_layout.addWidget(self.main_widget.sequence_widget)
        self.main_widget.build_generate_layout.addWidget(self.main_widget.builder_stacked_widget)
        self.main_widget.build_generate_layout.setStretch(0, 1)
        self.main_widget.build_generate_layout.setStretch(1, 1)
        self.main_widget.build_generate_widget.setLayout(self.main_widget.build_generate_layout)

        # Create Dictionary/Learn Widget
        self.main_widget.dictionary_learn_widget = QStackedWidget()
        self.main_widget.dictionary_learn_widget.addWidget(self.main_widget.dictionary_widget)
        self.main_widget.dictionary_learn_widget.addWidget(self.main_widget.learn_widget)

        # Add Build/Generate Widget and Dictionary/Learn Widget to main_stacked_widget
        self.main_widget.main_stacked_widget.addWidget(self.main_widget.build_generate_widget)  # Index 0
        self.main_widget.main_stacked_widget.addWidget(self.main_widget.dictionary_learn_widget)  # Index 1

    def _setup_layout(self):
        self.main_widget.main_layout = QVBoxLayout(self.main_widget)
        self.main_widget.setLayout(self.main_widget.main_layout)

        # Add navigation and menu bar widgets to the main layout
        self.main_widget.main_layout.addWidget(self.main_widget.navigation_widget)
        self.main_widget.main_layout.addWidget(self.main_widget.menu_bar_widget)

        # Add the main stacked widget to the main layout
        self.main_widget.main_layout.addWidget(self.main_widget.main_stacked_widget)
        self.main_widget.main_stacked_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

    def _setup_indices(self):
        self.main_widget.build_tab_index = 0
        self.main_widget.generate_tab_index = 1
        self.main_widget.dictionary_tab_index = 2
        self.main_widget.learn_tab_index = 3

    def _load_current_tab(self):
        self.main_widget.current_tab = (
            self.main_widget.settings_manager.global_settings.get_current_tab()
        )
        self.main_widget.tabs_handler.update_tab_based_on_settings()
