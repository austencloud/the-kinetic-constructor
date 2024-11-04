from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QGroupBox, QSizePolicy
from Enums.Enums import LetterType
from base_widgets.base_pictograph.base_pictograph import BasePictograph
from data.constants import OPP, SAME
from PyQt6.QtCore import Qt
from ...option_picker_section_header import OptionPickerSectionHeader
from .option_picker_pictograph_frame import OptionPickerPictographFrame

if TYPE_CHECKING:
    from ...option_picker_scroll_area import OptionPickerScrollArea


class OptionPickerSectionWidget(QGroupBox):
    SCROLLBAR_WIDTH = 20

    def __init__(
        self, letter_type: LetterType, scroll_area: "OptionPickerScrollArea"
    ) -> None:
        super().__init__(None)
        self.scroll_area = scroll_area
        self.letter_type = letter_type
        self.vtg_dir_btn_state: dict[str, bool] = {SAME: False, OPP: False}

    def setup_components(self) -> None:
        self.pictograph_frame = OptionPickerPictographFrame(self)
        self.header = OptionPickerSectionHeader(self)

        self.header.type_label.clicked.connect(self.toggle_section)
        self.pictographs: dict[str, BasePictograph] = {}
        self.pictograph_frame.setStyleSheet("QFrame {border: none;}")
        self._setup_layout()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.pictograph_frame)

    def toggle_section(self) -> None:
        is_visible = not self.pictograph_frame.isVisible()
        self.pictograph_frame.setVisible(is_visible)

    def clear_pictographs(self) -> None:
        for pictograph_key in list(self.pictographs.keys()):
            pictograph = self.pictographs.pop(pictograph_key)
            pictograph.view.setParent(None)
            pictograph.view.hide()

    def set_size_policy(self, horizontal, vertical) -> None:
        size_policy = QSizePolicy(horizontal, vertical)
        self.setSizePolicy(size_policy)
        for pictograph in self.pictographs.values():
            pictograph.view.setSizePolicy(size_policy)

    def add_pictograph(self, pictograph: BasePictograph) -> None:
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
        for pictograph in self.pictographs.values():
            pictograph.view.resize_pictograph_view()
        self.header.type_label.resize_section_type_label()
