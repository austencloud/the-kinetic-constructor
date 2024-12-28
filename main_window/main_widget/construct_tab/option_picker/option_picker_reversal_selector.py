from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt
from main_window.main_widget.construct_tab.option_picker.reversal_combobox import (
    ReversalCombobox,
)

if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.option_picker.option_picker import (
        OptionPicker,
    )


class OptionPickerReversalSelector(QWidget):

    def __init__(self, option_picker: "OptionPicker"):
        super().__init__(option_picker)
        self.option_picker = option_picker

        self.reversal_combobox = ReversalCombobox(self)
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.combo_box_label: QLabel = QLabel("Show:")
        self.layout.addWidget(self.combo_box_label)
        self.layout.addWidget(self.reversal_combobox)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        font = self.font()
        font_size = int(self.option_picker.construct_tab.main_widget.width() * 0.0075)
        font.setPointSize(font_size)
        font.setFamily("Georgia")
        self.setFont(font)
        self.combo_box_label.setFont(font)
