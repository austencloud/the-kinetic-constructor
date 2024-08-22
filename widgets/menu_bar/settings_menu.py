from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction


if TYPE_CHECKING:
    from widgets.menu_bar.main_window_menu_bar import MainWindowMenuBar

class SettingsMenu(QMenu):
    def __init__(self, menu_bar: "MainWindowMenuBar"):
        super().__init__("Settings", menu_bar)
        self.menu_bar = menu_bar

        preferences_action = QAction("Preferences", self)
        preferences_action.triggered.connect(self.open_preferences_dialog)
        self.addAction(preferences_action)

    def open_preferences_dialog(self):
        self.menu_bar.main_widget.main_settings_dialog.load_initial_settings()
        self.menu_bar.main_widget.main_settings_dialog.exec()
