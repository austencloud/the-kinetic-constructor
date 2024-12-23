from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QScreen, QPainter

from main_window.main_widget.main_widget_background_handler import (
    MainWidgetBackgroundHandler,
)
from splash_screen.splash_geometry_manager import SplashGeometryManager
from splash_screen.splash_background_handler import SplashBackgroundHandler
from splash_screen.splash_font_color_updater import SplashFontColorUpdater

from .splash_properties import SplashProperties
from .splash_components import SplashComponents
from .splash_layout_manager import SplashLayoutManager
from .splash_updater import SplashUpdater

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
        self.updater = SplashUpdater(self)
        self.geometry_manager = SplashGeometryManager(self)
        self.font_color_updater = SplashFontColorUpdater(self)
        self.background_handler = SplashBackgroundHandler(self)
        self.background_handler.setup_background_manager()

        self._setup_background_manager()
        self.show()

    def _setup_background_manager(self):
        self.background_manager = self.background_handler.background_manager

    def paintEvent(self, event):
        painter = QPainter(self)
        if self.background_handler.background_manager:
            self.background_handler.background_manager.paint_background(self, painter)
