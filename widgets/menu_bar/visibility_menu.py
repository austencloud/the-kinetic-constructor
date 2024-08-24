from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QAction


if TYPE_CHECKING:
    from widgets.menu_bar.main_window_menu_bar import MainWindowMenuBar


class VisibilityMenu(QMenu):
    def __init__(self, menu_bar: "MainWindowMenuBar"):
        super().__init__("Visibility", menu_bar)
        self.menu_bar = menu_bar
        self.glyph_visibility_manager = (
            self.menu_bar.main_widget.main_window.settings_manager.visibility.glyph_visibility_manager
        )
        self.grid_visibility_manager = (
            self.menu_bar.main_widget.main_window.settings_manager.visibility.grid_visibility_manager
        )

        # Glyph visibility toggles
        for glyph_type in ["TKA", "VTG", "Elemental", "EndPosition"]:
            action = QAction(f"{glyph_type} Glyph", self, checkable=True)
            action.setChecked(
                self.glyph_visibility_manager.get_glyph_visibility(glyph_type)
            )
            action.triggered.connect(
                lambda checked, gt=glyph_type: self.toggle_glyph_visibility(gt, checked)
            )
            self.addAction(action)

        non_radial_action = QAction("Non-Radial Points", self, checkable=True)
        non_radial_action.setChecked(self.grid_visibility_manager.non_radial_visible)
        non_radial_action.triggered.connect(
            self.grid_visibility_manager.toggle_visibility
        )
        self.addAction(non_radial_action)

    def toggle_glyph_visibility(self, glyph_type: str, visible: bool):
        self.glyph_visibility_manager.set_glyph_visibility(glyph_type, visible)
        self.glyph_visibility_manager.apply_glyph_visibility()
