# user_profile_dialog.py
from typing import TYPE_CHECKING
from ..options_dialog import OptionsDialog

if TYPE_CHECKING:
    from .user_profile_selector import UserProfileSelector


class UserProfileDialog:
    def __init__(self, user_profile_selector: "UserProfileSelector"):
        self.user_profile_selector = user_profile_selector
        self.user_manager = user_profile_selector.user_manager
        self.refresh_options()

    def refresh_options(self):
        self.users = self.user_manager.get_all_users()
        self.options = self.users + ["Edit Users"]

    def show_dialog(self):
        dialog = OptionsDialog(
            selector=self.user_profile_selector,
            options=self.options,
            callback=self.option_selected,
        )
        dialog.show_dialog(self.user_profile_selector.label)

    def option_selected(self, option: str):
        if option == "Edit Users":
            self.user_manager.open_edit_users_dialog()
            # Refresh options after editing
            self.refresh_options()
            # Optionally, re-open the dialog to show updated users
            self.show_dialog()
        else:
            self.user_profile_selector.set_current_user(option)
