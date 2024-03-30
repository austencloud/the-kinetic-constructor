from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from widgets.scroll_area.components.section_manager.section_widget.components.section_type_label import (
    SectionTypeLabel,
)

if TYPE_CHECKING:
    from widgets.sequence_builder.components.option_picker.option_picker_section_widget import (
        OptionPickerSectionWidget,
    )


class OptionPickerSectionHeader(QWidget):
    def __init__(self, section: "OptionPickerSectionWidget") -> None:
        super().__init__()
        self.section = section
        self.type_label = SectionTypeLabel(section)
        self._setup_layout()

    def _setup_layout(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addStretch(1)
        self.layout.addWidget(self.type_label)
        self.layout.addStretch(1)
