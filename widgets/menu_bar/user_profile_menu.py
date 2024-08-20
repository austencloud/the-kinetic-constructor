from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMenuBar, QMenu
from PyQt6.QtGui import QActionGroup, QAction

from Enums.PropTypes import PropType

if TYPE_CHECKING:
    from widgets.menu_bar.main_window_menu_bar import MainWindowMenuBar


class UserProfileMenu(QMenu):
    def __init__(self, menu_bar: "MainWindowMenuBar"):
        super().__init__("User Profile", menu_bar)
        self.menu_bar = menu_bar
        self.main_widget = menu_bar.main_widget
        self.user_manager = (
            self.main_widget.main_window.settings_manager.users.user_manager
        )
        user_profiles = self.user_manager.get_all_users()
        current_user = self.user_manager.get_current_user()

        user_action_group = QActionGroup(self)
        user_action_group.setExclusive(True)

        for user_name in user_profiles:
            action = QAction(user_name, self, checkable=True)
            action.triggered.connect(
                lambda checked, u=user_name: self._on_user_selection(u)
            )
            self.addAction(action)
            user_action_group.addAction(action)

            if user_name == current_user:
                action.setChecked(True)

        edit_users_action = QAction("Edit Users", self)
        edit_users_action.triggered.connect(self.user_manager.open_edit_users_dialog)
        self.addAction(edit_users_action)

    def _on_user_selection(self, user_name):
        self.user_manager.set_current_user(user_name)