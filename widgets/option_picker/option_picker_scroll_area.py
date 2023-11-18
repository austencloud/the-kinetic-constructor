from PyQt6.QtWidgets import (
    QScrollArea,
    QSizePolicy,
    QFrame,
    QWidget,
    QGridLayout,
    QPushButton,
)
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.option_picker.option_picker import OptionPicker
from PyQt6.QtWidgets import QScrollBar


class OptionPickerScrollArea(QScrollArea):
    scrollbar_width = 0  # Class variable to store the width of the scrollbar

    def __init__(self, option_picker: "OptionPicker") -> None:
        super().__init__()
        self.main_window = option_picker.main_window
        self.main_widget = option_picker.main_widget
        self.option_picker = option_picker
        self.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setWidgetResizable(True)
        self.grid_widget = QWidget()
        self.option_picker_grid_layout = QGridLayout(self.grid_widget)
        self.option_picker_grid_layout.setContentsMargins(0, 0, 0, 0)
        self.option_picker_grid_layout.setSpacing(0)
        self.setWidget(
            self.grid_widget
        )  # Set the grid widget as the widget for the scroll area
        # Assuming the width of the OptionBoard (self.width()) is available
        self.pictograph_width = (
            (self.main_widget.main_window.width() / 2) * (3 / 4) / 4
        )  # 4 pictographs per row
        self.pictograph_height = self.pictograph_width * (
            90 / 75
        )  # According to the desired ratio
        # set the vertical scrol bar's width
        self.verticalScrollBar().setFixedWidth(int(self.main_window.width() * 0.01))

        self.populate_pictographs()
        self.connect_signals()
        self.update_scroll_area_size()

    def connect_signals(self) -> None:
        for button in self.grid_widget.findChildren(QPushButton):
            button.clicked.connect(self.on_pictograph_clicked)

    def populate_pictographs(self) -> None:
        number_of_pictographs = 50
        MAX_ITEMS_PER_ROW = 4

        for i in range(number_of_pictographs):
            pictograph_button = QPushButton(f"Picto {i+1}")
            pictograph_button.setIcon(QIcon(QPixmap("path/to/your/pictograph/image")))
            pictograph_button.setIconSize(
                QSize(int(self.pictograph_width), int(self.pictograph_height))
            )
            pictograph_button.setFixedSize(
                int(self.pictograph_width), int(self.pictograph_height)
            )
            self.option_picker_grid_layout.addWidget(
                pictograph_button, i // MAX_ITEMS_PER_ROW, i % MAX_ITEMS_PER_ROW
            )

    def on_pictograph_clicked(self) -> None:
        pass

    def update_scroll_area_size(self) -> None:
        if self.scrollbar_width == 0:
            self.scrollbar_width = self.verticalScrollBar().width()
        self.setFixedWidth(int(self.pictograph_width * 4 + self.scrollbar_width))
