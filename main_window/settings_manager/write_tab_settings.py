from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class WriteTabSettings:
    DEFAULT_WRITE_TAB_SETTINGS = {
        "act_title": "Untitled Act",  # Default title if none saved
        "last_saved_act": None,  # Default to no saved act initially
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings.get(
            "write_tab", self.DEFAULT_WRITE_TAB_SETTINGS
        )

    def save_act_title(self, title: str) -> None:
        """Save the current act's title."""
        self.settings["act_title"] = title
        self.settings_manager.save_write_tab_settings(self.settings)

    def get_act_title(self) -> str:
        """Retrieve the saved act title."""
        return self.settings.get(
            "act_title", self.DEFAULT_WRITE_TAB_SETTINGS["act_title"]
        )

    def save_last_act(self, act_data: dict) -> None:
        """Save the most recent act data."""
        self.settings["last_saved_act"] = act_data
        self.settings_manager.save_settings()

    def load_last_act(self) -> dict:
        """Load the most recent act data."""
        return self.settings.get("last_saved_act", None)
