from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QWidget,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING

from data.constants import BLUE, RED
from widgets.factories.button_factory.buttons.letterbook_adjust_turns_button import (
    AdjustTurnsButton,
)

if TYPE_CHECKING:
    from widgets.graph_editor.start_pos_ori_picker_box.GE_start_pos_ori_picker_box import GE_StartPosOriPickerBox


class GE_StartPosOriPickerBoxHeader(QWidget):
    def __init__(self, turns_box: "GE_StartPosOriPickerBox") -> None:
        super().__init__(turns_box)

        self.turns_box = turns_box
        self.separator: QFrame = self.create_separator()
        self.header_label: QLabel = self._setup_header_label()
        self._setup_layout()
        self._add_widgets()

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.top_hbox = QHBoxLayout()
        self.bottom_hbox = QHBoxLayout()
        self.layout.addLayout(self.top_hbox)
        self.layout.addLayout(self.bottom_hbox)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

    def _add_widgets(self) -> None:
        self.top_hbox.addStretch(3)
        self.top_hbox.addStretch(1)
        self.top_hbox.addWidget(self.header_label)
        self.top_hbox.addStretch(1)
        self.top_hbox.addStretch(3)
        self.bottom_hbox.addWidget(self.separator)

    def create_separator(self) -> QFrame:
        separator = QFrame(self)
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Raised)
        separator.setStyleSheet("color: #000000;")
        return separator

    def _setup_header_label(self) -> QLabel:
        color = self.turns_box.color
        text = ""
        font_color = "#000000"

        if color == RED:
            text = "Right"
            font_color = "#ED1C24"
        elif color == BLUE:
            text = "Left"
            font_color = "#2E3192"

        font_size = self.turns_box.width() // 3
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

    def create_header_frame(self, layout: QHBoxLayout | QHBoxLayout) -> QFrame:
        frame = QFrame(self)
        frame.setLayout(layout)
        return frame

    def create_adjust_turns_button(self, text: str) -> AdjustTurnsButton:
        button = AdjustTurnsButton(self)
        button.setText(text)
        return button
