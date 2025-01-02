from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize

from main_window.main_widget.settings_dialog import SettingsDialog
from main_window.menu_bar_widget.settings_button import SettingsButton
from .social_media_widget import SocialMediaWidget
from .selectors_widget import SelectorsWidget

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget



class MenuBarWidget(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(0)

        self.social_media_widget = SocialMediaWidget(self)
        self.settings_button = SettingsButton(self, self.main_widget)

        # self.layout.addStretch(1)
        self.layout.addWidget(self.social_media_widget)
        self.layout.addWidget(self.settings_button)
        # self.layout.addStretch(1)

        self.setLayout(self.layout)

    def resizeEvent(self, event):
        self.social_media_widget.resize_social_media_buttons()
