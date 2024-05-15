import json
import os
from typing import TYPE_CHECKING
from Enums.PropTypes import PropType
from PyQt6.QtCore import QObject, pyqtSignal
from path_helpers import get_user_editable_resource_path
from widgets.menu_bar.glyph_visibility_manager import GlyphVisibilityManager
from prop_type_changer import PropTypeChanger
from widgets.menu_bar.grid_visibility_manager import GridVisibilityManager


if TYPE_CHECKING:
    from main import MainWindow


class SettingsManager(QObject):
    background_changed: pyqtSignal = pyqtSignal(str)


    MAX_COLUMN_COUNT = 8
    MIN_COLUMN_COUNT = 3
    DEFAULT_SETTINGS = {
        "pictograph_size": 1,
        "prop_type": "Staff",
        "glyph_visibility": {
            "VTG": False,
            "TKA": True,
            "Elemental": True,
            "EndPosition": True,
        },
        "default_left_orientation": "out",
        "default_right_orientation": "out",
        "default_left_orientation_Hand": "out",
        "default_right_orientation_Hand": "in",
        "word_length_visibility": {
            "2": False,
            "3": False,
            "4": False,
            "5": False,
            "6": False,
            "7": False,
            "8": False,
        },
        "image_export_options": {
            "include_start_pos": False,
            "user_name": "TacoCat",
        },
    }

    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__()
        self.settings_json = get_user_editable_resource_path("user_settings.json")
        self.main_window = main_window
        self.settings = self.load_settings()
        self.prop_type_changer = PropTypeChanger(main_window)
        self.glyph_visibility_manager = GlyphVisibilityManager(main_window)
        self.grid_visibility_manager = GridVisibilityManager(self)

    def load_settings(self) -> dict:
        if os.path.exists(self.settings_json):
            with open(self.settings_json, "r") as file:
                return json.load(file)
        else:
            self.save_settings(self.DEFAULT_SETTINGS)
            return self.DEFAULT_SETTINGS

    def save_settings(self, settings=None) -> None:
        if settings is None:
            settings = self.settings
        with open(self.settings_json, "w") as file:
            json.dump(settings, file, indent=4)

    def get_image_export_setting(self, key, default=None):
        # Retrieve specific image export settings
        image_export_settings: dict = self.settings.get("image_export", {})
        return image_export_settings.get(key, default)

    def set_image_export_setting(self, key, value):
        # Set specific image export settings
        if "image_export" not in self.settings:
            self.settings["image_export"] = {}
        self.settings["image_export"][key] = value
        self.save_settings()  # Save settings to file

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
        if key == "background_type" and self.settings[key] != value:
            self.background_changed.emit(value)

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
