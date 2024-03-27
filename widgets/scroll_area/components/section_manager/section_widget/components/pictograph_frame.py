from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QGridLayout
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from ..letterbook_section_widget import LetterBookSectionWidget


class ScrollAreaSectionPictographFrame(QFrame):
    def __init__(self, section) -> None:
        super().__init__()
        self.section = section
        self.spacing = 3
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(self.spacing)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
