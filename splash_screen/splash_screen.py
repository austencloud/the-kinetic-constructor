from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QScreen, QPainter

from main_window.main_widget.act_tab.act_sheet.act_header import title_label

from .splash_properties import SplashProperties
from .splash_components import SplashComponents
from .splash_layout_manager import SplashLayoutManager

if TYPE_CHECKING:
    from main_window.main_widget.dictionary_widget.dictionary_browser.rainbow_progress_bar import (
        RainbowProgressBar,
    )
    from main_window.settings_manager.settings_manager import SettingsManager


class SplashScreen(QWidget):
    title_label: QLabel
    currently_loading_label: QLabel
    created_by_label: QLabel
    progress_bar: "RainbowProgressBar"
    logo_label: QLabel

    def __init__(self, target_screen: QScreen, settings_manager: "SettingsManager"):
        super().__init__()
        self.target_screen = target_screen
        self.settings_manager = settings_manager

        self.properties = SplashProperties(self, self.target_screen)
        self.components = SplashComponents(self)
        self.layout_manager = SplashLayoutManager(self, self.components)
        self._setup_background_manager()
        self._center_on_screen()
        self.show()

    def _setup_background_manager(self):
        self.background_manager = (
            self.settings_manager.global_settings.setup_background_manager(
                self, is_splash_screen=True
            )
        )

    def _center_on_screen(self):
        screen_geometry = self.target_screen.geometry()
        self.setGeometry(
            screen_geometry.x() + (screen_geometry.width() - self.width()) // 2,
            screen_geometry.y() + (screen_geometry.height() - self.height()) // 2,
            self.width(),
            self.height(),
        )

    def paintEvent(self, event):
        painter = QPainter(self)
        self.background_manager.paint_background(self, painter)

    def update_progress(self, value, message=""):
        self.progress_bar.setValue(value)
        if message:
            self.currently_loading_label.setText(message)
