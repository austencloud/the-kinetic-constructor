from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QScreen, QPainter

from splash_screen.splash_geometry_manager import SplashScreenGeometryManager

from .splash_properties import SplashProperties
from .splash_components import SplashComponents
from .splash_layout_manager import SplashLayoutManager
from .splash_screen_updater import SplashScreenUpdater

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

        self.properties = SplashProperties(self)
        self.components = SplashComponents(self)
        self.layout_manager = SplashLayoutManager(self)
        self.updater = SplashScreenUpdater(self)
        self.geometry_manager = SplashScreenGeometryManager(self)
        self._setup_background_manager()
        self.show()

    def _setup_background_manager(self):
        self.background_manager = (
            self.settings_manager.global_settings.setup_background_manager(
                self, is_splash_screen=True
            )
        )

    def paintEvent(self, event):
        """Handle custom painting with background manager."""
        painter = QPainter(self)
        try:
            self.background_manager.paint_background(self, painter)
        finally:
            painter.end()  # Ensures QPainter is ended after painting
