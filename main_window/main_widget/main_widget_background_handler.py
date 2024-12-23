from typing import TYPE_CHECKING, Optional, Callable, Union
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt, pyqtSlot

from main_window.menu_bar_widget.background_selector.background_managers.aurora.aurora_background_manager import (
    AuroraBackgroundManager,
)
from main_window.menu_bar_widget.background_selector.background_managers.aurora_borealis_background_manager import (
    AuroraBorealisBackgroundManager,
)
from main_window.menu_bar_widget.background_selector.background_managers.background_manager import (
    BackgroundManager,
)
from main_window.menu_bar_widget.background_selector.background_managers.bubbles_background_manager import (
    BubblesBackgroundManager,
)
from main_window.menu_bar_widget.background_selector.background_managers.snowfall.snowfall_background_manager import (
    SnowfallBackgroundManager,
)
from main_window.menu_bar_widget.background_selector.background_managers.starfield.starfield_background_manager import (
    StarfieldBackgroundManager,
)

if TYPE_CHECKING:
    from .main_widget import MainWidget


class MainWidgetBackgroundHandler:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget
        self.background_manager: Optional[BackgroundManager] = None
        self.is_animating = False  # Flag to prevent overlapping animations

    def setup_background_manager(self):
        """Initializes the background manager based on the current background type."""
        bg_type = (
            self.main_widget.settings_manager.global_settings.get_background_type()
        )
        self.background_manager = self.get_background_manager(bg_type)
        self.main_widget.background_manager = self.background_manager
        if self.background_manager:
            # Connect the update_required signal to the main widget's update method
            self.background_manager.update_required.connect(self.main_widget.update)
            # Start the background animation
            self.background_manager.start_animation()

    def apply_background(self, is_splash_screen: bool = False):
        """Applies or reapplies the background manager."""
        if self.background_manager:
            # Stop existing animation before applying a new background
            self.background_manager.stop_animation()
            self.background_manager.update_required.disconnect(self.main_widget.update)

        self.setup_background_manager()

    def get_background_manager(self, bg_type: str) -> Optional[BackgroundManager]:
        """Returns an instance of the appropriate BackgroundManager based on bg_type."""

        self.main_widget.font_color_updater.update_main_widget_font_colors(bg_type)

        # else:
        #     self.main_widget.font_color_updater.apply_splash_screen_font_colors(widget, bg_type)
        background_manager_map = {
            "Starfield": StarfieldBackgroundManager,
            "Aurora": AuroraBackgroundManager,
            "AuroraBorealis": AuroraBorealisBackgroundManager,
            "Snowfall": SnowfallBackgroundManager,
            "Bubbles": BubblesBackgroundManager,
        }
        manager_class = background_manager_map.get(bg_type)
        return manager_class(self.main_widget) if manager_class else None

    def stop_animation(self):
        """Stops the background animation."""
        if self.background_manager:
            self.background_manager.stop_animation()
