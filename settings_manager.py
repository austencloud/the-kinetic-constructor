import json
from math import pi
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
        self.apply_settings()

    def load_settings(self) -> dict:
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as file:
                return json.load(file)
        else:
            return {}

    def save_settings(self) -> None:
        with open(self.settings_file, "w") as file:
            json.dump(self.settings, file, indent=4)

    def get_setting(self, key, default=None) -> any:
        return self.settings.get(key, default)

    def get_prop_type(self) -> str:
        return self.get_setting("prop_type")  # Default to STAFF

    def set_prop_type(self, prop_type: str) -> None:
        self.set_setting("prop_type", prop_type)

    def set_setting(self, key, value) -> None:
        self.settings[key] = value
        self.save_settings()

    def apply_settings(self) -> None:
        """Apply user settings to the application."""
        self._apply_pictograph_size()
        self._apply_prop_type()
        self.main_window.main_widget.main_tab_widget.codex.scroll_area.update_pictographs()

    def _apply_prop_type(self) -> None:
        prop_type = self.get_prop_type()
        self.main_window.main_widget.prop_type = prop_type
        self.update_props_to_type(prop_type)

    def update_props_to_type(self, new_prop_type) -> None:
        for (
            pictograph
        ) in (
            self.main_window.main_widget.main_tab_widget.codex.scroll_area.pictographs.values()
        ):
            for color, prop in pictograph.props.items():
                new_prop = pictograph.initializer.prop_factory.create_prop_of_type(
                    prop, new_prop_type
                )
                pictograph.props[color].deleteLater()
                pictograph.props[color] = new_prop
                pictograph.addItem(new_prop)
                pictograph.motions[color].prop = pictograph.props[color]
                pictograph.props[color].motion.attr_manager.update_prop_ori()
                pictograph.props[color].updater.update_prop()
                pictograph.updater.update_pictograph()

    def _apply_pictograph_size(self) -> None:
        pictograph_size = self.get_setting("pictograph_size", 1)
        inverted_value = self.MAX_COLUMN_COUNT - (pictograph_size - 1)
        column_count = max(
            self.MIN_COLUMN_COUNT, min(inverted_value, self.MAX_COLUMN_COUNT)
        )
        self.main_window.main_widget.main_tab_widget.codex.scroll_area.display_manager.COLUMN_COUNT = (
            column_count
        )
