from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QMouseEvent, QFont, QFontMetrics
from PyQt6.QtCore import Qt, pyqtSignal
from typing import TYPE_CHECKING, Literal


from data.constants import RED, BLUE


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

        border_size = max(
            int(required_width / 60), 1
        )  # Ensure border size is at least 1
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
