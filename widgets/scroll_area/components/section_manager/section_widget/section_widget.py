from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from utilities.TypeChecking.TypeChecking import LetterTypes
from .components.filter_tab import FilterTab
from .components.pictograph_frame import ScrollAreaSectionPictographFrame
from .components.type_label import ScrollAreaSectionTypeLabel

if TYPE_CHECKING:
    from ....scroll_area import ScrollArea


class SectionWidget(QWidget):
    SCROLLBAR_WIDTH = 25

    def __init__(self, letter_type: LetterTypes, scroll_area: "ScrollArea") -> None:
        super().__init__(scroll_area)
        self.scroll_area = scroll_area
        self.letter_type = letter_type

        # Components
        self.type_label = ScrollAreaSectionTypeLabel(self)
        self.filter_tab: FilterTab = None
        self.pictograph_frame = ScrollAreaSectionPictographFrame(self)
        
        self._setup_layout()

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.type_label)
        self.layout.addWidget(self.pictograph_frame)

    def resize_section(self) -> None:
        self.setMinimumWidth(self.scroll_area.width() - self.SCROLLBAR_WIDTH)
        self.filter_tab.resize_filter_tab()
