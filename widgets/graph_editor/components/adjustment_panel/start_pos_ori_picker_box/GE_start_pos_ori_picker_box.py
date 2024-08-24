from typing import TYPE_CHECKING
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, OPP, SAME
from widgets.graph_editor.components.adjustment_panel.ori_picker_widget.GE_start_pos_ori_picker_widget import (
    GE_StartPosOriPickerWidget,
)
from widgets.graph_editor.components.adjustment_panel.start_pos_ori_picker_box.GE_start_pos_ori_picker_header import (
    GE_StartPosOriPickerBoxHeader,
)
from PyQt6.QtWidgets import QFrame, QVBoxLayout

if TYPE_CHECKING:
    from widgets.graph_editor.components.adjustment_panel.GE_adjustment_panel import GE_AdjustmentPanel
    from widgets.pictograph.pictograph import Pictograph


class GE_StartPosOriPickerBox(QFrame):
    def __init__(
        self,
        adjustment_panel: "GE_AdjustmentPanel",
        start_pos: "Pictograph",
        color: str,
    ) -> None:
        super().__init__(adjustment_panel)
        self.setObjectName("GE_StartPosOriPickerBox")
        self.adjustment_panel = adjustment_panel
        self.color = color
        self.start_pos = start_pos
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
        self.header = GE_StartPosOriPickerBoxHeader(self)
        self.ori_picker_widget = GE_StartPosOriPickerWidget(self)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.header, 1)
        self.layout.addWidget(self.ori_picker_widget, 5)
        self.setLayout(self.layout)

    def update_styled_border(self) -> None:
        self.setStyleSheet(
            f"#GE_StartPosOriPickerBox {{ border: {self.border_width}px solid {self.color}; }}"
        )

    def calculate_button_size(self) -> int:
        return int((self.start_pos.view.height() // 8))

    def resize_GE_ori_picker_box(self) -> None:
        self.ori_picker_widget.resize_GE_start_pos_ori_picker_widget()
