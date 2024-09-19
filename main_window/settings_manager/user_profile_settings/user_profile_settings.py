from typing import TYPE_CHECKING
from .notes_manager.notes_manager import NotesManager
from .user_manager.user_manager import UserManager

if TYPE_CHECKING:
    from ..settings_manager import SettingsManager


class UserProfileSettings:
    DEFAULT_USER_SETTINGS = {
        "current_user": "",
        "user_profiles": {},
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

