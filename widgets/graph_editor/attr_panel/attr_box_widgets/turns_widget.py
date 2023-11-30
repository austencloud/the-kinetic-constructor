from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSpacerItem,
    QSizePolicy,
    QVBoxLayout,
    QFrame,
)
from PyQt6.QtCore import Qt
from utilities.TypeChecking.TypeChecking import Colors
from typing import TYPE_CHECKING
from PyQt6.QtGui import QFont

if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class TurnsWidget(QWidget):
    def __init__(
        self, pictograph: "Pictograph", color: Colors, attr_box: "AttrBox"
    ) -> None:
        super().__init__()
        self.pictograph = pictograph
        self.color = color
        self.attr_box = attr_box
        self.init_ui()

    def create_button(self, text, callback) -> QPushButton:
        button = QPushButton(text, self)
        button.clicked.connect(callback)
        button.setStyleSheet(self.attr_box.get_button_style())
        return button

    def init_ui(self) -> None:
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setFixedHeight(int(self.attr_box.height() * 1 / 6))
        top_layout = QHBoxLayout(self)
        bottom_layout = QHBoxLayout(self)

        turns_label_header_font = QFont("Arial", 12)
        self.turns_label_header = self._create_label("Turns", turns_label_header_font)
        self.turns_label_header.setContentsMargins(0, 0, 0, 0)
        top_layout.addWidget(self.turns_label_header)
        self.turns_label_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turns_label_header.setFixedWidth(int(self.attr_box.attr_box_width))
        self.turns_label_header.setFixedHeight(int(self.height() * 3 / 8))
        top_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.turns_label_header.setFrameShape(QFrame.Shape.Box)
        self.turns_label_header.setLineWidth(1)
        self.turns_label_header.setFrameShadow(QFrame.Shadow.Plain)

        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setContentsMargins(0, 0, 0, 0)
        top_layout.setSpacing(0)
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(0)
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setFixedWidth(int(self.attr_box.width()))

        # Create buttons
        self.subtract_turn_button = self.create_button(
            "-1", self.subtract_turn_callback
        )
        self.subtract_half_turn_button = self.create_button(
            "-0.5", self.subtract_half_turn_callback
        )
        self.add_half_turn_button = self.create_button(
            "+0.5", self.add_half_turn_callback
        )
        self.add_turn_button = self.create_button("+1", self.add_turn_callback)

        self.bottom_widget = QWidget(self)
        self.bottom_widget.setLayout(bottom_layout)
        self.bottom_widget.setStyleSheet("border: 1px solid black;")
        self.bottom_widget.setFixedHeight(int(self.height() * 5 / 8))
        self.bottom_widget.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setContentsMargins(0, 0, 0, 0)

        # Turns label
        self.turns_label = QLabel("0", self)
        self.turns_label.setContentsMargins(0, 0, 0, 0)
        self.turns_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turns_label.setStyleSheet(
            f"font-size: {int(self.bottom_widget.height()* 0.9)}px; font-weight: bold;"
        )
        self.turns_label.setFixedHeight(int(self.height() * 5 / 8))

        # Add widgets to layout
        bottom_layout.addWidget(self.subtract_turn_button)
        bottom_layout.addWidget(self.subtract_half_turn_button)
        bottom_layout.addWidget(self.turns_label)
        bottom_layout.addWidget(self.add_half_turn_button)
        bottom_layout.addWidget(self.add_turn_button)

        self.layout.addLayout(top_layout)

        self.layout.addWidget(self.bottom_widget)

        self.top_layout = top_layout
        self.bottom_layout = bottom_layout

    def _create_label(self, text: str, font: QFont) -> QLabel:
        label = QLabel(text, self)
        label.setFont(font)
        label.setFixedHeight(int(self.width() * 0.2 / 2))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label


    def add_turn_callback(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.add_turn()
            self.attr_box.update_labels(motion)

    def subtract_turn_callback(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.subtract_turn()
            self.attr_box.update_labels(motion)

    def add_half_turn_callback(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.add_half_turn()
            self.attr_box.update_labels(motion)

    def subtract_half_turn_callback(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.subtract_half_turn()
            self.attr_box.update_labels(motion)

    def update_turns_widget_size(self) -> None:
        self.setFixedSize(
            self.attr_box.attr_box_width,
            int(self.attr_box.height() * 1 / 6),
        )
        self.turns_label.setFixedWidth(int(self.attr_box.attr_box_width / 3))
        self.turns_label.setFixedHeight(int(self.height() * 5 / 8))
