import json
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MainWindow


class SettingsManager:
    MAX_COLUMN_COUNT = 8
    MIN_COLUMN_COUNT = 3

    def __init__(self, main_window: "MainWindow", settings_file="user_settings.json"):
        self.settings_file = settings_file
        self.main_window = main_window
        self.settings = self.load_settings()
        self.apply_settings()  # Apply settings on initialization

    def load_settings(self) -> dict:
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as file:
                return json.load(file)
        else:
            return {}

    def save_settings(self) -> None:
        with open(self.settings_file, "w") as file:
            json.dump(self.settings, file, indent=4)

    def get_setting(self, key, default=None):
        return self.settings.get(key, default)

    def set_setting(self, key, value):
        self.settings[key] = value
        self.save_settings()

    def apply_settings(self):
        """Apply user settings to the application."""
        # Get pictograph size from settings, with a default value
        pictograph_size = self.get_setting("pictograph_size", 1)
        # Convert pictograph size to column count
        inverted_value = self.MAX_COLUMN_COUNT - (pictograph_size - 1)
        column_count = max(
            self.MIN_COLUMN_COUNT, min(inverted_value, self.MAX_COLUMN_COUNT)
        )
        # Apply the column count
        self.main_window.main_widget.main_tab_widget.codex.scroll_area.display_manager.COLUMN_COUNT = (
            column_count
        )
        # Update the pictographs
        self.main_window.main_widget.main_tab_widget.codex.scroll_area.update_pictographs()
