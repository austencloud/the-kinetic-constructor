from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QComboBox, QInputDialog
from PyQt6.QtCore import QObject

from edit_user_profiles_dialog import EditUserProfilesDialog

if TYPE_CHECKING:
    from settings_manager import SettingsManager


class UserManager(QObject):
    def __init__(self, settings_manager: "SettingsManager"):
        super().__init__()
        self.settings_manager = settings_manager
        self.user_combo_box = QComboBox()
        self._populate_user_profiles()

    def _populate_user_profiles(self):
        self.user_combo_box.clear()
        user_profiles = self.settings_manager.settings.get("user_profiles", {})
        current_user = self.settings_manager.get_image_export_setting(
            "current_user", "TacoCat"
        )
        for user_name in user_profiles.keys():
            self.user_combo_box.addItem(user_name)
        self.user_combo_box.addItem("Edit Users")
        if current_user in user_profiles:
            index = self.user_combo_box.findText(current_user)
            if index != -1:
                self.user_combo_box.setCurrentIndex(index)
        self.user_combo_box.currentIndexChanged.connect(self._update_current_user)

    def _update_current_user(self):
        selected_user = self.user_combo_box.currentText()
        if selected_user == "Edit Users":
            self.open_edit_users_dialog()
        else:
            self.settings_manager.set_setting("current_user", selected_user)

    def open_edit_users_dialog(self):
        dialog = EditUserProfilesDialog(self)
        if dialog.exec():
            self._populate_user_profiles()

    def get_all_users(self):
        return list(self.settings_manager.settings.get("user_profiles", {}).keys())

    def add_new_user(self, user_name):
        user_profiles = self.settings_manager.settings.get("user_profiles", {})
        if user_name in user_profiles:
            return False
        user_profiles[user_name] = {"name": user_name}
        self.settings_manager.settings["user_profiles"] = user_profiles
        self.settings_manager.set_setting("current_user", user_name)
        return True

    def remove_user(self, user_name):
        user_profiles = self.settings_manager.settings.get("user_profiles", {})
        if user_name in user_profiles:
            del user_profiles[user_name]
            self.settings_manager.settings["user_profiles"] = user_profiles
            if self.user_combo_box.currentText() == user_name:
                self.user_combo_box.setCurrentIndex(0)  # Set to the first user
            return True
        return False

    def save_users(self):
        self.settings_manager.save_settings()
