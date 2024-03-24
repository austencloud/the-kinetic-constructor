from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QGroupBox,
)

if TYPE_CHECKING:
    from widgets.sequence_builder.advanced_start_pos_picker.advanced_start_pos_picker import (
        AdvancedStartPosPicker,
    )


class AdvancedStartPosPickerDefaultOriWidget(QWidget):
    def __init__(self, advanced_start_pos_picker: "AdvancedStartPosPicker"):
        super().__init__(advanced_start_pos_picker)
        self.advanced_start_pos_picker = advanced_start_pos_picker
        self.main_widget = advanced_start_pos_picker.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager
        self.orientations = ["in", "counter", "out", "clock"]
        self.init_ui()

    def init_ui(self):
        self.group_box = QGroupBox("Default Orientation Picker")
        self.group_box.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.group_box_layout = QVBoxLayout()

        self.setup_orientation_buttons("Left Hand (Blue)", self.set_left_orientation)
        self.setup_orientation_buttons("Right Hand (Red)", self.set_right_orientation)

        self.group_box.setLayout(self.group_box_layout)
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.group_box, alignment=Qt.AlignmentFlag.AlignCenter)

    def setup_orientation_buttons(self, hand_label_text: str, orientation_setter):
        layout = QHBoxLayout()
        hand_label = QLabel(hand_label_text)
        layout.addWidget(hand_label)

        for orientation in self.orientations:
            button = QPushButton(orientation)
            button.clicked.connect(
                lambda checked, ori=orientation: orientation_setter(ori)
            )
            layout.addWidget(button)

        self.group_box_layout.addLayout(layout)

    def set_left_orientation(self, ori: str) -> None:
        self.settings_manager.set_setting("default_left_orientation", ori)
        self.advanced_start_pos_picker.advanced_start_pos_manager.update_left_default_ori(
            ori
        )

    def set_right_orientation(self, ori: str) -> None:
        self.settings_manager.set_setting("default_right_orientation", ori)
        self.advanced_start_pos_picker.advanced_start_pos_manager.update_right_default_ori(
            ori
        )
