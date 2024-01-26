from typing import TYPE_CHECKING, Dict
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from constants import OPP, SAME
from utilities.TypeChecking.TypeChecking import LetterTypes
from .....pictograph.pictograph import Pictograph
from .....turns_box.turns_box_widgets.vtg_dir_button_manager import VtgDirButtonManager
from .components.filter_tab import FilterTab
from .components.pictograph_frame import ScrollAreaSectionPictographFrame
from .components.type_label import SectionTypeLabel

if TYPE_CHECKING:
    from ....scroll_area import ScrollArea
from PyQt6.QtWidgets import QGroupBox


class SectionWidget(QGroupBox):
    SCROLLBAR_WIDTH = 20

    def __init__(self, letter_type: LetterTypes, scroll_area: "ScrollArea") -> None:
        super().__init__(None)
        self.scroll_area = scroll_area
        self.letter_type = letter_type
        self.vtg_dir_btn_state: Dict[str, bool] = {SAME: False, OPP: False}
        self.filter_tab: FilterTab = None
        self.type_label = SectionTypeLabel(self)
        self.type_label.clicked.connect(self.toggle_section)
        self._setup_layout()

    def setup_components(self) -> None:
        self.pictograph_frame = ScrollAreaSectionPictographFrame(self)
        self.vtg_dir_button_manager = VtgDirButtonManager(self)
        self.pictographs: Dict[str, Pictograph] = {}
        self.layout.addWidget(self.pictograph_frame)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.header_layout = self._setup_header_layout()
        self.layout.addLayout(self.header_layout)

    def _setup_header_layout(self) -> QHBoxLayout:
        header_layout = QHBoxLayout()
        header_layout.addStretch(2)
        header_layout.addWidget(self.type_label)
        header_layout.addStretch(1)
        header_layout.addWidget(self.type_label.arrow_label)
        header_layout.addStretch(2)
        return header_layout

    def resize_section(self) -> None:
        self.setMinimumWidth(self.scroll_area.width() - self.SCROLLBAR_WIDTH)
        self.setMaximumWidth(self.scroll_area.width() - self.SCROLLBAR_WIDTH)
        self.type_label.setMinimumHeight(self.width() // 20)
        self.type_label.setMaximumHeight(self.width() // 20)
        self.filter_tab.resize_filter_tab()

    def toggle_section(self) -> None:
        is_visible = not self.pictograph_frame.isVisible()
        self.pictograph_frame.setVisible(is_visible)
        if self.filter_tab:
            self.filter_tab.setVisible(is_visible)
        self.type_label.set_styled_text(self.letter_type)
        self.type_label.toggle_dropdown_arrow(not is_visible)
