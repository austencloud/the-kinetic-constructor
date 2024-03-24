import json
import os
from typing import TYPE_CHECKING
from Enums.PropTypes import PropType
from resource_path import resource_path
from widgets.menu_bar.glyph_visibility_manager import GlyphVisibilityManager
from prop_type_changer import PropTypeChanger


if TYPE_CHECKING:
    from main import MainWindow


class SettingsManager:
    MAX_COLUMN_COUNT = 8
    MIN_COLUMN_COUNT = 3

    def __init__(
        self,
        main_window: "MainWindow",
    ):
        self.settings_file = resource_path("user_settings.json")
        self.main_window = main_window
        self.settings = self.load_settings()
        self.prop_type_changer = PropTypeChanger(main_window)
        self.glyph_visibility_manager = GlyphVisibilityManager(main_window)

    def load_settings(
        self,
    ) -> dict[str, int | str, str | str, dict[str, bool]]:
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

    def get_prop_type(self) -> PropType:
        prop_type = self.get_setting("prop_type")
        for prop_type_enum in PropType:
            if str(prop_type_enum.name) == prop_type:
                return prop_type_enum

    def set_prop_type(self, prop_type: str) -> None:
        self.set_setting("prop_type", prop_type)

    def set_setting(self, key, value) -> None:
        self.settings[key] = value
        self.save_settings()

    def _apply_pictograph_size(self) -> None:
        pictograph_size = self.get_setting("pictograph_size", 1)
        inverted_value = self.MAX_COLUMN_COUNT - (pictograph_size - 1)
        column_count = max(
            self.MIN_COLUMN_COUNT, min(inverted_value, self.MAX_COLUMN_COUNT)
        )
        self.main_window.main_widget.main_tab_widget.letterbook.scroll_area.display_manager.COLUMN_COUNT = (
            column_count
        )

    def get_default_orientation(self, prop_type: str, hand: str) -> str:
        return self.get_setting(f"default_{hand}_orientation_{prop_type}", "in")

    def set_default_orientation(
        self, prop_type: str, hand: str, orientation: str
    ) -> None:
        self.set_setting(f"default_{hand}_orientation_{prop_type}", orientation)

    def get_word_length_visibility(self) -> dict:
        # Returns a dictionary with lengths as keys and visibility (True/False) as values
        return self.get_setting(
            "word_length_visibility",
            {2: True, 3: True, 4: True, 5: False, 6: False, 7: False, 8: False},
        )

    def set_word_length_visibility(self, lengths_visibility: dict) -> None:
        # Ensure keys are strings for JSON compatibility
        corrected_visibility = {
            str(key): value for key, value in lengths_visibility.items()
        }
        self.set_setting("word_length_visibility", corrected_visibility)
