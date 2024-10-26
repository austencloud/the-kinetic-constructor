from typing import TYPE_CHECKING
from main_window.settings_manager.autobuilder_settings import AutoBuilderSettings
from main_window.settings_manager.manual_builder_settings import ManualBuilderSettings

if TYPE_CHECKING:
    from main_window.settings_manager.settings_manager import SettingsManager


class BuilderSettings:
    DEFAULT_BUILDER_SETTINGS = {
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
        self.settings = self.settings_manager.settings  # QSettings instance

        # Initialize auto and manual builder settings
        self.auto_builder = AutoBuilderSettings(self.settings_manager)
        self.manual_builder = ManualBuilderSettings(self.settings_manager)

    def get_last_used_builder(self) -> str:
        return self.settings.value(
            "builder/last_used_builder", self.DEFAULT_BUILDER_SETTINGS["last_used_builder"]
        )

    def set_last_used_builder(self, builder_type: str):
        self.settings.setValue("builder/last_used_builder", builder_type)
