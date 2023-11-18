from typing import TYPE_CHECKING

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtWidgets import (
    QGridLayout,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from data.letter_engine_data import letter_types
from settings.string_constants import LETTER_SVG_DIR

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QFrame, QHBoxLayout
from .option_picker_buttons_frame import LetterButtons
from .option_picker_scroll_area import OptionPickerScrollArea


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
        self.scroll_area = OptionPickerScrollArea(self)
        self.button_frame = LetterButtons(self.main_window)

        self.main_layout.addWidget(self.scroll_area)
        self.main_layout.addWidget(self.button_frame)

        self.setLayout(self.main_layout)

    ### RESIZE EVENT HANDLERS ###

    def update_size(self) -> None:
        self.setFixedSize(
            int(self.main_widget.width() * 0.5), int(self.main_widget.height() * 3 / 4)
        )
        self.scroll_area.update_scroll_area_size()
        self.button_frame.update_letter_buttons_size()
