from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class WriteTabSettings:
    DEFAULT_WRITE_TAB_SETTINGS = {}

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings.get(
            "write_tab", self.DEFAULT_WRITE_TAB_SETTINGS
        )
