from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout

if TYPE_CHECKING:
    from widgets.sequence_builder.components.start_position_picker.start_pos_picker import (
        StartPosPicker,
    )


class StartPosDefaultOriPicker(QWidget):
    def __init__(self, start_pos_picker: "StartPosPicker"):
        super().__init__(start_pos_picker)
        self.start_pos_picker = start_pos_picker
        self.main_widget = start_pos_picker.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager
        self.orientations = ["in", "counter", "out", "clock"]
        self.current_left_orientation_index = 0
        self.current_right_orientation_index = 0
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        left_layout = QHBoxLayout()
        right_layout = QHBoxLayout()

        left_label = QLabel("Left Hand (Blue) Orientation:")
        self.left_orientation_display = QLabel()
        self.left_ccw_button = QPushButton("CCW")
        self.left_ccw_button.clicked.connect(self.rotate_left_ccw)
        self.left_cw_button = QPushButton("CW")
        self.left_cw_button.clicked.connect(self.rotate_left_cw)
        left_layout.addWidget(left_label)
        left_layout.addWidget(self.left_orientation_display)
        left_layout.addWidget(self.left_ccw_button)
        left_layout.addWidget(self.left_cw_button)

        right_label = QLabel("Right Hand (Red) Orientation:")
        self.right_orientation_display = QLabel()
        self.right_ccw_button = QPushButton("CCW")
        self.right_ccw_button.clicked.connect(self.rotate_right_ccw)
        self.right_cw_button = QPushButton("CW")
        self.right_cw_button.clicked.connect(self.rotate_right_cw)
        right_layout.addWidget(right_label)
        right_layout.addWidget(self.right_orientation_display)
        right_layout.addWidget(self.right_ccw_button)
        right_layout.addWidget(self.right_cw_button)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

    def load_default_orientations(self):
        default_left_orientation = self.settings_manager.get_setting(
            "default_left_orientation", "in"
        )
        default_right_orientation = self.settings_manager.get_setting(
            "default_right_orientation", "in"
        )
        self.current_left_orientation_index = self.orientations.index(default_left_orientation)
        self.current_right_orientation_index = self.orientations.index(default_right_orientation)
        self.update_orientation_displays()

    def rotate_left_ccw(self):
        self.current_left_orientation_index = (
            self.current_left_orientation_index - 1
        ) % len(self.orientations)
        self.update_left_orientation()

    def rotate_left_cw(self):
        self.current_left_orientation_index = (
            self.current_left_orientation_index + 1
        ) % len(self.orientations)
        self.update_left_orientation()

    def rotate_right_ccw(self):
        self.current_right_orientation_index = (
            self.current_right_orientation_index - 1
        ) % len(self.orientations)
        self.update_right_orientation()

    def rotate_right_cw(self):
        self.current_right_orientation_index = (
            self.current_right_orientation_index + 1
        ) % len(self.orientations)
        self.update_right_orientation()
        
    def update_left_orientation(self):
        orientation = self.orientations[self.current_left_orientation_index]
        self.left_orientation_display.setText(orientation)
        self.settings_manager.set_setting("default_left_orientation", orientation)
        self.start_pos_picker.start_pos_manager.update_start_pos_pictographs()

    def update_right_orientation(self):
        orientation = self.orientations[self.current_right_orientation_index]
        self.right_orientation_display.setText(orientation)
        self.settings_manager.set_setting("default_right_orientation", orientation)
        self.start_pos_picker.start_pos_manager.update_start_pos_pictographs()

    def update_orientation_displays(self):
        self.left_orientation_display.setText(
            self.orientations[self.current_left_orientation_index]
        )
        self.right_orientation_display.setText(
            self.orientations[self.current_right_orientation_index]
        )