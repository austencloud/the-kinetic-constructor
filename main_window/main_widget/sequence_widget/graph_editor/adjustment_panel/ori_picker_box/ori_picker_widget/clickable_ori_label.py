from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QMouseEvent, QFont, QFontMetrics
from PyQt6.QtCore import Qt, pyqtSignal
from typing import TYPE_CHECKING, Literal

from PyQt6.QtCore import QPoint
from data.constants import RED, BLUE, IN, OUT, CLOCK, COUNTER
from main_window.main_widget.sequence_widget.graph_editor.adjustment_panel.ori_picker_box.ori_picker_widget.ori_selection_dialog import (
    OriSelectionDialog,
)


if TYPE_CHECKING:
    from .ori_picker_widget import OriPickerWidget


class ClickableOriLabel(QLabel):
    leftClicked = pyqtSignal()
    rightClicked = pyqtSignal()

    def __init__(self, ori_picker_widget: "OriPickerWidget"):
        super().__init__(ori_picker_widget)
        self.ori_picker_widget = ori_picker_widget
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.leftClicked.connect(self._on_orientation_display_clicked)
        self.rightClicked.connect(self._on_orientation_label_right_clicked)
        self.dialog = OriSelectionDialog(self.ori_picker_widget)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.leftClicked.emit()
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightClicked.emit()

    def set_orientation(self, orientation):
        self.setText(orientation)

    def resize_clickable_ori_label(self):
        font_size = self.ori_picker_widget.ori_picker_box.graph_editor.width() // 30
        font = QFont("Arial", font_size, QFont.Weight.Bold)
        self.setFont(font)

        font_metrics = QFontMetrics(font)
        text_width = font_metrics.horizontalAdvance("counter")
        padding = font_metrics.horizontalAdvance("  ")

        required_width = text_width + padding
        self.setMinimumWidth(required_width)

        border_size = max(int(required_width / 60), 1)
        border_color = self._get_border_color(self.ori_picker_widget.color)
        self.setStyleSheet(
            f"QLabel {{ border: {border_size}px solid {border_color}; background-color: white; }}"
        )

    def _get_border_color(
        self, color
    ) -> Literal["#ED1C24"] | Literal["#2E3192"] | Literal["black"]:
        if color == RED:
            return "#ED1C24"
        elif color == BLUE:
            return "#2E3192"
        else:
            return "black"

    def _on_orientation_display_clicked(self):
        self.dialog.move(self.mapToGlobal(QPoint(0, 0)))
        if self.dialog.exec():
            new_orientation = self.dialog.selected_orientation
            self.ori_picker_widget.ori_setter.set_orientation(new_orientation)

    def _on_orientation_label_right_clicked(self):
        current_ori = self.ori_picker_widget.orientations[
            self.ori_picker_widget.current_orientation_index
        ]
        if current_ori in [IN, OUT]:
            new_ori = OUT if current_ori == IN else IN
        elif current_ori in [CLOCK, COUNTER]:
            new_ori = COUNTER if current_ori == CLOCK else CLOCK
        else:
            new_ori = current_ori
        self.ori_picker_widget.ori_setter.set_orientation(new_ori)

    def resizeEvent(self, event):
        self.resize_clickable_ori_label()
        super().resizeEvent(event)
