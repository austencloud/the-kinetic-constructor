from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QHBoxLayout, QListWidget, QStackedWidget, QWidget
from PyQt6.QtCore import Qt

from .prop_type_selector import PropTypeSelector
from .glyph_visibility_widget import GlyphVisibilityWidget
from .default_orientation_selector import DefaultOrientationSelector

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget

class PreferencesDialog(QDialog):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget.main_window)
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.settings_manager = main_widget.main_window.settings_manager
        self.setWindowTitle("Preferences")
        self._setup_widgets()
        self._setup_layout()

    def _setup_widgets(self) -> None:
        self.prop_type_selector = PropTypeSelector(self.main_widget)
        self.glyph_visibility_widget = GlyphVisibilityWidget(self.main_window)
        self.default_orientation_selector = DefaultOrientationSelector(self.main_widget)
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_settings)

    def _setup_layout(self) -> None:
        main_layout = QHBoxLayout(self)

        self.sections_list = QListWidget()
        self.sections_list.addItems(["Prop Type", "Glyph Visibility", "Default Orientations"])
        self.sections_list.currentRowChanged.connect(self.change_section)

        self.pages_widget = QStackedWidget()
        self.pages_widget.addWidget(self.prop_type_selector)
        self.pages_widget.addWidget(self.glyph_visibility_widget)
        self.pages_widget.addWidget(self.default_orientation_selector)

        main_layout.addWidget(self.sections_list, 1)
        main_layout.addWidget(self.pages_widget, 3)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(self.apply_button)

        layout = QVBoxLayout()
        layout.addLayout(main_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def change_section(self, index: int) -> None:
        self.pages_widget.setCurrentIndex(index)

    def apply_settings(self) -> None:
        self.prop_type_selector.apply_settings()
        self.glyph_visibility_widget.apply_settings()
        self.default_orientation_selector.apply_settings()
        self.settings_manager.save_settings()
        self.close()

    def load_initial_settings(self) -> None:
        self.prop_type_selector.load_initial_settings()
        self.glyph_visibility_widget.load_initial_settings()
        self.default_orientation_selector.load_initial_settings()