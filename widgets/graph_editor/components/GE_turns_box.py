from typing import TYPE_CHECKING
from Enums.MotionAttributes import Color
from objects.motion.motion import Motion
from .GE_motion_types_widget import GE_MotionTypeWidget
from ...turns_panel import GE_AdjustmentPanel
from ...factories.button_factory.buttons.adjust_turns_button import AdjustTurnsButton

from .GE_header_widget import GE_HeaderWidget
from .GE_turns_widget import GE_TurnsWidget

from PyQt6.QtWidgets import QFrame

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


from PyQt6.QtGui import QFont


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
        # add black borders
        self.setStyleSheet("border: 1px solid black;")

    def _setup_widgets(self) -> None:
        self.header_widget = GE_HeaderWidget(self)
        self.turns_widget = GE_TurnsWidget(self)

    ### CREATE LABELS ###

    def calculate_button_size(self) -> int:
        return int((self.pictograph.view.height() // 2 // 4) * 1)

    def resize_GE_turns_box(self) -> None:
        self.setMinimumHeight(self.pictograph.view.height())
