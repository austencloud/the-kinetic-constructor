from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QComboBox
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class DefaultOrientationSelector(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.settings_manager = main_widget.main_window.settings_manager
        self.orientations = ["in", "counter", "out", "clock"]
        self._setup_widgets()
        self._setup_layout()

    def _setup_widgets(self) -> None:
        self.left_label = QLabel("Default Left Hand Orientation:")
        self.left_combo_box = QComboBox()
        self.left_combo_box.addItems(self.orientations)

        self.right_label = QLabel("Default Right Hand Orientation:")
        self.right_combo_box = QComboBox()
        self.right_combo_box.addItems(self.orientations)

    def _setup_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addWidget(self.left_label)
        layout.addWidget(self.left_combo_box)
        layout.addSpacing(10)
        layout.addWidget(self.right_label)
        layout.addWidget(self.right_combo_box)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(layout)

    def load_initial_settings(self) -> None:
        default_left_orientation = self.settings_manager.get_setting(
            "default_left_orientation", "in"
        )
        default_right_orientation = self.settings_manager.get_setting(
            "default_right_orientation", "in"
        )
        self.left_combo_box.setCurrentText(default_left_orientation)
        self.right_combo_box.setCurrentText(default_right_orientation)

    def apply_settings(self) -> None:
        default_left_orientation = self.left_combo_box.currentText()
        default_right_orientation = self.right_combo_box.currentText()
        self.settings_manager.set_setting(
            "default_left_orientation", default_left_orientation
        )
        self.settings_manager.set_setting(
            "default_right_orientation", default_right_orientation
        )
