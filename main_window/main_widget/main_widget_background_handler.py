# main_widget_background_handler.py
from typing import TYPE_CHECKING, Optional
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import QObject

from main_window.menu_bar_widget.background_selector.backgrounds.aurora.aurora_background import (
    AuroraBackground,
)
from main_window.menu_bar_widget.background_selector.backgrounds.aurora_borealis_background import (
    AuroraBorealisBackground,
)
from main_window.menu_bar_widget.background_selector.backgrounds.base_background import (
    BaseBackground,
)
from main_window.menu_bar_widget.background_selector.backgrounds.bubbles_background import (
    BubblesBackground,
)
from main_window.menu_bar_widget.background_selector.backgrounds.snowfall.snowfall_background import (
    SnowfallBackground,
)
from main_window.menu_bar_widget.background_selector.backgrounds.starfield.starfield_background import (
    StarfieldBackground,
)

if TYPE_CHECKING:
    from .main_widget import MainWidget


class MainWidgetBackgroundHandler(QObject):
    """Handles background setup, application, and management for the MainWidget."""

    def __init__(self, main_widget: "MainWidget"):
        super().__init__()
        self.main_widget = main_widget
        self.background: Optional[BaseBackground] = None
        self.is_animating = False

    def setup_background(self, is_splash_screen: bool = False):
        """Initializes the background based on the current background type."""
        bg_type = (
            self.main_widget.settings_manager.global_settings.get_background_type()
        )
        self.background = self.get_background(bg_type)

        if self.background:
            # Connect the update_required signal to the main widget's update method
            self.background.update_required.connect(self.main_widget.update)
            # Start the background animation
            self.background.start_animation()

    def apply_background(self, is_splash_screen: bool = False):
        """Applies or reapplies the background."""
        if self.background:
            # Stop existing animation and disconnect signals
            self.background.stop_animation()
            self.background.update_required.disconnect(self.main_widget.update)

        self.setup_background(is_splash_screen)

    def get_background(self, bg_type: str) -> Optional[BaseBackground]:
        """Returns an instance of the appropriate Background based on bg_type."""
        background_map = {
            "Starfield": StarfieldBackground,
            "Aurora": AuroraBackground,
            "AuroraBorealis": AuroraBorealisBackground,
            "Snowfall": SnowfallBackground,
            "Bubbles": BubblesBackground,
        }
        manager_class = background_map.get(bg_type)
        return manager_class(self.main_widget) if manager_class else None

    def stop_animation(self):
        """Stops the background animation."""
        if self.background:
            self.background.stop_animation()
