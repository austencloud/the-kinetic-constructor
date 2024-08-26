from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMenu
from PyQt6.QtGui import QActionGroup, QAction


if TYPE_CHECKING:
    from main_window.main_window_menu_bar import MainWindowMenuBar


class UserProfileMenu(QMenu):
    def __init__(self, menu_bar: "MainWindowMenuBar"):
        super().__init__("User Profile", menu_bar)
        self.menu_bar = menu_bar
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
        # update the current sequence json file to reflect the new user
        self.main_widget.json_manager.updater.update_sequence_properties()

    def populate_user_profiles_menu(self):
        # clear all the users without clearing the edit users action
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

        # move the edit users action to the bottom
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
