# visibility_selector.py
from typing import TYPE_CHECKING
from ..base_selector import ButtonSelector
from .visibility_dialog import VisibilityDialog

if TYPE_CHECKING:
    from main_window.menu_bar_widget.menu_bar_widget import MenuBarWidget


class VisibilitySelector(ButtonSelector):
    def __init__(self, menu_bar_widget: "MenuBarWidget"):
        super().__init__(menu_bar_widget, "Visibility")
        self.settings_manager = self.main_window.settings_manager

    def on_button_clicked(self):
        dialog = VisibilityDialog(self)
        dialog.show_dialog()
