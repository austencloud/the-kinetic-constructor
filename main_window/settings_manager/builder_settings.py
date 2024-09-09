from typing import TYPE_CHECKING
from main_window.settings_manager.autobuilder_settings import AutoBuilderSettings

if TYPE_CHECKING:
    from main_window.settings_manager.settings_manager import SettingsManager


class BuilderSettings:
    DEFAULT_SETTINGS = {
        "last_used_builder": "manual",  # "manual" or "auto"
        "last_used_auto_builder": "freeform",  # "freeform" or "circular"
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self._load_builder_settings()

        # Initialize manual and auto builder settings
        self.auto_builder = AutoBuilderSettings(self.settings_manager)
        # self.manual_builder_settings = ManualBuilderSettings(self.settings_manager)

    def _load_builder_settings(self):
        return self.settings_manager.settings.get("builder", self.DEFAULT_SETTINGS)

    def get_last_used_builder(self) -> str:
        return self.settings.get("last_used_builder", "manual")

    def set_last_used_builder(self, builder_type: str):
        """Save the last used builder ('manual' or 'auto')."""
        self.settings["last_used_builder"] = builder_type
        self._save_builder_settings()

    def _save_builder_settings(self):
        self.settings_manager.save_builder_settings(self.settings)
