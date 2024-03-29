from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QGroupBox, QSizePolicy
from Enums.Enums import LetterType
from constants import OPP, SAME
from PyQt6.QtCore import Qt

from widgets.scroll_area.components.section_manager.section_widget.components.option_picker_section_header import (
    OptionPickerSectionHeader,
)
from ....scroll_area.components.section_manager.section_widget.components.turns_tab.turns_tab import (
    TurnsTab,
)
from ....pictograph.pictograph import Pictograph
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
        self.turns_tab: TurnsTab = None

        # remove the default frame styles
        

    def setup_components(self) -> None:
        self._setup_layout()
        self.pictograph_frame = ScrollAreaSectionPictographFrame(self)
        self.pictographs: dict[str, Pictograph] = {}
        self.layout.addWidget(self.pictograph_frame)
        self.pictograph_frame.setStyleSheet("QFrame {border: none;}")  # Add this line to remove the default frame styles
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 15, 0, 0)
        self.setup_header()
        # self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def setup_header(self) -> None:
        self.header = OptionPickerSectionHeader(self)
        self.header.clicked.connect(self.toggle_section)
        self.layout.addWidget(self.header)

    def toggle_section(self) -> None:
        is_visible = not self.pictograph_frame.isVisible()
        self.pictograph_frame.setVisible(is_visible)
        if self.turns_tab:
            self.turns_tab.setVisible(is_visible)
        self.header.toggle_dropdown_arrow(not is_visible)

    def reset_section(self, index: int) -> None:
        for pictograph in self.pictographs.values():
            for motion in pictograph.motions.values():
                motion.turns_manager.set_turns(0)
            pictograph.updater.update_pictograph()
        for panel in self.turns_tab.panels:
            for box in panel.boxes:
                box.turns_widget.display_manager.update_turns_display("0")
                box.prop_rot_dir_button_manager.hide_prop_rot_dir_buttons()

    def clear_pictographs(self):
        for pictograph_key in list(self.pictographs.keys()):
            pictograph = self.pictographs.pop(pictograph_key)
            pictograph.view.setParent(None)
            pictograph.view.hide()

    def set_size_policy(self, horizontal, vertical) -> None:
        size_policy = QSizePolicy(horizontal, vertical)
        self.setSizePolicy(size_policy)
        for pictograph in self.pictographs.values():
            pictograph.view.setSizePolicy(size_policy)

    def add_pictograph(self, pictograph: Pictograph) -> None:
        """Add a pictograph widget to the section layout."""
        self.pictographs[
            self.scroll_area.main_widget.pictograph_key_generator.generate_pictograph_key(
                pictograph.pictograph_dict
            )
        ] = pictograph
        self.pictograph_frame.layout.addWidget(pictograph.view)
        pictograph.view.resize_pictograph_view()
        pictograph.view.show()

    def resize_option_picker_section_widget(self) -> None:
        section_width = int((self.scroll_area.width()))
        if self.letter_type in [LetterType.Type1, LetterType.Type2, LetterType.Type3]:
            self.setMinimumWidth(section_width)
            self.setMaximumWidth(section_width)
        elif self.letter_type in [LetterType.Type4, LetterType.Type5, LetterType.Type6]:
            self.setMinimumWidth(int(section_width / 3))
            self.setMaximumWidth(int(section_width / 3))
