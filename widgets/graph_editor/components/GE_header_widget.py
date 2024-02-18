from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
)
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING

from widgets.codex.codex_header_widget import CodexHeaderWidget

if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_turns_box import (
        GE_TurnsBox,
    )
from constants import BLUE, HEX_BLUE, HEX_RED, RED


class GE_HeaderWidget(CodexHeaderWidget):
    def __init__(self, turns_box: "GE_TurnsBox") -> None:
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
