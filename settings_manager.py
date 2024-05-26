from datetime import datetime
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
            "current_user": "TacoCat",
            "user_profiles": {
                "TacoCat": {
                    "name": "TacoCat",
                },
            },
        },
        "grow_sequence": True,
    }

    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__()
        self.settings_json = get_user_editable_resource_path("user_settings.json")
        self.main_window = main_window
        self.settings = self.load_settings()
        self.prop_type_changer = PropTypeChanger(main_window)
        self.glyph_visibility_manager = GlyphVisibilityManager(main_window)
        self.grid_visibility_manager = GridVisibilityManager(self)

    def load_settings(self) -> dict[str, dict]:
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

    def get_grow_sequence(self) -> bool:
        return self.settings.get("grow_sequence", False)

    def set_grow_sequence(self, grow_sequence: bool) -> None:
        self.settings["grow_sequence"] = grow_sequence
        self.save_settings()

    def get_image_export_setting(self, key, default=None):
        image_export_settings: dict = self.settings.get("image_export_options", {})
        return image_export_settings.get(key, default)

    def set_setting(self, key, value):
        self.settings[key] = value
        self.save_settings()

    def set_image_export_setting(self, key, value):
        if "image_export_options" not in self.settings:
            self.settings["image_export_options"] = {}
        self.settings["image_export_options"][key] = value
        self.save_settings()

    def get_current_user_profile(self) -> dict:
        current_user = self.get_image_export_setting("current_user", "TacoCat")
        user_profiles = self.get_image_export_setting("user_profiles", {})
        return user_profiles.get(current_user, {})

    def add_or_update_user_profile(self, user_profile: dict) -> None:
        user_profiles = self.get_image_export_setting("user_profiles", {})
        user_profiles[user_profile["name"]] = user_profile
        self.set_image_export_setting("user_profiles", user_profiles)
        self.set_image_export_setting("current_user", user_profile["name"])

    def get_setting(self, key, default=None):
        return self.settings.get(key, default)
    

    def get_prop_type(self) -> PropType:
        return PropType[self.get_setting("prop_type", "Staff")]
    
    def set_prop_type(self, prop_type: PropType) -> None:
        self.set_setting("prop_type", prop_type.name)
        