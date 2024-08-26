from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout
from .menu_bar.menu_bar import MenuBar

if TYPE_CHECKING:
    from main_window.main_window import MainWindow


class MenuBarWidget(QWidget):
    def __init__(self, main_window: "MainWindow") -> None:

        super().__init__()
        self.main_window = main_window
        self.menu_bar = MenuBar(self)
        layout: QHBoxLayout = QHBoxLayout(self)
        layout.addStretch(1)
        layout.addWidget(self.menu_bar)
        layout.addStretch(1)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def resize_menu_bar_widget(self):
        self.menu_bar.resize_menu_bar()