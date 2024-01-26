# Import necessary components
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
)
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from widgets.scroll_area.components.section_manager.section_widget.section_widget import (
        SectionWidget,
    )


class ScrollAreaSectionPictographFrame(QFrame):
    def __init__(self, scroll_area_section: "SectionWidget") -> None:
        super().__init__()
        self.section = scroll_area_section
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
