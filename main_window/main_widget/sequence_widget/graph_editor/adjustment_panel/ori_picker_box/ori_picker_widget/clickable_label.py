from PyQt6.QtWidgets import (
    QLabel,
)
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtCore import Qt, pyqtSignal
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .ori_picker_widget import OriPickerWidget


class ClickableOriLabel(QLabel):
    leftClicked = pyqtSignal()
    rightClicked = pyqtSignal()

    def __init__(self, ori_picker_widget: "OriPickerWidget"):
        super().__init__(ori_picker_widget)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self.leftClicked.emit()
        elif event.button() == Qt.MouseButton.RightButton:
            self.rightClicked.emit()
