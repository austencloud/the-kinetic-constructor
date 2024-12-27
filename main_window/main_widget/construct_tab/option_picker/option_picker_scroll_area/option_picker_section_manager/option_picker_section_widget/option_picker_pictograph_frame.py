from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QGridLayout
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from widgets.sequence_builder.components.option_picker.option_picker_scroll_area.option_picker_section_manager.option_picker_section_widget.option_picker_section_widget import OptionPickerSectionWidget


class OptionPickerPictographFrame(QFrame):
    def __init__(self, section: "OptionPickerSectionWidget"):
        super().__init__()
        self.section = section
        self.spacing = 3
        self.layout: QGridLayout = QGridLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(self.spacing)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
