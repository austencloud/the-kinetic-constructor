from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QSizePolicy,
)
from PyQt6.QtCore import QSize
from PyQt6.QtGui import QPixmap, QIcon
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class OptionBoard(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.grid_widget = QWidget()
        self.optionboard_grid_layout = QGridLayout()
        self.scroll_area = QScrollArea()
        self.main_layout = QVBoxLayout()

        self.setup_ui()
        self.populate_pictographs()
        self.connect_signals()

    def setup_ui(self) -> None:
        self.grid_widget.setLayout(self.optionboard_grid_layout)
        self.optionboard_grid_layout.setSpacing(0)

        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.grid_widget)

        self.scroll_area.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.scroll_area.setMaximumWidth(
            int(self.main_widget.main_window.width() * 0.35)
        )
        self.scroll_area.setMinimumHeight(
            int(self.main_widget.main_window.height() * 0.6)
        )
        self.main_layout.addWidget(self.scroll_area)
        # Remove padding in the optionboard layout
        self.optionboard_grid_layout.setContentsMargins(0, 0, 0, 0)

        # Remove padding in the main layout
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

    def populate_pictographs(self) -> None:
        number_of_pictographs = 50
        MAX_ITEMS_PER_ROW = 4

        # Assuming the width of the OptionBoard (self.width()) is available
        pictograph_width = self.scroll_area.width() / 4  # 4 pictographs per row
        pictograph_height = pictograph_width * (
            90 / 75
        )  # According to the desired ratio

        for i in range(number_of_pictographs):
            pictograph_button = QPushButton(f"Picto {i+1}")
            pictograph_button.setIcon(QIcon(QPixmap("path/to/your/pictograph/image")))
            pictograph_button.setIconSize(
                QSize(int(pictograph_width), int(pictograph_height))
            )
            pictograph_button.setFixedSize(
                int(pictograph_width), int(pictograph_height)
            )
            self.optionboard_grid_layout.addWidget(
                pictograph_button, i // MAX_ITEMS_PER_ROW, i % MAX_ITEMS_PER_ROW
            )

    def connect_signals(self) -> None:
        for button in self.grid_widget.findChildren(QPushButton):
            button.clicked.connect(self.on_pictograph_clicked)

    def on_pictograph_clicked(self) -> None:
        pass
