# user_profile_selector.py
from typing import TYPE_CHECKING
from ..base_selector import LabelSelector
from .user_profile_dialog import UserProfileDialog

if TYPE_CHECKING:
    from main_window.menu_bar_widget.menu_bar_widget import MenuBarWidget


class UserProfileSelector(LabelSelector):
    def __init__(self, menu_bar_widget: "MenuBarWidget"):
        self.user_manager = menu_bar_widget.main_window.settings_manager.users.user_manager
        current_user = self.user_manager.get_current_user()
        super().__init__(menu_bar_widget, current_user)
        self.main_widget = menu_bar_widget.main_window.main_widget

    def on_label_clicked(self):
        dialog = UserProfileDialog(self)
        dialog.show_dialog()

    def set_current_user(self, user_name: str):
        self.set_display_text(user_name)
        self.user_manager.set_current_user(user_name)
        self.main_widget.sequence_properties_manager.update_sequence_properties()
