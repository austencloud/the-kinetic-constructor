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
        self.options: list[str] = self.users + ["Edit Users"]

    def show_dialog(self):
        self.dialog = OptionsDialog(
            selector=self.user_profile_selector,
            options=self.options,
            callback=self.option_selected,
        )
        self.dialog.show_dialog(self.user_profile_selector.label)

    def option_selected(self, option: str):
        if option == "Edit Users":
            self.user_manager.open_edit_users_dialog()
            self.refresh_options()
            self.show_dialog()
        else:
            self.user_profile_selector.set_current_user(option)
        self.dialog.accept()

    def populate_user_profiles_dialog(self):
        for option in self.options:
            if option != "Edit Users":
                self.options.remove(option)
        self.refresh_options()
        current_user = self.user_manager.get_current_user()
        self.dialog.select_option(current_user)

    def close_dialog(self):
        self.dialog.accept()