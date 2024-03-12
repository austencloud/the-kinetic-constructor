from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
    QCheckBox,
)
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

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
        self.init_ui()

    def init_ui(self):
        self.collapsible_group_box = QGroupBox("Default Orientation Picker")
        self.collapsible_group_box.setCheckable(True)
        self.collapsible_group_box.setChecked(False)

        # Center the title
        self.collapsible_group_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Group box layout
        self.group_box_layout = QVBoxLayout()

        # Left orientation selector
        self.left_layout = QHBoxLayout()
        left_label = QLabel("Left Hand (Blue) Orientation:")
        self.left_orientation_display = QLabel()
        self.left_ccw_button = QPushButton("CCW")
        self.left_ccw_button.clicked.connect(self.rotate_left_ccw)
        self.left_cw_button = QPushButton("CW")
        self.left_cw_button.clicked.connect(self.rotate_left_cw)
        self.left_layout.addWidget(left_label)
        self.left_layout.addWidget(self.left_orientation_display)
        self.left_layout.addWidget(self.left_ccw_button)
        self.left_layout.addWidget(self.left_cw_button)

        # Right orientation selector
        self.right_layout = QHBoxLayout()
        right_label = QLabel("Right Hand (Red) Orientation:")
        self.right_orientation_display = QLabel()
        self.right_ccw_button = QPushButton("CCW")
        self.right_ccw_button.clicked.connect(self.rotate_right_ccw)
        self.right_cw_button = QPushButton("CW")
        self.right_cw_button.clicked.connect(self.rotate_right_cw)
        self.right_layout.addWidget(right_label)
        self.right_layout.addWidget(self.right_orientation_display)
        self.right_layout.addWidget(self.right_ccw_button)
        self.right_layout.addWidget(self.right_cw_button)

        # Add to group box layout
        self.group_box_layout.addLayout(self.left_layout)
        self.group_box_layout.addLayout(self.right_layout)

        # Set the layout for group box
        self.collapsible_group_box.setLayout(self.group_box_layout)

        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(
            self.collapsible_group_box, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Connect the toggled signal to the handler function
        self.collapsible_group_box.toggled.connect(self.handle_collapsed)

    def handle_collapsed(self, checked):
        if checked:
            self.group_box_layout.show()  # Show the contents
        else:
            self.group_box_layout.hide()  # Hide the contents

    def load_default_orientations(self):
        default_left_orientation = self.settings_manager.get_setting(
            "default_left_orientation", "in"
        )
        default_right_orientation = self.settings_manager.get_setting(
            "default_right_orientation", "in"
        )
        self.current_left_orientation_index = self.orientations.index(
            default_left_orientation
        )
        self.current_right_orientation_index = self.orientations.index(
            default_right_orientation
        )
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
