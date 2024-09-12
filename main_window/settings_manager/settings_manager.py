import json
import os
from typing import TYPE_CHECKING
from PyQt6.QtCore import QObject, pyqtSignal

from main_window.settings_manager.builder_settings import BuilderSettings
from main_window.settings_manager.sequence_sharing_settings import (
    SequenceSharingSettings,
)

from ..settings_manager.dictionary_settings import DictionarySettings
from ..settings_manager.image_export_settings import ImageExportSettings
from ..settings_manager.sequence_layout_settings import SequenceLayoutSettings
from ..settings_manager.user_profile_settings.user_profile_settings import (
    UserProfileSettings,
)
from .visibility_settings.visibility_settings import VisibilitySettings
from utilities.path_helpers import get_user_editable_resource_path
from .global_settings.global_settings import GlobalSettings

if TYPE_CHECKING:
    from main_window.main_window import MainWindow


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
        self.dictionary_settings = DictionarySettings(self)
        self.sequence_layout = SequenceLayoutSettings(self)
        self.builder_settings = BuilderSettings(self)
        self.sequence_sharing = SequenceSharingSettings(self)  # New sharing settings

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
                "sequence_layout": SequenceLayoutSettings.DEFAULT_LAYOUT_SETTINGS,
                "builder": BuilderSettings.DEFAULT_SETTINGS,
                "sequence_sharing": SequenceSharingSettings.DEFAULT_SEQUENCE_SHARING_SETTINGS,
            }
            self.save_settings(default_settings)
            return default_settings

    def save_settings(self, settings=None) -> None:
        if settings is None:
            settings = self.settings
        with open(self.settings_json, "w", encoding="utf-8") as file:
            json.dump(settings, file, ensure_ascii=False, indent=4)

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

    def save_layout_settings(self, settings) -> None:
        self.settings["sequence_layout"] = settings
        self.save_settings()

    def save_auto_builder_settings(self, settings, builder_type) -> None:
        self.settings["builder"]["auto_builder"][builder_type] = settings
        self.save_settings()

    def save_builder_settings(self, settings) -> None:
        self.settings["builder"] = settings
        self.save_settings()

    def save_sequence_sharing_settings(self, settings) -> None:
        self.settings["sequence_sharing"] = settings
        self.save_settings()
