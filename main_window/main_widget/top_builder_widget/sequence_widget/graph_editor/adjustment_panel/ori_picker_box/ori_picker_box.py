from typing import TYPE_CHECKING
from data.constants import CLOCKWISE, COUNTER_CLOCKWISE, OPP, SAME
from PyQt6.QtWidgets import QFrame, QVBoxLayout

from .ori_picker_widget.ori_picker_widget import OriPickerWidget
from .ori_picker_header import GE_OriPickerHeader

if TYPE_CHECKING:
    from ..beat_adjustment_panel import BeatAdjustmentPanel
    from widgets.base_widgets.pictograph.base_pictograph import BasePictograph


class OriPickerBox(QFrame):
    def __init__(
        self,
        adjustment_panel: "BeatAdjustmentPanel",
        start_pos: "BasePictograph",
        color: str,
    ) -> None:
        super().__init__(adjustment_panel)
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
        self.header = GE_OriPickerHeader(self)
        self.ori_picker_widget = OriPickerWidget(self)

    def _setup_layout(self) -> None:
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.addWidget(self.header)
        layout.addWidget(self.ori_picker_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def update_styles(self) -> None:
        self.setObjectName(self.__class__.__name__)
        self.setStyleSheet(
            f"#{self.__class__.__name__} {{ border: {self.border_width}px solid {self.color}; background-color: white;}}"
        )

    def resize_ori_picker_box(self) -> None:
        self.header.resize_header()
        self.ori_picker_widget.resize_ori_picker_widget()
        self.update_styles()
