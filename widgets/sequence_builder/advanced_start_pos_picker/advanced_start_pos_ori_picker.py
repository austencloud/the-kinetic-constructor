from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt6.QtGui import QFont

if TYPE_CHECKING:
    from widgets.sequence_builder.advanced_start_pos_picker.advanced_start_pos_picker import (
        AdvancedStartPosPicker,
    )


class AdvancedStartPosOriPicker(QWidget):
    def __init__(self, advanced_start_pos_picker: "AdvancedStartPosPicker") -> None:
        super().__init__(advanced_start_pos_picker)
        self.advanced_start_pos_picker = advanced_start_pos_picker
        self.main_widget = advanced_start_pos_picker.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager
        self.left_buttons: list[QPushButton] = []
        self.right_buttons: list[QPushButton] = []
        self.init_ui()

    def init_ui(self):
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setSpacing(0)

        self.red_header = self.setup_orientation_buttons(
            "Left", self.set_left_orientation, "blue"
        )
        self.blue_header = self.setup_orientation_buttons(
            "Right", self.set_right_orientation, "red"
        )

        self.header_labels: list[QLabel] = [self.red_header, self.blue_header]

    def setup_orientation_buttons(
        self, hand_label_text: str, orientation_setter, color: str
    ) -> QLabel:
        layout = QVBoxLayout()
        header = QLabel(hand_label_text)
        header.setStyleSheet(f"color: {color}; font-weight: bold;")
        layout.addWidget(
            header,
            alignment=Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignHCenter,
        )
        # create a label to be a line and add it between the header and the buttons
        line = QLabel()
        line.setFixedHeight(4)
        line.setStyleSheet(f"background-color: {color};")
        layout.addWidget(line)
        layout.setSpacing(5)

        row1_layout = QHBoxLayout()
        row2_layout = QHBoxLayout()

        for orientation in ["in", "out"]:
            button = QPushButton(orientation)
            if hand_label_text == "Left":
                self.left_buttons.append(button)
            else:
                self.right_buttons.append(button)

            button.setStyleSheet(
                "padding: 4px; margin: 2px; background-color: rgba(255, 255, 255, 0.5);"
            )
            # add a cursor change on mouseover
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.clicked.connect(
                lambda checked, ori=orientation: orientation_setter(ori)
            )
            row1_layout.addWidget(button)

        for orientation in ["counter", "clock"]:
            button = QPushButton(orientation)
            if hand_label_text == "Left":
                self.left_buttons.append(button)
            else:
                self.right_buttons.append(button)

            button.setStyleSheet(
                "padding: 4px; margin: 2px; background-color: rgba(255, 255, 255, 0.5);"
            )
            button.setCursor(Qt.CursorShape.PointingHandCursor)

            button.clicked.connect(
                lambda checked, ori=orientation: orientation_setter(ori)
            )
            row2_layout.addWidget(button)

        layout.addLayout(row1_layout)
        layout.addLayout(row2_layout)

        self.main_layout.addLayout(layout)
        return header

    def set_left_orientation(self, ori: str) -> None:
        self.advanced_start_pos_picker.advanced_start_pos_manager.update_left_default_ori(
            ori
        )

    def set_right_orientation(self, ori: str) -> None:
        self.advanced_start_pos_picker.advanced_start_pos_manager.update_right_default_ori(
            ori
        )

    def resize_default_ori_picker(self) -> None:
        width = self.advanced_start_pos_picker.sequence_builder.width()
        header_size = width // 30
        for header in self.header_labels:
            header.setFont(QFont("Arial", header_size, QFont.Weight.Bold))
        self.setMinimumWidth(width)

        for button in self.left_buttons + self.right_buttons:
            button.setFixedWidth(width // 6)
            button.setFont(QFont("Arial", width // 40))
