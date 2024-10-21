from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QGroupBox, QSizePolicy
from Enums.Enums import LetterType
from data.constants import OPP, SAME
from PyQt6.QtCore import Qt


from base_widgets.base_pictograph.base_pictograph import BasePictograph
from main_window.main_widget.sequence_builder.option_picker.option_picker_scroll_area.option_picker_section_header import (
    OptionPickerSectionHeader,
)
from main_window.main_widget.sequence_builder.option_picker.option_picker_scroll_area.option_picker_section_pictograph_frame import (
    OptionPickerSectionPictographFrame,
)


if TYPE_CHECKING:
    from main_window.main_widget.sequence_builder.option_picker.option_picker_scroll_area.option_picker_scroll_area import (
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

    def setup_components(self) -> None:
        self.pictograph_frame = OptionPickerSectionPictographFrame(self)
        self.pictographs: dict[str, BasePictograph] = {}
        self.pictograph_frame.setStyleSheet("QFrame {border: none;}")
        self._setup_header()
        self._setup_layout()
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.pictograph_frame)

    def _setup_header(self) -> None:
        self.header = OptionPickerSectionHeader(self)
        self.header.type_label.clicked.connect(self.toggle_section)

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
        section_width = int((self.scroll_area.manual_builder.width()))
        if self.letter_type in [LetterType.Type1, LetterType.Type2, LetterType.Type3]:
            self.setMinimumWidth(section_width)
            self.setMaximumWidth(section_width)
        elif self.letter_type in [LetterType.Type4, LetterType.Type5, LetterType.Type6]:
            self.setMinimumWidth(int(section_width / 3))
            self.setMaximumWidth(int(section_width / 3))
        for pictograph in self.pictographs.values():
            pictograph.view.resize_pictograph_view()
        self.header.type_label.resize_section_type_label()
