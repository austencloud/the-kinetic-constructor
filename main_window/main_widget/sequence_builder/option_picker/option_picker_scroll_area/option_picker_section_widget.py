from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QGroupBox
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

    def add_pictograph(self, pictograph: BasePictograph) -> None:
        self.pictographs[
            self.scroll_area.main_widget.pictograph_key_generator.generate_pictograph_key(
                pictograph.pictograph_dict
            )
        ] = pictograph
        
        # Suppose we keep a count of how many pictographs we've added:
        count = len(self.pictographs)
        row, col = divmod(count - 1, self.scroll_area.option_picker.COLUMN_COUNT) 
        self.pictograph_frame.layout.addWidget(pictograph.view, row, col)
        pictograph.view.show()


    def resizeEvent(self, event) -> None:
        """Resizes the section widget and ensures minimal space usage."""
        section_width = self.scroll_area.manual_builder.width()

        if self.letter_type in [LetterType.Type1, LetterType.Type2, LetterType.Type3]:
            self.setFixedWidth(section_width)
        elif self.letter_type in [LetterType.Type4, LetterType.Type5, LetterType.Type6]:
            COLUMN_COUNT = self.scroll_area.option_picker.COLUMN_COUNT
            sections = self.scroll_area.section_manager.sections

            calculated_width = int(
                (self.scroll_area.option_picker.width() / COLUMN_COUNT)
                - ((self.scroll_area.spacing))
            )

            view_width = (
                calculated_width
                if calculated_width < self.scroll_area.option_picker.height() // 8
                else self.scroll_area.option_picker.height() // 8
            )
            width = int(view_width * 8) // 3
            self.setFixedWidth(width)

        self.header.type_label.resize_section_type_label()
        super().resizeEvent(event)
