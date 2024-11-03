from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class AutoBuilderSettings:
    DEFAULT_FREEFORM_SETTINGS = {
        "sequence_type": "freeform",
        "sequence_length": 16,
        "max_turn_intensity": 1,
        "sequence_level": 1,
        "continuous_rotation": False,
    }

    DEFAULT_CIRCULAR_SETTINGS = {
        "sequence_type": "circular",
        "sequence_length": 16,
        "max_turn_intensity": 1,
        "sequence_level": 1,
        "rotation_type": "quartered",
        "permutation_type": "rotated",
        "continuous_rotation": False,
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings  # QSettings instance

    def get_auto_builder_setting(self, key: str, builder_type: str):
        """Retrieve a setting for a specific builder type."""
        prefix = f"builder/auto_builder/{builder_type}_auto_builder/"
        default = (
            self.DEFAULT_FREEFORM_SETTINGS.get(key)
            if builder_type == "freeform"
            else self.DEFAULT_CIRCULAR_SETTINGS.get(key)
        )
        return self.settings.value(prefix + key, default)

    def set_auto_builder_setting(self, key: str, value, builder_type: str):
        """Set a setting for a specific builder type."""
        prefix = f"builder/auto_builder/{builder_type}_auto_builder/"
        self.settings.setValue(prefix + key, value)

    def get_current_auto_builder(self) -> str:
        return self.settings.value(
            "builder/auto_builder/current_auto_builder", "circular"
        )

    def update_current_auto_builder(self, builder_type: str):
        self.settings.setValue(
            "builder/auto_builder/current_auto_builder", builder_type
        )
