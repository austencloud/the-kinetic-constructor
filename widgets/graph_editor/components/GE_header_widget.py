from PyQt6.QtWidgets import QHBoxLayout, QLabel, QWidget, QFrame, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING

from Enums.MotionAttributes import Color
from widgets.factories.button_factory.buttons.adjust_turns_button import (
    AdjustTurnsButton,
)

if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_turns_box import (
        GE_TurnsBox,
    )


class GE_HeaderWidget(QWidget):
    def __init__(self, turns_box: "GE_TurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box: "GE_TurnsBox" = turns_box
        self.header_label = self._setup_header_label()
        self.layout: QVBoxLayout = self._setup_layout()
        self.layout.addWidget(self.header_label)
        self.layout.addWidget(self.create_separator())

    def create_separator(self) -> QFrame:
        separator = QFrame(self)
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Raised)
        separator.setStyleSheet("color: #000000;")
        return separator

    def _setup_layout(self) -> QVBoxLayout:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        return layout

    def _setup_header_label(self) -> QLabel:
        color = self.turns_box.color
        text = ""
        font_color = "#000000"

        if color == Color.RED:
            text = "Right"
            font_color = "#ED1C24"
        elif color == Color.BLUE:
            text = "Left"
            font_color = "#2E3192"

        font_size = self.turns_box.width() // 4
        font_weight = "bold"

        label = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            f"color: {font_color}; font-size: {font_size}px; font-weight: {font_weight};"
        )

        return label

    def create_attr_header_label(
        self, text: str, align: Qt.AlignmentFlag = Qt.AlignmentFlag.AlignCenter
    ) -> QLabel:
        attr_label = QLabel(text, self)
        attr_label.setFont(QFont("Arial"))
        attr_label.setAlignment(align)
        attr_label.setContentsMargins(0, 0, 0, 0)
        return attr_label

    def create_header_frame(self, layout: QHBoxLayout | QVBoxLayout) -> QFrame:
        frame = QFrame(self)
        frame.setLayout(layout)
        return frame

    def create_adjust_turns_button(self, text: str) -> AdjustTurnsButton:
        button = AdjustTurnsButton(self)
        button.setText(text)
        return button
