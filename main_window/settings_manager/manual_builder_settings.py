# manual_builder_settings.py
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.settings_manager.settings_manager import SettingsManager


class ManualBuilderSettings:
    DEFAULT_SETTINGS = {
        "filters": {
            "continuous_motions": True,
            "prop_reversals": True,
            "hand_reversals": True,
        }
    }

    def __init__(self, settings_manager: "SettingsManager"):
        self.settings_manager = settings_manager
        self.settings = self._load_manual_builder_settings()

    def _load_manual_builder_settings(self):
        return self.settings_manager.settings.get("builder", {}).get(
            "manual_builder", self.DEFAULT_SETTINGS
        )

    def get_filters(self) -> dict:
        return self.settings.get("filters", self.DEFAULT_SETTINGS["filters"])

    def set_filters(self, filters: dict):
        self.settings["filters"] = filters
        self._save_manual_builder_settings()

    def _save_manual_builder_settings(self):
        builder_settings = self.settings_manager.settings.get("builder", {})
        builder_settings["manual_builder"] = self.settings
        self.settings_manager.settings["builder"] = builder_settings
        self.settings_manager.save_settings()
