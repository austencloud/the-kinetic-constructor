# grid_mode_selector.py
from typing import TYPE_CHECKING
from ..base_selector import LabelSelector
from .grid_mode_dialog import GridModeDialog

if TYPE_CHECKING:
    from main_window.menu_bar_widget.menu_bar_widget import MenuBarWidget


class GridModeSelector(LabelSelector):
    def __init__(self, menu_bar_widget: "MenuBarWidget"):
        current_grid_mode = menu_bar_widget.main_window.settings_manager.global_settings.get_grid_mode().capitalize()
        super().__init__(menu_bar_widget, current_grid_mode)
        self.settings_manager = self.main_window.settings_manager
        self.main_widget = self.main_window.main_widget

    def on_label_clicked(self):
        dialog = GridModeDialog(self)
        dialog.show_dialog()

    def set_current_grid_mode(self, grid_mode: str):
        self.set_display_text(grid_mode.capitalize())
        self.settings_manager.global_settings.set_grid_mode(grid_mode.lower())
        self.main_widget.set_grid_mode(grid_mode.lower())
        self.settings_manager.save_settings()
