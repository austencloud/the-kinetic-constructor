from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon, QCursor
from PyQt6.QtCore import QSize, Qt

from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog

if TYPE_CHECKING:
    from main_window.menu_bar.menu_bar import MenuBarWidget


class SettingsButton(QPushButton):
    def __init__(self, menu_bar: "MenuBarWidget") -> None:
        super().__init__(
            QIcon("images\icons\sequence_widget_icons\settings.png"), None, menu_bar
        )
        self.main_widget = menu_bar.main_widget
        self.clicked.connect(self.show_settings_dialog)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

    def show_settings_dialog(self):
        dialog = SettingsDialog(self.main_widget)
        dialog.exec()

    def resizeEvent(self, event):
        size = int(self.main_widget.width() // 24)
        self.setFixedSize(QSize(size, size))
        icon_size = int(size * 0.75)
        self.setIconSize(QSize(icon_size, icon_size))
        super().resizeEvent(event)
