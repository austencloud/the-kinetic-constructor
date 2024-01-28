# In PreferencesDialog.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QSpinBox,
    QPushButton,
    QGroupBox,
    QHBoxLayout,
    QFormLayout,
    QSizePolicy,
    QSlider,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from widgets.clickable_slider import ClickableSlider

if TYPE_CHECKING:
    from main import MainWindow


class PreferencesDialog(QDialog):
    MAX_COLUMN_COUNT = 8
    MIN_COLUMN_COUNT = 3

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

        # Pictograph Settings Group
        pictograph_settings_group = QGroupBox("Pictograph Settings")
        pictograph_settings_layout = QFormLayout()
        pictograph_settings_group.setLayout(pictograph_settings_layout)

        # Slider for pictograph size
        self.size_slider = ClickableSlider(Qt.Orientation.Horizontal)
        self.size_slider.setMinimum(1)
        self.size_slider.setMaximum(self.MAX_COLUMN_COUNT - self.MIN_COLUMN_COUNT + 1)
        self.size_slider.setTickPosition(QSlider.TickPosition.TicksBelow)  # Set tick marks below the slider
        self.size_slider.setTickInterval(1)  # Set tick interval to 1
        self.size_slider.setPageStep(1)  # This ensures the slider moves one step at a time when the area beside the slider is clicked
        self.size_slider.valueChanged.connect(self.slider_value_changed)
        pictograph_settings_layout.addRow(QLabel("Pictograph size:"), self.size_slider)

        self.layout().addWidget(pictograph_settings_group)

        # Apply Button
        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_settings)
        self.apply_button.setEnabled(False)
        self.layout().addWidget(self.apply_button)

        self.load_initial_settings()

    def load_initial_settings(self):
        initial_size_setting = self.settings_manager.get_setting("pictograph_size")
        self.size_slider.setValue(initial_size_setting)

    def slider_value_changed(self, value):
        inverted_value = self.MAX_COLUMN_COUNT - (value - 1)
        column_count = max(
            self.MIN_COLUMN_COUNT, min(inverted_value, self.MAX_COLUMN_COUNT)
        )
        self.scroll_area.display_manager.COLUMN_COUNT = column_count
        self.scroll_area.update_pictographs()
        self.apply_button.setEnabled(True)

    def apply_settings(self):
        self.settings_manager.set_setting("pictograph_size", self.size_slider.value())
        self.settings_manager.save_settings()
        self.apply_button.setEnabled(False)
        self.close()

    def update_column_count(self, value) -> None:
        self.settings_manager.set_setting("column_count", value)
        self.scroll_area.display_manager.COLUMN_COUNT = value
        self.scroll_area.update_pictographs()
