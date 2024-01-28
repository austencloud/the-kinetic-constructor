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
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)

        self.pictograph_size_adjuster = PictographSizeAdjuster(self)
        self.pictograph_settings = self.pictograph_size_adjuster.create_widget()
        self.layout().addWidget(self.pictograph_settings)

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_settings)
        self.apply_button.setEnabled(False)
        self.layout().addWidget(self.apply_button)

        self.load_initial_settings()

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

    def update_column_count(self, value) -> None:
        self.settings_manager.set_setting("column_count", value)
        self.scroll_area.display_manager.COLUMN_COUNT = value
        self.scroll_area.update_pictographs()
