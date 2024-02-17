from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
)
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING, Callable

from widgets.sequence_widget.header_widget import HeaderWidget

if TYPE_CHECKING:
    from widgets.graph_editor_tab.graph_editor_attr_box import (
        GraphEditorTurnsBox,
    )
from constants import BLUE, CCW_HANDPATH, CW_HANDPATH, HEX_BLUE, HEX_RED, ICON_DIR, RED


class GraphEditorHeaderWidget(HeaderWidget):
    def __init__(self, turns_box: "GraphEditorTurnsBox") -> None:
        super().__init__(turns_box)
        self.header_label = self._setup_header_label()

        self._setup_layout()

    def _setup_layout(self) -> None:
        super()._setup_layout()
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.setSpacing(0)
        header_layout.addStretch(1)
        # header_layout.addWidget(self.header_label)
        header_layout.addStretch(1)
        self.separator = self.create_separator()
        # self.layout.addLayout(header_layout)
        # self.layout.addWidget(self.separator)

    def _setup_header_label(self) -> QLabel:
        text = "Left" if self.turns_box.color == BLUE else "Right"
        color_hex = HEX_RED if self.turns_box.color == RED else HEX_BLUE
        label = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"color: {color_hex}; font-weight: bold;")
        return label
