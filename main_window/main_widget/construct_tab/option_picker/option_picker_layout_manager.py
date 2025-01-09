from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.option_picker.option_picker import (
        OptionPicker,
    )


class OptionPickerLayoutManager:
    def __init__(self, option_picker: "OptionPicker"):
        self.op = option_picker
        self.setup_layout()

    def setup_layout(self) -> None:
        self.op.layout = QVBoxLayout(self.op)
        self.op.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.op.choose_next_label.show()

        header_layout = QVBoxLayout()
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        header_label_layout = QHBoxLayout()
        header_label_layout.addWidget(self.op.choose_next_label)
        header_layout.addLayout(header_label_layout)

        self.op.layout.addLayout(header_layout)
        self.op.layout.addWidget(self.op.reversal_filter)
        self.op.layout.addWidget(self.op.scroll_area, 14)
