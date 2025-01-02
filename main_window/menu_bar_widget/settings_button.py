from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

from main_window.main_widget.settings_dialog import SettingsDialog
from .social_media_widget import SocialMediaWidget
from .selectors_widget import SelectorsWidget

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SettingsButton(QPushButton):
    def __init__(self, parent: QWidget, main_widget: "MainWidget") -> None:
        super().__init__(QIcon("path/to/settings/icon.png"), "Settings", parent)
        self.main_widget = main_widget
        self.clicked.connect(self.show_settings_dialog)

    def show_settings_dialog(self):
        dialog = SettingsDialog(self.main_widget)
        dialog.exec()
