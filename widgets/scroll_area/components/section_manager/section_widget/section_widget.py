from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QGroupBox
from constants import OPP, SAME
from utilities.TypeChecking.TypeChecking import LetterTypes
from .components.filter_tab.filter_tab import FilterTab
from .components.section_header import SectionHeader
from .....pictograph.pictograph import Pictograph
from .....turns_box.turns_box_widgets.vtg_dir_button_manager import VtgDirButtonManager
from .components.pictograph_frame import ScrollAreaSectionPictographFrame

if TYPE_CHECKING:
    from ....scroll_area import CodexScrollArea


class SectionWidget(QGroupBox):
    SCROLLBAR_WIDTH = 20

    def __init__(
        self, letter_type: LetterTypes, scroll_area: "CodexScrollArea"
    ) -> None:
        super().__init__(None)
        self.scroll_area = scroll_area
        self.letter_type = letter_type
        self.vtg_dir_btn_state: dict[str, bool] = {SAME: False, OPP: False}
        self.filter_tab: FilterTab = None

    def setup_components(self) -> None:
        self.vtg_dir_button_manager = VtgDirButtonManager(self)
        self._setup_layout()
        self.pictograph_frame = ScrollAreaSectionPictographFrame(self)
        self.pictographs: dict[str, Pictograph] = {}
        self.layout.addWidget(self.pictograph_frame)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.header = SectionHeader(self)
        self.header.clicked.connect(self.toggle_section)
        self.layout.addWidget(self.header)

    def resize_section(self) -> None:
        self.setMinimumWidth(self.scroll_area.width() - self.SCROLLBAR_WIDTH)
        self.setMaximumWidth(self.scroll_area.width() - self.SCROLLBAR_WIDTH)

        self.header.type_label.setMinimumHeight(self.width() // 20)
        self.header.type_label.setMaximumHeight(self.width() // 20)
        self.filter_tab.visibility_handler.resize_filter_tab()

    def toggle_section(self) -> None:
        self.layout.setEnabled(False)
        is_visible = not self.pictograph_frame.isVisible()
        self.pictograph_frame.setVisible(is_visible)
        if self.filter_tab:
            self.filter_tab.setVisible(is_visible)

        self.header.toggle_dropdown_arrow(not is_visible)

        if is_visible:
            if self.vtg_dir_btn_state[SAME] or self.vtg_dir_btn_state[OPP]:
                self.vtg_dir_button_manager.show_vtg_dir_buttons()
        else:
            self.vtg_dir_button_manager.hide_vtg_dir_buttons()
        self.layout.setEnabled(True)
        self.layout.activate()
