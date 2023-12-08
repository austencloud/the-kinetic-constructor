from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget

from PyQt6.QtWidgets import QFrame, QHBoxLayout
from .option_picker_letter_buttons import OptionPickerLetterButtons
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
        self.setFixedSize(self.width(), self.height())
        self.option_picker = OptionPicker(self)
        self.button_frame = OptionPickerLetterButtons(self.main_widget, self)

        self.main_layout.addWidget(self.option_picker)
        self.main_layout.addWidget(self.button_frame)

        self.setLayout(self.main_layout)

    ### RESIZE EVENT HANDLERS ###

    def update_size(self) -> None:
        self.setFixedSize(
            int(self.main_widget.width() * 0.5), int(self.main_widget.height() * 2 / 3)
        )

        self.option_picker.update_option_picker_size()
        self.button_frame.update_button_frame_size()
