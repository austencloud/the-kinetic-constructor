from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QGroupBox, QSizePolicy
from Enums import LetterType
from constants import OPP, SAME
from PyQt6.QtCore import Qt
from ....scroll_area.components.section_manager.section_widget.components.filter_tab.filter_tab import (
    FilterTab,
)
from ....scroll_area.components.section_manager.section_widget.components.section_header import (
    SectionHeader,
)
from ....pictograph.pictograph import Pictograph
from ....turns_box.turns_box_widgets.vtg_dir_button_manager import VtgDirButtonManager
from ....scroll_area.components.section_manager.section_widget.components.pictograph_frame import (
    ScrollAreaSectionPictographFrame,
)

if TYPE_CHECKING:
    from widgets.sequence_builder.components.option_picker.option_picker_scroll_area import (
        OptionPickerScrollArea,
    )



class OptionPickerSectionWidget(QGroupBox):
    SCROLLBAR_WIDTH = 20

    def __init__(
        self, letter_type: LetterType, scroll_area: "OptionPickerScrollArea"
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
        self.setStyleSheet("QGroupBox {border: 1px solid black;}")

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 15, 0, 15)
        self.setup_header()
        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def setup_header(self):
        self.header = SectionHeader(self)
        self.header.clicked.connect(self.toggle_section)
        self.layout.addWidget(self.header)

    def resize_section(self) -> None:
        if self.letter_type in [
            LetterType.Type1,
            LetterType.Type2,
            LetterType.Type3,
        ]:
            self.setMinimumWidth(self.scroll_area.width() - self.SCROLLBAR_WIDTH)
            self.setMaximumWidth(self.scroll_area.width() - self.SCROLLBAR_WIDTH)
        elif self.letter_type in [
            LetterType.Type4,
            LetterType.Type5,
            LetterType.Type6,
        ]:
            self.setMinimumWidth(
                int((self.scroll_area.width() - self.SCROLLBAR_WIDTH) / 3)
            )
            self.setMaximumWidth(
                int((self.scroll_area.width() - self.SCROLLBAR_WIDTH) / 3)
            )

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

    def reset_section(self, index: int) -> None:
        for pictograph in self.pictographs.values():
            for motion in pictograph.motions.values():
                motion.turns_manager.set_turns(0)
            pictograph.updater.update_pictograph()
        for panel in self.filter_tab.panels:
            for box in panel.boxes:
                box.turns_widget.display_manager.update_turns_display("0")
                box.prop_rot_dir_button_manager.hide_prop_rot_dir_buttons()
        self.vtg_dir_button_manager.hide_vtg_dir_buttons()

    def clear_pictographs(self):
        for pictograph_key in list(self.pictographs.keys()):
            pictograph = self.pictographs.pop(pictograph_key)
            pictograph.view.setParent(None)
            pictograph.view.hide()

    def set_size_policy(self, horizontal, vertical):
        size_policy = QSizePolicy(horizontal, vertical)
        self.setSizePolicy(size_policy)
        for pictograph in self.pictographs.values():
            pictograph.view.setSizePolicy(size_policy)

    def adjust_size(self):
        self.resize_section()
        # self.filter_tab.visibility_handler.resize_filter_tab()

    def add_pictograph(self, pictograph: Pictograph):
        """Add a pictograph widget to the section layout."""
        self.pictographs[
            self.scroll_area.pictograph_factory.generate_pictograph_key_from_dict(
                pictograph.get.pictograph_dict()
            )
        ] = pictograph
        self.pictograph_frame.layout.addWidget(pictograph.view)
        pictograph.view.resize_pictograph_view()
        pictograph.view.show()
