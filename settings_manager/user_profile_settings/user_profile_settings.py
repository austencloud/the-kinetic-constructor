from typing import TYPE_CHECKING

from settings_manager.user_profile_settings.notes_manager.notes_manager import NotesManager
from settings_manager.user_profile_settings.user_manager.user_manager import UserManager


if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class UserProfileSettings:
    DEFAULT_USER_SETTINGS = {
        "current_user": "Austen Cloud",
        "user_profiles": {
            "AC": {"name": "AC"}
        },
        "current_note": "Created using The Kinetic Alphabet",
        "saved_notes": ["Created using The Kinetic Alphabet"],
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings.get(
            "user_profile", self.DEFAULT_USER_SETTINGS
        )
        self.user_manager = UserManager(self)
        self.notes_manager = NotesManager(self)

    def get_current_user_profile(self) -> dict:
        current_user = self.settings.get("current_user", "Austen Cloud")
        user_profiles = self.settings.get("user_profiles", {})
        return user_profiles.get(current_user, {})

    def add_or_update_user_profile(self, user_profile: dict) -> None:
        user_profiles = self.settings.get("user_profiles", {})
        user_profiles[user_profile["name"]] = user_profile
        self.settings["user_profiles"] = user_profiles
        self.settings_manager.save_settings()
