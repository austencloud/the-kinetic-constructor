from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class NonRadialPointsToggler:
    def __init__(self, main_widget: "MainWidget") -> None:
        self.main_widget = main_widget
        self.settings = self.main_widget.settings_manager.visibility
        self.settings_manager = self.settings.settings_manager
        self.non_radial_visible = self.settings.get_non_radial_visibility()
