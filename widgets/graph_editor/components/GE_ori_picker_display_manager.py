from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from constants import RED

if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_start_pos_ori_picker_widget import (
        GE_StartPosOriPickerWidget,
    )


class GE_OriPickerDisplayManager:
    def __init__(self, ori_picker_widget: "GE_StartPosOriPickerWidget"):
        self.ori_picker_widget = ori_picker_widget
        self.setup_current_orientation_display()

    def setup_current_orientation_display(self):
        self.ori_picker_widget.current_ori_display = QLabel(
            self.ori_picker_widget.orientations[
                self.ori_picker_widget.current_orientation_index
            ],
            self.ori_picker_widget,
        )
        self.ori_picker_widget.current_ori_display.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.ori_picker_widget.current_ori_display.mousePressEvent = (
            self.ori_picker_widget.on_orientation_display_clicked
        )
        self.set_label_styles(self.ori_picker_widget.current_ori_display)

    def set_label_styles(self, current_ori_display: QLabel):
        color = self.ori_picker_widget.color
        border_color = "#ED1C24" if color == RED else "#2E3192"
        current_ori_display.setStyleSheet(
            f"""
            QLabel {{
                border: 2px solid {border_color};
                border-radius: 10px;
                padding: 5px;
                background-color: white;
            }}
        """
        )

    def resize_current_orientation_display(self):
        font_size = int(
            self.ori_picker_widget.ori_picker_box.graph_editor.width() // 40
        )
        font = QFont("Arial", font_size)  # Adjust font size as needed
        font.setWeight(QFont.Weight.Bold)
        self.ori_picker_widget.current_ori_display.setFont(font)
        # limit the width of the ori display to half the width of the ori picker bo
        self.ori_picker_widget.current_ori_display.setMaximumWidth(
            self.ori_picker_widget.ori_picker_box.width() // 2
        )