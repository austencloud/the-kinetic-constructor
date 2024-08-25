from typing import TYPE_CHECKING

from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, OPP, SAME
from widgets.graph_editor.adjustment_panel.turns_box.prop_rot_dir_button_manager import (
    PropRotDirButtonManager,
)
from widgets.graph_editor.adjustment_panel.turns_box.vtg_dir_button_handler import (
    VtgDirButtonManager,
)


from .turns_box_header import TurnsBoxHeader
from .turns_widget.GE_turns_widget import GE_TurnsWidget
from PyQt6.QtWidgets import QFrame, QVBoxLayout

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph
    from widgets.graph_editor.adjustment_panel.GE_adjustment_panel import (
        GE_AdjustmentPanel,
    )


class TurnsBox(QFrame):
    def __init__(
        self,
        adjustment_panel: "GE_AdjustmentPanel",
        pictograph: "Pictograph",
        color: str,
    ) -> None:
        super().__init__(adjustment_panel)
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
        self.vtg_dir_button_manager = VtgDirButtonManager(self)
        self.prop_rot_dir_button_manager = PropRotDirButtonManager(self)
        self.header = TurnsBoxHeader(self)
        self.turns_widget = GE_TurnsWidget(self)

    def _setup_layout(self) -> None:
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.addWidget(self.header)
        layout.addWidget(self.turns_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def update_styles(self) -> None:
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(
            f"#{self.__class__.__name__} {{ border: {self.border_width}px solid {self.color}; background-color: white;}}"
        )

    def resize_turns_box(self) -> None:
        self.header.resize_header()
        self.turns_widget.resize_turns_widget()
        self.update_styles()