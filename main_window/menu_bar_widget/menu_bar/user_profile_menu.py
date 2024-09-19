from PyQt6.QtGui import QAction, QActionGroup
from typing import TYPE_CHECKING

from .hoverable_menu import HoverableMenu

if TYPE_CHECKING:
    from .menu_bar import MenuBar


class UserProfileMenu(HoverableMenu):
    def __init__(self, menu_bar: "MenuBar"):
        super().__init__("User Profile", menu_bar)
        self.main_widget = menu_bar.main_widget
        self.user_manager = (
            self.main_widget.main_window.settings_manager.users.user_manager
        )

        self.user_action_group = QActionGroup(self)
        self.user_action_group.setExclusive(True)

        self.edit_users_action = QAction("Edit Users", self)
        self.edit_users_action.triggered.connect(
            self.user_manager.open_edit_users_dialog
        )
        self.populate_user_profiles_menu()
        self.addAction(self.edit_users_action)

    def _on_user_selection(self, user_name):
        self.set_current_user_in_user_menu(user_name)
        self.main_widget.json_manager.updater.update_sequence_properties()

    def populate_user_profiles_menu(self):
        for action in self.actions():
            if action.text() != "Edit Users":
                self.removeAction(action)
        user_profiles = self.user_manager.get_all_users()
        current_user = self.user_manager.get_current_user()
        for user_name in user_profiles:
            action = QAction(user_name, self, checkable=True)
            action.triggered.connect(
                lambda checked, u=user_name: self._on_user_selection(u)
            )
            self.addAction(action)
            self.user_action_group.addAction(action)

            if user_name == current_user:
                action.setChecked(True)

        self.addAction(self.edit_users_action)

    def set_current_user_in_user_menu(self, user_name):
        if user_name != "Edit Users":
            self.user_manager.user_profile_settings.settings["current_user"] = user_name
            self.user_manager.user_profile_settings.settings_manager.save_settings()
        for action in self.actions():
            if action.text() == user_name:
                action.setChecked(True)
            else:
                action.setChecked(False)
