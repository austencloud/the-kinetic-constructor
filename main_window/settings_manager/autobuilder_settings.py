from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class AutoBuilderSettings:
    DEFAULT_FREEFORM_SETTINGS = {
        "sequence_type": "freeform",
        "sequence_length": 16,
        "max_turns": 50,
        "max_turn_intensity": 50,
        "sequence_level": 1,  # 1: Level 1, 2: Level 2, 3: Level 3
    }

    DEFAULT_CIRCULAR_SETTINGS = {
        "sequence_type": "circular",
        "sequence_length": 4,  # Circular builder requires multiples of 4
        "max_turns": 50,
        "max_turn_intensity": 50,
        "sequence_level": 1,
        "rotation_type": "quartered",
        "permutation_type": "rotational",
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.circular_settings = self._load_builder_settings("circular")
        self.freeform_settings = self._load_builder_settings("freeform")

    def _load_builder_settings(self, builder_type):
        """Load settings based on the builder type."""
        if builder_type == "freeform":
            return self.settings_manager.settings.get("auto_builder").get(
                "freeform_auto_builder", self.DEFAULT_FREEFORM_SETTINGS
            )

        elif builder_type == "circular":
            return self.settings_manager.settings.get("auto_builder").get(
                "circular_auto_builder", self.DEFAULT_CIRCULAR_SETTINGS
            )
        else:
            raise ValueError(f"Unknown builder type: {builder_type}")

    def get_auto_builder_setting(self, key: str, builder_type: str):
        """Retrieve a setting for the current builder."""
        if builder_type == "freeform":
            settings = self.freeform_settings
        elif builder_type == "circular":
            settings = self.circular_settings
        return settings.get(
            key,
            (
                self.DEFAULT_FREEFORM_SETTINGS.get(key)
                if builder_type == "freeform"
                else self.DEFAULT_CIRCULAR_SETTINGS.get(key)
            ),
        )

    def get_auto_builder_settings(self, builder_type: str) -> dict:
        """Retrieve all settings for the current builder."""
        if builder_type == "freeform":
            return self.freeform_settings
        elif builder_type == "circular":
            return self.circular_settings

    def set_auto_builder_setting(self, key: str, value, builder_type: str):
        """Set a setting for the current builder."""
        if builder_type == "freeform":
            settings = self.freeform_settings
        elif builder_type == "circular":
            settings = self.circular_settings
        settings[key] = value
        self._save_builder_settings(builder_type)

    def _save_builder_settings(self, builder_type: str):
        """Save the settings for the specific builder."""
        if builder_type == "freeform":
            self.settings_manager.save_auto_builder_settings(
                self.freeform_settings, "freeform_auto_builder"
            )
        elif builder_type == "circular":
            self.settings_manager.save_auto_builder_settings(
                self.circular_settings, "circular_auto_builder"
            )
