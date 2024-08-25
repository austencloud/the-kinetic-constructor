from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QWidget,
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QColor
from typing import TYPE_CHECKING

from data.constants import BLUE, RED
from widgets.factories.button_factory.buttons.letterbook_adjust_turns_button import (
    AdjustTurnsButton,
)

if TYPE_CHECKING:
    from widgets.graph_editor.ori_picker_box.GE_ori_picker_box import (
        GE_OriPickerBox,
    )


class GE_OriPickerHeader(QWidget):
    def __init__(self, turns_box: "GE_OriPickerBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box
        self.graph_editor = self.turns_box.graph_editor
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
        header_label = QLabel(self)
        color = self.turns_box.color
        text = ""

        if color == RED:
            text = "Right"
            font_color = QColor("#ED1C24")
        elif color == BLUE:
            text = "Left"
            font_color = QColor("#2E3192")

        self.header_label_font = QFont("Arial")
        self.header_label_font.setBold(True)
        header_label.setFont(self.header_label_font)
        header_label.setText(text)
        header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_label.setStyleSheet(f"color: {font_color.name()};")
        return header_label

    def resize_ori_picker_header(self) -> None:
        self.setFixedHeight(self.turns_box.height() // 4)
        self._resize_header_label()

    def _resize_header_label(self) -> None:
        font_size = self.graph_editor.width() // 40
        self.header_label_font.setPointSize(font_size)
        self.header_label.setFont(self.header_label_font)
        self.header_label.repaint()
