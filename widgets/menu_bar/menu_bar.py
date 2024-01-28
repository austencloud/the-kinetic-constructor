# MenuBar.py
from PyQt6.QtWidgets import QMenuBar
from typing import TYPE_CHECKING
from PyQt6.QtGui import QAction

from widgets.menu_bar.preferences_dialog import PreferencesDialog

if TYPE_CHECKING:
    from ..main_widget.main_widget import MainWidget


class MainWindowMenuBar(QMenuBar):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self._setup_menu()
        self._setup_settings_menu()

    def _setup_settings_menu(self) -> None:
        settings_menu = self.addMenu("Settings")
        preferences_action = QAction("Preferences", self)
        preferences_action.triggered.connect(self.open_preferences_dialog)
        settings_menu.addAction(preferences_action)

    def open_preferences_dialog(self) -> None:
        preferences_dialog = PreferencesDialog(self.main_widget.main_window)
        preferences_dialog.exec()

    def _setup_menu(self) -> None:
        refresh_action = QAction("Refresh Placements", self)
        refresh_action.triggered.connect(self.main_widget.refresh_placements)
        self.addAction(refresh_action)

        collapse_action = QAction("Collapse", self)
        collapse_action.triggered.connect(self.main_widget.toggle_main_sequence_widget)
        self.addAction(collapse_action)
