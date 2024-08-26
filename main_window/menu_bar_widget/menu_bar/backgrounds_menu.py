from PyQt6.QtGui import QAction, QActionGroup
from typing import TYPE_CHECKING

from .hoverable_menu import HoverableMenu

if TYPE_CHECKING:
    from .menu_bar import MenuBar


class BackgroundsMenu(HoverableMenu):
    def __init__(self, menu_bar: "MenuBar"):
        super().__init__("Backgrounds", menu_bar)
        self.menu_bar = menu_bar
        self.settings_manager = self.menu_bar.main_widget.main_window.settings_manager

        background_action_group = QActionGroup(self)
        background_action_group.setExclusive(True)

        background_types = [
            "Rainbow",
            "Starfield",
            "Particle",
            "Aurora",
            "AuroraBorealis",
        ]
        current_bg = self.settings_manager.global_settings.get_background_type()

        for bg_type in background_types:
            action = QAction(bg_type, self, checkable=True)
            action.setChecked(current_bg == bg_type)
            action.triggered.connect(
                lambda checked, bg=bg_type: (
                    self.set_background_type(bg) if checked else None
                )
            )
            self.addAction(action)
            background_action_group.addAction(action)

    def set_background_type(self, bg_type: str):
        self.settings_manager.global_settings.set_background_type(bg_type)
