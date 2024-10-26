from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class WriteTabSettings:
    DEFAULT_WRITE_TAB_SETTINGS = {
        "act_title": "Untitled Act",
        "last_saved_act": None,
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings  # QSettings instance

    def save_act_title(self, title: str) -> None:
        """Save the current act's title."""
        self.settings.setValue("write_tab/act_title", title)

    def get_act_title(self) -> str:
        """Retrieve the saved act title with a default fallback."""
        return self.settings.value(
            "write_tab/act_title", self.DEFAULT_WRITE_TAB_SETTINGS["act_title"]
        )

    def save_last_act(self, act_data: dict) -> None:
        """Save the most recent act data."""
        self.settings.setValue("write_tab/last_saved_act", act_data)

    def load_last_act(self) -> dict:
        """Load the most recent act data with None as the default."""
        return self.settings.value("write_tab/last_saved_act", None, type=dict)
