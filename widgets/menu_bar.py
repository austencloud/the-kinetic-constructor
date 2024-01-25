# MenuBar.py
from PyQt6.QtWidgets import QMenuBar
from typing import TYPE_CHECKING
from PyQt6.QtGui import QAction

if TYPE_CHECKING:
    from .main_widget.main_widget import MainWidget


class MainWindowMenuBar(QMenuBar):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self._setup_menu()

    def _setup_menu(self) -> None:
        # Example: Add a 'Refresh Placements' action
        refresh_action = QAction("Refresh Placements", self)
        refresh_action.triggered.connect(self.main_widget.refresh_placements)
        self.addAction(refresh_action)

        # Add collapse button
        collapse_action = QAction("Collapse", self)
        collapse_action.triggered.connect(self.main_widget.toggle_main_sequence_widget)
        self.addAction(collapse_action)
        # Additional menu items can be added here
