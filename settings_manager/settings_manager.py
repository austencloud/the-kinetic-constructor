import json
import os
from typing import TYPE_CHECKING
from PyQt6.QtCore import QObject, pyqtSignal
from Enums.PropTypes import PropType
from settings_manager.dictionary_settings import DictionarySettings
from settings_manager.image_export_settings import ImageExportSettings
from settings_manager.user_profile_settings import UserProfileSettings
from settings_manager.visibility_settings import VisibilitySettings
from widgets.path_helpers.path_helpers import get_user_editable_resource_path
from .global_settings import GlobalSettings

if TYPE_CHECKING:
    from main import MainWindow


class SettingsManager(QObject):
    background_changed: pyqtSignal = pyqtSignal(str)

    def __init__(self, main_window: "MainWindow") -> None:
        super().__init__()
        self.settings_json = get_user_editable_resource_path("settings.json")
        self.main_window = main_window
        self.settings = self.load_settings()
        self.global_settings = GlobalSettings(self)
        self.image_export = ImageExportSettings(self)
        self.users = UserProfileSettings(self)
        self.visibility = VisibilitySettings(self)
        self.dictionary = DictionarySettings(self)

    def load_settings(self) -> dict:
        if os.path.exists(self.settings_json):
            with open(self.settings_json, "r") as file:
                return json.load(file)
        else:
            default_settings = {
                "global": GlobalSettings.DEFAULT_GLOBAL_SETTINGS,
                "image_export": ImageExportSettings.DEFAULT_IMAGE_EXPORT_SETTINGS,
                "user_profile": UserProfileSettings.DEFAULT_USER_SETTINGS,
                "visibility": VisibilitySettings.DEFAULT_VISIBILITY_SETTINGS,
                "dictionary": DictionarySettings.DEFAULT_DICTIONARY_SETTINGS,
            }
            self.save_settings(default_settings)
            return default_settings

    def save_settings(self, settings=None) -> None:
        if settings is None:
            settings = self.settings
        with open(self.settings_json, "w") as file:
            json.dump(settings, file, indent=4)

    def save_image_export_settings(self, settings) -> None:
        self.settings["image_export"] = settings
        self.save_settings()

    def save_user_profile_settings(self, settings) -> None:
        self.settings["user_profile"] = settings
        self.save_settings()

    def save_visibility_settings(self, settings) -> None:
        self.settings["visibility"] = settings
        self.save_settings()

    def save_global_settings(self, settings) -> None:
        self.settings["global"] = settings
        self.save_settings()

    def save_dictionary_settings(self, settings) -> None:
        self.settings["dictionary"] = settings
        self.save_settings()