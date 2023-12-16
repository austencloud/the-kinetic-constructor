from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy
from .option_picker_letter_buttons import LetterButtons
from .option_picker import OptionPicker


class OptionPickerWidget(QFrame):
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
        self.button_frame = LetterButtons(self.main_widget, self)
        self.option_picker = OptionPicker(self.main_widget, self)

        self.main_layout.addWidget(self.option_picker, 5)
        self.main_layout.addWidget(self.button_frame, 1)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        self.setLayout(self.main_layout)

    def resize_option_picker_widget(self) -> None:
        self.option_picker.resize_option_views()
        self.button_frame.resize_letter_buttons()
