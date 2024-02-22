from typing import TYPE_CHECKING
from Enums.MotionAttributes import Color
from constants import CLOCKWISE, COUNTER_CLOCKWISE, OPP, SAME
from widgets.graph_editor.components.GE_ori_picker_widget import (
    GE_StartPosOriPickerWidget,
)
from widgets.graph_editor.components.GE_start_pos_ori_picker_header import (
    GE_StartPosOriPickerHeader,
)
from PyQt6.QtWidgets import QFrame, QVBoxLayout

if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_turns_panel import GE_AdjustmentPanel
    from widgets.pictograph.pictograph import Pictograph


class GE_StartPosOriPickerBox(QFrame):
    def __init__(
        self,
        adjustment_panel: "GE_AdjustmentPanel",
        start_pos: "Pictograph",
        color: Color,
    ) -> None:
        super().__init__(adjustment_panel)
        self.setObjectName("GE_StartPosOriPickerBox")  # Assign a unique object name
        self.adjustment_panel = adjustment_panel
        self.color = color
        self.start_pos = start_pos
        self.graph_editor = self.adjustment_panel.graph_editor

        self.vtg_dir_btn_state: dict[str, bool] = {SAME: False, OPP: False}
        self.prop_rot_dir_btn_state: dict[str, bool] = {
            CLOCKWISE: False,
            COUNTER_CLOCKWISE: False,
        }
        self._setup_widgets()
        self._setup_layout()
        self._set_border_color()

    def _setup_widgets(self) -> None:
        self.header_widget = GE_StartPosOriPickerHeader(self)
        self.ori_picker_widget = GE_StartPosOriPickerWidget(self)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.header_widget, 1)
        self.layout.addWidget(self.ori_picker_widget, 4)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    def _set_border_color(self) -> None:
        border_width = self.width() // 40
        self.setStyleSheet(
            f"#GE_TurnsBox {{ border: {border_width}px solid {self.color.name}; }}"
        )

    def calculate_button_size(self) -> int:
        return int((self.start_pos.view.height() // 8))

    def resize_GE_turns_box(self) -> None:
        self.ori_picker_widget.resize_GE_ori_picker_widget()
        self.header_widget.resize_dir_buttons()
