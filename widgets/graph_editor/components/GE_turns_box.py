from typing import TYPE_CHECKING
from Enums.MotionAttributes import Color
from constants import CLOCKWISE, COUNTER_CLOCKWISE, OPP, SAME
from widgets.graph_editor.components.GE_prop_rot_dir_button_manager import (
    GE_PropRotDirButtonManager,
)
from widgets.graph_editor.components.GE_vtg_dir_button_handler import (
    GE_VtgDirButtonManager,
)
from .GE_turns_box_header import GE_TurnsBoxHeader
from .GE_turns_widget import GE_TurnsWidget
from PyQt6.QtWidgets import QFrame, QVBoxLayout

if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_adjustment_panel import GE_AdjustmentPanel
    from widgets.pictograph.pictograph import Pictograph


class GE_TurnsBox(QFrame):
    def __init__(
        self,
        turns_panel: "GE_AdjustmentPanel",
        pictograph: "Pictograph",
        color: Color,
    ) -> None:
        super().__init__(turns_panel)
        self.setObjectName("GE_TurnsBox")  # Assign a unique object name
        self.turns_panel = turns_panel
        self.color = color
        self.pictograph = pictograph
        self.graph_editor = self.turns_panel.graph_editor

        self.vtg_dir_btn_state: dict[str, bool] = {SAME: False, OPP: False}
        self.prop_rot_dir_btn_state: dict[str, bool] = {
            CLOCKWISE: False,
            COUNTER_CLOCKWISE: False,
        }
        self._setup_widgets()
        self._setup_layout()
        self._set_border_color()

    def _setup_widgets(self) -> None:
        self.vtg_dir_button_manager = GE_VtgDirButtonManager(self)
        self.prop_rot_dir_button_manager = GE_PropRotDirButtonManager(self)
        self.header_widget = GE_TurnsBoxHeader(self)
        self.turns_widget = GE_TurnsWidget(self)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.header_widget, 1)
        self.layout.addWidget(self.turns_widget, 3)
        # self.layout.addStretch(1)
        self.setLayout(self.layout)

    def _set_border_color(self) -> None:
        border_width = self.width() // 40
        self.setStyleSheet(
            f"#GE_TurnsBox {{ border: {border_width}px solid {self.color.name}; }}"
        )

    def resize_GE_turns_box(self) -> None:
        self.setMinimumWidth(
            int(
                (
                    self.graph_editor.width()
                    - self.graph_editor.GE_pictograph_view.width()
                )
                / 2
            )
        )
        self.turns_widget.resize_GE_turns_widget()
