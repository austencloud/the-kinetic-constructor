from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
from PyQt6.QtWidgets import QFrame, QHBoxLayout
from .letter_buttons import LetterButtons
from .scroll_area import ScrollArea


class OptionPicker(QFrame):
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
        self.scroll_area = ScrollArea(self)
        self.button_frame = LetterButtons(self.main_widget, self)

        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.button_frame)

        self.setLayout(self.main_layout)

    ### RESIZE EVENT HANDLERS ###

    def update_size(self) -> None:
        self.setFixedSize(
            int(self.main_widget.width() * 0.5), int(self.main_widget.height() * 2 / 3)
        )

        self.scroll_area.update_scroll_area_size()
        self.button_frame.update_size()
