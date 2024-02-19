from typing import TYPE_CHECKING
from Enums.MotionAttributes import Color
from .GE_header_widget import GE_HeaderWidget
from .GE_turns_widget import GE_TurnsWidget
from PyQt6.QtWidgets import QFrame, QVBoxLayout

if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_turns_panel import GE_TurnsPanel
    from widgets.pictograph.pictograph import Pictograph


class GE_TurnsBox(QFrame):
    def __init__(
        self,
        turns_panel: "GE_TurnsPanel",
        pictograph: "Pictograph",
        color: Color,
    ) -> None:
        super().__init__(turns_panel)
        self.turns_panel = turns_panel
        self.color = color
        self.pictograph = pictograph
        self.graph_editor = self.turns_panel.graph_editor
        self._setup_widgets()
        self._setup_layout()

    def _setup_widgets(self) -> None:
        self.header_widget = GE_HeaderWidget(self)
        self.turns_widget = GE_TurnsWidget(self)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.header_widget)
        self.layout.addWidget(self.turns_widget)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def calculate_button_size(self) -> int:
        return int((self.pictograph.view.height() // 8))

    def resize_GE_turns_box(self) -> None:
        # self.setMinimumHeight(self.pictograph.view.height())
        self.turns_widget.resize_GE_turns_widget()
