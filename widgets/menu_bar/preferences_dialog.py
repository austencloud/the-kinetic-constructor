from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from .pictograph_size_adjuster import PictographSizeAdjuster

if TYPE_CHECKING:
    from main import MainWindow


class PreferencesDialog(QDialog):
    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__(main_window)
        self.main_window = main_window
        self.settings_manager = main_window.settings_manager
        self.scroll_area = (
            self.main_window.main_widget.main_tab_widget.codex.scroll_area
        )
        self.setWindowTitle("Preferences")
        self.pictograph_size_adjuster = PictographSizeAdjuster(self)
        self._setup_apply_button()
        self._setup_layout()
        self.load_initial_settings()

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.addWidget(self.pictograph_size_adjuster)
        self.layout.addWidget(self.apply_button)

    def _setup_apply_button(self) -> None:
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_settings)
        self.apply_button.setEnabled(False)

    def load_initial_settings(self) -> None:
        initial_size_setting = self.settings_manager.get_setting("pictograph_size")
        self.pictograph_size_adjuster.size_slider.setValue(initial_size_setting)

    def apply_settings(self) -> None:
        self.settings_manager.set_setting(
            "pictograph_size", self.pictograph_size_adjuster.size_slider.value()
        )
        self.settings_manager.save_settings()
        self.apply_button.setEnabled(False)
        self.close()
