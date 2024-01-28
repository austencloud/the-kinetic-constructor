from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QGroupBox, QFormLayout, QSlider
from PyQt6.QtCore import Qt
from widgets.clickable_slider import ClickableSlider

if TYPE_CHECKING:
    from widgets.menu_bar.preferences_dialog import PreferencesDialog


class PictographSizeAdjuster:
    MAX_COLUMN_COUNT = 8
    MIN_COLUMN_COUNT = 3

    def __init__(self, preferences_dialog: "PreferencesDialog") -> None:
        self.preferences_dialog = preferences_dialog
        self._setup_size_slider()

    def _setup_size_slider(self) -> None:
        self.size_slider = ClickableSlider(Qt.Orientation.Horizontal)
        self.size_slider.setMinimum(1)
        self.size_slider.setMaximum(self.MAX_COLUMN_COUNT - self.MIN_COLUMN_COUNT + 1)
        self.size_slider.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.size_slider.setTickInterval(1)
        self.size_slider.setPageStep(1)
        self.size_slider.valueChanged.connect(self.slider_value_changed)

    def create_widget(self) -> QGroupBox:
        group_box = QGroupBox()
        layout = QFormLayout()
        layout.addRow(QLabel("Pictograph size:"), self.size_slider)
        group_box.setLayout(layout)
        return group_box

    def slider_value_changed(self, value) -> None:
        inverted_value = self.MAX_COLUMN_COUNT - (value - 1)
        column_count = max(
            self.MIN_COLUMN_COUNT, min(inverted_value, self.MAX_COLUMN_COUNT)
        )
        self.preferences_dialog.scroll_area.display_manager.COLUMN_COUNT = column_count
        self.preferences_dialog.scroll_area.update_pictographs()
        self.preferences_dialog.apply_button.setEnabled(True)
