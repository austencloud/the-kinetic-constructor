from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QComboBox, QInputDialog
from PyQt6.QtCore import QObject
if TYPE_CHECKING:
    from settings_manager import SettingsManager


class UserManager(QObject):
    def __init__(self, settings_manager: "SettingsManager"):
        super().__init__()
        self.settings_manager = settings_manager
        self.user_combo_box = QComboBox()
        self._populate_user_profiles()

    def _populate_user_profiles(self):
        user_profiles = self.settings_manager.settings.get("user_profiles", {})
        current_user = self.settings_manager.get_image_export_setting(
            "current_user", "TacoCat"
        )
        for user_name in user_profiles.keys():
            self.user_combo_box.addItem(user_name)
        if current_user in user_profiles:
            index = self.user_combo_box.findText(current_user)
            if index != -1:
                self.user_combo_box.setCurrentIndex(index)
        self.user_combo_box.currentIndexChanged.connect(self._update_current_user)

    def _update_current_user(self):
        selected_user = self.user_combo_box.currentText()
        if selected_user:
            self.settings_manager.set_setting("current_user", selected_user)

    def add_new_user(self):
        text, ok = QInputDialog.getText(
            self.user_combo_box, "Add New User", "Enter user name:"
        )
        if ok and text:
            new_user_profile = {"name": text}
            self.settings_manager.add_or_update_user_profile(new_user_profile)
            self.user_combo_box.addItem(text)
            self.user_combo_box.setCurrentText(text)
