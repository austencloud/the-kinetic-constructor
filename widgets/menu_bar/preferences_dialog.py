from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt

from .pictograph_size_adjuster import PictographSizeAdjuster

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class PreferencesDialog(QDialog):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget.main_window)
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.settings_manager = main_widget.main_window.settings_manager
        self.codex_scroll_area = self.main_widget.main_tab_widget.codex.scroll_area
        self.pictograph_size_adjuster = PictographSizeAdjuster(self)
        self.setWindowTitle("Preferences")
        self._setup_apply_button()


    def setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.pictograph_size_adjuster)
        self.layout.addWidget(self.main_window.main_widget.prop_type_selector)
        self.layout.addWidget(self.apply_button)

    def _setup_apply_button(self) -> None:
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_settings)
        self.apply_button.setEnabled(False)

    def apply_settings(self) -> None:
        self.settings_manager.set_setting(
            "pictograph_size", self.pictograph_size_adjuster.size_slider.value()
        )
        self.settings_manager.save_settings()
        self.settings_manager.apply_settings()
        self.apply_button.setEnabled(False)
        self.close()

    def load_initial_settings(self) -> None:
        self.pictograph_size_adjuster.load_initial_settings()
        self.main_window.main_widget.prop_type_selector.load_initial_settings()
