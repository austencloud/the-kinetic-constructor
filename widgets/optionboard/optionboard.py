from PyQt6.QtWidgets import (
    QGraphicsScene,
    QGraphicsView,
    QGridLayout,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QScrollArea,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from typing import TYPE_CHECKING
from widgets.optionboard.optionboard_view import OptionBoardView
if TYPE_CHECKING:
    from widgets.main_widget import MainWidget


class OptionBoard(QGraphicsScene):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.grid_widget = QWidget()
        self.optionboard_grid_layout = QGridLayout()
        self.scroll_area = QScrollArea()
        self.main_layout = QVBoxLayout()
        self.container_widget = QWidget()
        self.setup_ui()
        self.view = OptionBoardView(self)
        self.populate_pictographs()
        self.connect_signals()

    def setup_ui(self) -> None:
        self.grid_widget.setLayout(self.optionboard_grid_layout)
        self.optionboard_grid_layout.setSpacing(0)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.grid_widget)
        self.main_layout.addWidget(self.scroll_area)
        self.container_widget.setLayout(self.main_layout)
        self.container_widget.setFixedSize(600, 800)
        self.setSceneRect(0, 0, 600, 800)
        self.addWidget(self.container_widget)

    def populate_pictographs(self) -> None:
        number_of_pictographs = 50
        MAX_ITEMS_PER_ROW = 4

        for i in range(number_of_pictographs):
            pictograph_button = QPushButton(f"Picto {i+1}")
            pictograph_button.setIcon(QIcon(QPixmap("path/to/your/pictograph/image")))
            pictograph_button.setIconSize(QSize(100, 100))
            pictograph_button.setFixedSize(125, 150)
            self.optionboard_grid_layout.addWidget(
                pictograph_button, i // MAX_ITEMS_PER_ROW, i % MAX_ITEMS_PER_ROW
            )

    def connect_signals(self) -> None:
        for button in self.grid_widget.findChildren(QPushButton):
            button.clicked.connect(self.on_pictograph_clicked)

    def on_pictograph_clicked(self) -> None:
        pass


# In another part of your code, where you instantiate Op
