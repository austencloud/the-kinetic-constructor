from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import pyqtSignal, Qt
from .GE_ori_picker_display_frame import GE_OriPickerDisplayFrame

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..ori_picker_box import OriPickerBox


class GE_OriPickerWidget(QWidget):
    ori_adjusted = pyqtSignal(str)

    def __init__(self, ori_picker_box: "OriPickerBox") -> None:
        super().__init__()
        self.ori_picker_box = ori_picker_box
        self.color = self.ori_picker_box.color

        self.current_orientation_index = 0
        self._setup_components()
        self._setup_layout()

    def _setup_components(self) -> None:
        self.ori_display_frame = GE_OriPickerDisplayFrame(self)
        self.ori_text = self._setup_ori_text()

    def _setup_layout(self) -> None:
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.ori_text, 1)
        layout.addWidget(self.ori_display_frame, 10)

    def _setup_ori_text(self) -> QLabel:
        ori_text = QLabel("Orientation", self)
        ori_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return ori_text

    def resize_ori_picker_widget(self) -> None:
        self.ori_display_frame.resize_ori_display_frame()
        self._resize_orientation_text()

    def _resize_orientation_text(self) -> None:
        ori_label_font_size = self.ori_picker_box.graph_editor.width() // 60
        font = QFont("Cambria", ori_label_font_size, QFont.Weight.Bold)
        font.setUnderline(True)
        self.ori_text.setFont(font)
