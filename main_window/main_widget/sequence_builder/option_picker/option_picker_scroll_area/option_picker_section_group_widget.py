from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
if TYPE_CHECKING:
    from main_window.main_widget.sequence_builder.option_picker.option_picker_scroll_area.option_picker_scroll_area import OptionPickerScrollArea
    from main_window.main_widget.sequence_builder.option_picker.option_picker_scroll_area.option_picker_section_widget import OptionPickerSectionWidget


class OptionPickerSectionGroupWidget(QWidget):
    def __init__(self, scroll_area: "OptionPickerScrollArea") -> None:
        super().__init__(scroll_area)
        self.scroll_area = scroll_area

        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(10)  # Space between sections, adjust as needed
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        self.setLayout(self.layout)

    def add_section_widget(self, section: "OptionPickerSectionWidget") -> None:
        """Add each section to the layout and ensure it’s centered."""
        section.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.layout.addWidget(section, alignment=Qt.AlignmentFlag.AlignCenter)
