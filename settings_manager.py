# In SettingsManager.py
import json
import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MainWindow


class SettingsManager:
    def __init__(
        self, main_window: "MainWindow", settings_file="user_settings.json"
    ) -> None:
        self.settings_file = settings_file
        self.main_window = main_window
        self.settings = self.load_settings()
        self.main_window.main_widget.main_tab_widget.codex.scroll_area.display_manager.COLUMN_COUNT = self.get_setting(
            "column_count", 8
        )

    def load_settings(self) -> dict:
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as file:
                return json.load(file)
        else:
            return {}

    def save_settings(self) -> None:
        with open(self.settings_file, "w") as file:
            json.dump(self.settings, file, indent=4)

    def get_setting(self, key, default=None) -> str:
        return self.settings.get(key, default)

    def set_setting(self, key, value) -> None:
        self.settings[key] = value
        self.save_settings()
