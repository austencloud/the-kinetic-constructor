import json
import os
from typing import TYPE_CHECKING
from Enums.PropTypes import PropTypes
from widgets.menu_bar.glyph_visibility_manager import GlyphVisibilityToggler
from prop_type_changer import PropTypeChanger


if TYPE_CHECKING:
    from main import MainWindow


class SettingsManager:
    MAX_COLUMN_COUNT = 8
    MIN_COLUMN_COUNT = 3

    def __init__(self, main_window: "MainWindow", settings_file="user_settings.json"):
        self.settings_file = settings_file
        self.main_window = main_window
        self.settings = self.load_settings()
        self.prop_type_changer = PropTypeChanger(main_window)
        self.glyph_visibility_manager = GlyphVisibilityToggler(main_window)

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

    def get_prop_type(self) -> PropTypes:
        prop_type = self.get_setting("prop_type")
        for prop_type_enum in PropTypes:
            if str(prop_type_enum.name) == prop_type:
                return prop_type_enum

    def set_prop_type(self, prop_type: str) -> None:
        self.set_setting("prop_type", prop_type)

    def set_setting(self, key, value) -> None:
        self.settings[key] = value
        self.save_settings()

    def apply_settings(self) -> None:
        """Apply user settings to the application."""
        self._apply_pictograph_size()
        self.prop_type_changer.apply_prop_type()
        self.glyph_visibility_manager.toggle_visibility()
        self.main_window.main_widget.main_tab_widget.codex.update_pictographs()

    def _apply_pictograph_size(self) -> None:
        pictograph_size = self.get_setting("pictograph_size", 1)
        inverted_value = self.MAX_COLUMN_COUNT - (pictograph_size - 1)
        column_count = max(
            self.MIN_COLUMN_COUNT, min(inverted_value, self.MAX_COLUMN_COUNT)
        )
        self.main_window.main_widget.main_tab_widget.codex.scroll_area.display_manager.COLUMN_COUNT = (
            column_count
        )

    def get_glyph_visibility(self, glyph_type: str) -> bool:
        return self.settings.get("glyph_visibility", {}).get(glyph_type, True)

    def set_glyph_visibility(self, glyph_type: str, visible: bool) -> None:
        if "glyph_visibility" not in self.settings:
            self.settings["glyph_visibility"] = {}
        self.settings["glyph_visibility"][glyph_type] = visible
        self.save_settings()
        self._apply_glyph_visibility()

    def _apply_glyph_visibility(self):
        for pictograph_list in self.main_window.main_widget.all_pictographs.values():
            for pictograph in pictograph_list.values():
                if pictograph.view.isVisible():
                    self.glyph_visibility_manager.apply_current_visibility_settings(
                        pictograph
                    )
