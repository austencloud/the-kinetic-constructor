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
        self.settings = self.settings_manager.settings  # QSettings instance

    def get_filters(self) -> dict:
        return self.settings.value(
            "builder/manual_builder/filters",
            self.DEFAULT_SETTINGS["filters"],
            type=dict,
        )

    def set_filters(self, filters: dict):
        self.settings.setValue("builder/manual_builder/filters", filters)
