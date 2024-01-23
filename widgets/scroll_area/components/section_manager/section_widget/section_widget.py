from typing import TYPE_CHECKING, Dict
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QSizePolicy
from constants import OPP, SAME
from utilities.TypeChecking.TypeChecking import LetterTypes, Letters
from widgets.pictograph.pictograph import Pictograph
from widgets.turns_box.turns_box_widgets.rot_dir_button_manager import (
    RotDirButtonManager,
)
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
        self.rot_dir_button_manager = RotDirButtonManager(self)
        self.pictographs: Dict[str, Pictograph]  = {}
        
    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)

        # Header layout with type label
        self.header_layout = QHBoxLayout()
        self.header_layout.addStretch(1)
        self.header_layout.addWidget(self.type_label)
        self.header_layout.addStretch(1)

        self.layout.addLayout(self.header_layout)
        self.layout.addWidget(self.pictograph_frame)

    def resize_section(self) -> None:
        self.setMinimumWidth(self.scroll_area.width() - self.SCROLLBAR_WIDTH)
        self.filter_tab.resize_filter_tab()
