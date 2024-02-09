from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QGridLayout
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from ..section_widget import SectionWidget


class ScrollAreaSectionPictographFrame(QFrame):
    def __init__(self, section: "SectionWidget") -> None:
        super().__init__()
        self.section = section
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def add_pictograph(self, pictograph) -> None:
        self.layout.addWidget(pictograph, 0, 0)
        self.section.resize_section()
        self.section.scroll_area.resize_sequence_builder_scroll_area()