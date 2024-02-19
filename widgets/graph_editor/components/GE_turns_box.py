from typing import TYPE_CHECKING
from Enums.MotionAttributes import Color
from ...turns_panel import GE_AdjustmentPanel

from .GE_header_widget import GE_HeaderWidget
from .GE_turns_widget import GE_TurnsWidget

from PyQt6.QtWidgets import QFrame, QVBoxLayout

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph




class GE_TurnsBox(QFrame):
    def __init__(
        self,
        adjustment_panel: "GE_AdjustmentPanel",
        pictograph: "Pictograph",
        color: Color,
    ) -> None:
        super().__init__(adjustment_panel)
        self.color = color
        self.pictograph = pictograph
        self._setup_widgets()
        self._setup_layout()

    def _setup_widgets(self) -> None:
        self.header_widget = GE_HeaderWidget(self)
        self.turns_widget = GE_TurnsWidget(self)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.header_widget)
        self.layout.addWidget(self.turns_widget)
        self.setLayout(self.layout)

    ### CREATE LABELS ###

    def calculate_button_size(self) -> int:
        return int((self.pictograph.view.height() // 8))

    def resize_GE_turns_box(self) -> None:
        self.setMinimumHeight(self.pictograph.view.height())
