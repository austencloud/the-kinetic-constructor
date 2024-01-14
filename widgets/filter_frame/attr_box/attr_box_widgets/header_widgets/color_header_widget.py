from PyQt6.QtWidgets import QHBoxLayout, QLabel
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING
from utilities.TypeChecking.TypeChecking import Colors

from .base_header_widget import BaseHeaderWidget

if TYPE_CHECKING:
    from widgets.filter_frame.attr_box.color_attr_box import ColorAttrBox
from constants import (
    BLUE,
    RED,
)


class ColorHeaderWidget(BaseHeaderWidget):
    def __init__(self, attr_box: "ColorAttrBox", color: Colors) -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.color = color
        self.header_label = self._setup_header_label()
        self.separator = self.create_separator()
        self._setup_layout()

    def _setup_layout(self) -> None:
        super()._setup_layout()
        header_layout = QHBoxLayout()
        header_layout.addStretch(1)
        header_layout.addWidget(self.header_label)
        header_layout.addStretch(1)
        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.separator)

    def _setup_dash_static_layout(self) -> None:
        super()._setup_layout()
        header_layout = QHBoxLayout()
        header_layout.addStretch(1)
        header_layout.addWidget(self.header_label)
        header_layout.addStretch(1)
        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.separator)

    def _setup_header_label(self) -> QLabel:
        text = ""
        font_color = ""
        font_size = 30
        font_weight = "bold"

        if self.color == BLUE:
            text = "Left"
            font_color = "#2E3192"
        elif self.color == RED:
            text = "Right"
            font_color = "#ED1C24"

        label = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            f"color: {font_color}; font-size: {font_size}px; font-weight: {font_weight};"
        )
        return label
