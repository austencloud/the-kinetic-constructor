from typing import TYPE_CHECKING
from main_window.settings_manager.autobuilder_settings import AutoBuilderSettings
from main_window.settings_manager.manual_builder_settings import ManualBuilderSettings

if TYPE_CHECKING:
    from main_window.settings_manager.settings_manager import SettingsManager


class BuilderSettings:
    DEFAULT_SETTINGS = {
        "auto_builder": {
            "circular_auto_builder": {
                "sequence_type": "circular",
                "sequence_length": 16,
                "max_turn_intensity": 1,
                "sequence_level": 1,
                "rotation_type": "quartered",
                "permutation_type": "rotated",
                "continuous_rotation": True,
            },
            "freeform_auto_builder": {
                "sequence_type": "freeform",
                "sequence_length": 16,
                "max_turn_intensity": 1,
                "sequence_level": 1,
                "continuous_rotation": True,
            },
            "current_auto_builder": "circular",
        },
        "manual_builder": {},
        "last_used_builder": "auto",
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self._load_builder_settings()

        # Initialize manual and auto builder settings
        self.auto_builder = AutoBuilderSettings(self.settings_manager)
        self.manual_builder = ManualBuilderSettings(self.settings_manager)  # Initialize manual builder settings

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
