from typing import TYPE_CHECKING
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt

from constants import BLUE, RED

if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_start_pos_ori_picker_widget import (
        GE_StartPosOriPickerWidget,
    )


class GE_OriPickerDisplayManager:
    def __init__(self, ori_picker_widget: "GE_StartPosOriPickerWidget") -> None:
        self.ori_picker_widget = ori_picker_widget
        self.ori_picker_box = ori_picker_widget.ori_picker_box
        self.setup_current_orientation_display()

    def setup_current_orientation_display(self) -> None:
        self.ori_display_label = self.ori_picker_widget.ori_display_label
        self.ori_display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ori_display_label.mousePressEvent = (
            self.ori_picker_widget.on_orientation_display_clicked
        )

    def set_label_styles(self) -> None:
        graph_editor_width = self.ori_picker_box.adjustment_panel.graph_editor.width()
        self.ori_display_label.setFixedWidth(graph_editor_width // 5)
        ori_display_width = self.ori_display_label.width()

        ori_display_border = int(ori_display_width / 30)
        border_color = self._get_border_color()

        self.ori_display_label.setStyleSheet(
            f"""
            QLabel {{
                border: {ori_display_border}px solid {border_color};
                background-color: white;

            }}
            """
        )

    def _get_border_color(self) -> str:
        if self.ori_picker_box.color == RED:
            border_color = "#ED1C24"
        elif self.ori_picker_box.color == BLUE:
            border_color = "#2E3192"
        else:
            border_color = "black"
        return border_color

    def set_ori_display_font_size(self) -> None:
        font_size = int(self.ori_picker_box.graph_editor.width() // 30)
        font = QFont("Arial", font_size)
        font.setWeight(QFont.Weight.Bold)
        self.ori_picker_widget.ori_display_label.setFont(font)
