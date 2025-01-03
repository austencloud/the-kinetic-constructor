from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QTabWidget,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QWidget,
)
from PyQt6.QtGui import QFont

from main_window.main_widget.settings_dialog.settings_dialog_styler import SettingsDialogStyler

from .user_profile_tab import UserProfileTab
from .prop_type_tab import PropTypeTab
from .background_tab import BackgroundTab
from .visibility_tab import VisibilityTab

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog
    from main_window.main_widget.main_widget import MainWidget

class SettingsDialogActionButtons(QWidget):
    def __init__(self, dialog: "SettingsDialog"):
        super().__init__(dialog)
        self.dialog = dialog
        self._setup_ui()

    def _setup_ui(self):
        layout = QHBoxLayout(self)
        self.setLayout(layout)

        layout.addSpacerItem(
            QSpacerItem(
                40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
            )
        )

        self.save_button = HoverButton("Save", self.dialog)
        self.close_button = HoverButton("Close", self.dialog)

        layout.addWidget(self.save_button)
        layout.addWidget(self.close_button)


class HoverButton(QPushButton):
    def __init__(self, text, parent):
        super().__init__(text, parent)
        SettingsDialogStyler.style_button(self)

    def enterEvent(self, event):
        self.setStyleSheet("""
            QPushButton {
                background-color: #99CCFF;
                color: white;
                border-radius: 10px;
                padding: 10px 15px;
            }
        """)
        super().enterEvent(event)

    def leaveEvent(self, event):
        SettingsDialogStyler.style_button(self)
        super().leaveEvent(event)
