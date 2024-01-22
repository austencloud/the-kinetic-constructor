# Import necessary components
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
)
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from widgets.scroll_area.scroll_area_section import ScrollAreaSection


class ScrollAreaSectionPictographFrame(QFrame):
    def __init__(self, scroll_area_section: "ScrollAreaSection") -> None:
        super().__init__()
        self.section = scroll_area_section
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # self.layout.setColumnStretch(0, 1)  # Stretch the first column
        # self.layout.setColumnStretch(2, 1)  # Stretch the last column
