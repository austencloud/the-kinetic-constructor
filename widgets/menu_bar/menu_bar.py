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
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_preferences_dialog)
        self.addAction(settings_action)

    def open_preferences_dialog(self) -> None:
        preferences_dialog = PreferencesDialog(self.main_widget.main_window)
        preferences_dialog.exec()

    def _setup_menu(self) -> None:
        refresh_action = QAction("Refresh Placements", self)
        refresh_action.triggered.connect(
            self.main_widget.special_placement_loader.refresh_placements
        )
        self.addAction(refresh_action)

        # Optionally, other menu items and actions can be added here.

        # Set the font size for the menu items
        font = self.font()  # Gets the current font
        font.setPointSize(12)  # Adjust the font size as desired
        self.setFont(font)
