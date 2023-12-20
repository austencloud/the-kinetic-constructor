from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy
from .option_picker_letter_button_frame import OptionPickerLetterButtonFrame
from .option_picker_scroll import OptionPickerScroll


class OptionPickerTab(QFrame):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.main_layout = QHBoxLayout(self)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.button_frame = OptionPickerLetterButtonFrame(self.main_widget, self)
        self.option_picker = OptionPickerScroll(self.main_widget, self)

        self.main_layout.addWidget(self.option_picker)
        self.main_layout.addWidget(self.button_frame)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setLayout(self.main_layout)

    def resize_option_picker_widget(self) -> None:
        self.option_picker.resize_option_picker()
        self.button_frame.resize_letter_buttons()
