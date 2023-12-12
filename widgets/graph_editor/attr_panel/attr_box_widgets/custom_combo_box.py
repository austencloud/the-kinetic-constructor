from typing import TYPE_CHECKING
from settings.string_constants import (
    ICON_DIR,
)
from PyQt6.QtGui import QResizeEvent

if TYPE_CHECKING:
    pass
from PyQt6.QtWidgets import QComboBox


class CustomComboBox(QComboBox):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self.combobox_border = 2

    def sizeHint(self):
        # Ensure size hint accounts for border width
        size = super().sizeHint()
        border_adjustment = (
            2 * self.combobox_border
        )  # Adjust the 2 if border width is different
        size.setWidth(size.width() + border_adjustment)
        size.setHeight(size.height() + border_adjustment)
        return size

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)

