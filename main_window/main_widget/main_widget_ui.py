from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QStackedWidget, QSizePolicy

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
        self._ensure_equal_size()
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

    def _setup_layout(self):
        self.main_widget.main_layout = QVBoxLayout(self.main_widget)
        
        self.main_widget.stacked_widget = QStackedWidget()
        self.main_widget.content_layout = QHBoxLayout()

        self.main_widget.setLayout(self.main_widget.main_layout)
        self.main_widget.main_layout.addWidget(self.main_widget.navigation_widget)
        self.main_widget.main_layout.addWidget(self.main_widget.menu_bar_widget)
        self.main_widget.main_layout.addLayout(self.main_widget.content_layout)

        self.main_widget.stacked_widget.addWidget(self.main_widget.manual_builder)
        self.main_widget.stacked_widget.addWidget(self.main_widget.sequence_generator)
        self.main_widget.stacked_widget.addWidget(self.main_widget.dictionary_widget)
        self.main_widget.stacked_widget.addWidget(self.main_widget.learn_widget)
        self.main_widget.content_layout.addWidget(self.main_widget.sequence_widget)
        self.main_widget.content_layout.addWidget(self.main_widget.stacked_widget)

    def _ensure_equal_size(self):
        self.main_widget.content_layout.setStretch(0, 1)  # sequence_widget
        self.main_widget.content_layout.setStretch(1, 1)  # stacked_widget
        self.main_widget.sequence_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        self.main_widget.stacked_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )

    def _setup_indices(self):
        self.main_widget.build_tab_index = 0
        self.main_widget.generate_tab_index = 1
        self.main_widget.dictionary_tab_index = 2
        self.main_widget.learn_tab_index = 3
