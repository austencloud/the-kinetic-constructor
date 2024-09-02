from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class AutoBuilderSettings:
    DEFAULT_AUTO_BUILDER_SETTINGS = {
        "sequence_type": "Random Freeform",
        "sequence_length": 16,
        "turn_intensity": 50,
        "sequence_level": 1,  # 1: Level 1, 2: Level 2, 3: Level 3
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings.get(
            "auto_builder", self.DEFAULT_AUTO_BUILDER_SETTINGS
        )

    def get_auto_builder_setting(self, key: str):
        return self.settings.get(key, self.DEFAULT_AUTO_BUILDER_SETTINGS.get(key))

    def set_auto_builder_setting(self, key: str, value):
        self.settings[key] = value
        self.settings_manager.save_auto_builder_settings(self.settings)
