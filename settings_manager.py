import json
import os
from typing import TYPE_CHECKING
from Enums.PropTypes import PropType
from PyQt6.QtCore import QObject, pyqtSignal
from background_managers.aurora_background_manager import AuroraBackgroundManager
from background_managers.aurora_borealis_background_manager import (
    AuroraBorealisBackgroundManager,
)
from background_managers.background_manager import *
from background_managers.particle_background_manager import ParticleBackgroundManager
from background_managers.rainbow_background_manager import RainbowBackgroundManager
from background_managers.startfield_background_manager import StarfieldBackgroundManager
from background_managers.water_ripple_background_manager import (
    WaterRipplesBackgroundManager,
)
from path_helpers import get_user_editable_resource_path
from widgets.menu_bar.glyph_visibility_manager import GlyphVisibilityManager
from prop_type_changer import PropTypeChanger
from widgets.menu_bar.grid_visibility_manager import GridVisibilityManager
from widgets.notes_manager import NotesManager
from widgets.user_manager import UserManager


if TYPE_CHECKING:
    from main import MainWindow


class SettingsManager(QObject):
    background_changed: pyqtSignal = pyqtSignal(str)

    MAX_COLUMN_COUNT = 8
    MIN_COLUMN_COUNT = 3
    DEFAULT_SETTINGS = {
    "current_user": "AC",
    "current_note": "Created using The Kinetic Alphabet",
    "user_profiles": {
        "AC": {
            "name": "AC"
        },
        "Austen Cloud": {
            "name": "Austen Cloud"
        }
    },
    "notes": [
        "Created using The Kinetic Alphabet"
    ],
    "pictograph_size": 1,
    "prop_type": "Staff",
    "glyph_visibility": {
        "VTG": False,
        "TKA": True,
        "Elemental": False,
        "EndPosition": False
    },
    "grid_visibility": {
        "non_radial_points": True
    },
    "background_type": "AuroraBorealis",
    "grow_sequence": True,
    "image_export": {
        "include_start_position": False,
        "add_info": True,
        "open_directory_on_export": True,
        "current_user": "Jesus",
        "add_word": True
    }
}

    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__()
        self.settings_json = get_user_editable_resource_path("user_settings.json")
        self.main_window = main_window
        self.settings = self.load_settings()
        self.prop_type_changer = PropTypeChanger(main_window)
        self.glyph_visibility_manager = GlyphVisibilityManager(main_window)
        self.grid_visibility_manager = GridVisibilityManager(self)
        self.user_manager = UserManager(self)
        self.notes_manager = NotesManager(self)

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
        image_export_settings: dict = self.settings.get("image_export", {})
        return image_export_settings.get(key, default)

    def set_setting(self, key, value):
        self.settings[key] = value
        self.save_settings()

    def set_image_export_setting(self, key, value):
        if "image_export" not in self.settings:
            self.settings["image_export"] = {}
        self.settings["image_export"][key] = value
        self.save_settings()

    def get_current_user_profile(self) -> dict:
        current_user = self.get_image_export_setting("current_user", "TacoCat")
        user_profiles = self.get_image_export_setting("user_profiles", {})
        return user_profiles.get(current_user, {})

    def add_or_update_user_profile(self, user_profile: dict) -> None:
        user_profiles = self.settings["user_profiles"]
        user_profiles[user_profile["name"]] = user_profile
        self.settings["user_profiles"] = user_profiles

    def get_setting(self, key, default=None):
        return self.settings.get(key, default)

    def get_prop_type(self) -> PropType:
        return PropType[self.get_setting("prop_type", "Staff")]

    def set_prop_type(self, prop_type: PropType) -> None:
        self.set_setting("prop_type", prop_type.name)

    def get_background_type(self) -> str:
        return self.settings.get("background_type", "Rainbow")

    def set_background_type(self, background_type: str) -> None:
        self.settings["background_type"] = background_type
        self.save_settings()
        self.background_changed.emit(background_type)

    def setup_background_manager(self, widget):
        bg_type = self.get_background_type()
        if bg_type == "Rainbow":
            return RainbowBackgroundManager(widget)
        elif bg_type == "Starfield":
            return StarfieldBackgroundManager(widget)
        elif bg_type == "Particle":
            return ParticleBackgroundManager(widget)
        elif bg_type == "Aurora":
            return AuroraBackgroundManager(widget)
        elif bg_type == "AuroraBorealis":
            return AuroraBorealisBackgroundManager(widget)
        elif bg_type == "WaterRipples":
            return WaterRipplesBackgroundManager(widget)
        return None
