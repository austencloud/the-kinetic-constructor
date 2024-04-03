from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QGroupBox, QSizePolicy
from Enums.Enums import LetterType

from Enums.letters import Letter
from constants import DASH, NO_ROT, OPP, SAME, STATIC
from .components.turns_tab.turns_tab import TurnsTab
from .components.codex_section_header import CodexSectionHeader
from .....pictograph.pictograph import Pictograph
from .....codex.codex_letter_button_frame.components.codex_vtg_dir_button_manager import (
    CodexVtgDirButtonManager,
)
from .components.pictograph_frame import ScrollAreaSectionPictographFrame

if TYPE_CHECKING:
    pass

    from ....codex_scroll_area import CodexScrollArea


class CodexSectionWidget(QGroupBox):
    SCROLLBAR_WIDTH = 20

    def __init__(self, letter_type: LetterType, scroll_area: "CodexScrollArea") -> None:
        super().__init__(None)
        self.scroll_area = scroll_area
        self.letter_type = letter_type
        self.vtg_dir_btn_state: dict[str, bool] = {SAME: False, OPP: False}
        self.turns_tab: TurnsTab = None

    def setup_components(self) -> None:
        self.vtg_dir_button_manager = CodexVtgDirButtonManager(self)
        self._setup_layout()
        self.pictograph_frame = ScrollAreaSectionPictographFrame(self)
        self.pictographs: dict[Letter, Pictograph] = {}
        self.layout.addWidget(self.pictograph_frame)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(3)
        self.setContentsMargins(0, 0, 0, 0)
        self.setup_header()

    def setup_header(self):
        self.header = CodexSectionHeader(self)
        self.header.clicked.connect(self.toggle_section)
        self.layout.addWidget(self.header)

    def resize_section(self) -> None:
        self.setMinimumWidth(self.scroll_area.width() - self.SCROLLBAR_WIDTH)
        self.setMaximumWidth(self.scroll_area.width() - self.SCROLLBAR_WIDTH)
        self.header.resize_section_header()
        self.turns_tab.visibility_handler.resize_turns_tab()

    def toggle_section(self) -> None:
        self.layout.setEnabled(False)
        is_visible = not self.pictograph_frame.isVisible()
        self.pictograph_frame.setVisible(is_visible)
        if self.turns_tab:
            self.turns_tab.setVisible(is_visible)

        self.header.toggle_dropdown_arrow(not is_visible)

        if is_visible:
            if self.vtg_dir_btn_state[SAME] or self.vtg_dir_btn_state[OPP]:
                self.vtg_dir_button_manager.show_vtg_dir_buttons()
        else:
            self.vtg_dir_button_manager.hide_vtg_dir_buttons()
        self.layout.setEnabled(True)
        self.layout.activate()

    def reset_section(self, index: int) -> None:

        # Need to fix this so the dash arrows don't show up the wrong way

        for pictograph in self.pictographs.values():
            for motion in pictograph.motions.values():
                motion.turns_manager.set_turns(0)
                if motion.motion_type in [DASH, STATIC]:
                    motion.prop_rot_dir = NO_ROT

            pictograph.updater.update_pictograph()
        for panel in self.turns_tab.panels:
            for box in panel.boxes:
                box.turns_widget.display_manager.update_turns_display("0")
                box.prop_rot_dir_button_manager.hide_prop_rot_dir_buttons()
        self.vtg_dir_button_manager.hide_vtg_dir_buttons()

    def clear_pictographs(self):
        for pictograph_key in list(self.pictographs.keys()):
            pictograph = self.pictographs.pop(pictograph_key)
            pictograph.view.setParent(None)

    def set_size_policy(self, horizontal, vertical):
        size_policy = QSizePolicy(horizontal, vertical)
        self.setSizePolicy(size_policy)
        for pictograph in self.pictographs.values():
            pictograph.view.setSizePolicy(size_policy)

    def adjust_size(self):
        self.resize_section()
        self.turns_tab.visibility_handler.resize_turns_tab()
