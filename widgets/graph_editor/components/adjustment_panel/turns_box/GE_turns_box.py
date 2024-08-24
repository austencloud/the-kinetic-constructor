from typing import TYPE_CHECKING

from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, OPP, SAME
from widgets.graph_editor.components.adjustment_panel.turns_box.GE_prop_rot_dir_button_manager import GE_PropRotDirButtonManager
from widgets.graph_editor.components.adjustment_panel.turns_box.GE_vtg_dir_button_handler import GE_VtgDirButtonManager

from .GE_turns_box_header import GE_TurnsBoxHeader
from .turns_widget.GE_turns_widget import GE_TurnsWidget
from PyQt6.QtWidgets import QFrame, QVBoxLayout

if TYPE_CHECKING:
    from widgets.graph_editor.components.adjustment_panel.GE_adjustment_panel import GE_AdjustmentPanel
    from widgets.pictograph.pictograph import Pictograph


class GE_TurnsBox(QFrame):
    def __init__(
        self, adjustment_panel: "GE_AdjustmentPanel", pictograph: "Pictograph", color: str
    ) -> None:
        super().__init__(adjustment_panel)
        self.setObjectName("GE_TurnsBox")
        self.adjustment_panel = adjustment_panel
        self.color = color
        self.pictograph = pictograph
        self.graph_editor = self.adjustment_panel.graph_editor
        self.border_width = self.graph_editor.width() // 100

        self.vtg_dir_btn_state: dict[str, bool] = {SAME: False, OPP: False}
        self.prop_rot_dir_btn_state: dict[str, bool] = {
            CLOCKWISE: False,
            COUNTER_CLOCKWISE: False,
        }
        self._setup_widgets()
        self._setup_layout()

    def _setup_widgets(self) -> None:
        self.vtg_dir_button_manager = GE_VtgDirButtonManager(self)
        self.prop_rot_dir_button_manager = GE_PropRotDirButtonManager(self)
        self.header = GE_TurnsBoxHeader(self)
        self.turns_widget = GE_TurnsWidget(self)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.header)
        self.layout.addWidget(self.turns_widget)
        self.setLayout(self.layout)

    def update_styled_border(self) -> None:
        self.setStyleSheet(
            f"#GE_TurnsBox {{ border: {self.border_width}px solid {self.color};}}"
        )

    def resize_GE_turns_box(self) -> None:
        self.setMaximumWidth(
            int(
                (
                    self.graph_editor.width()
                    - self.graph_editor.GE_pictograph_view.width()
                )
                / 2
            )
        )
        self.header.resize_GE_turns_box_header()
        self.turns_widget.resize_GE_turns_widget()
