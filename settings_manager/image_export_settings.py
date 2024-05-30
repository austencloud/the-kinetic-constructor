from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class ImageExportSettings:
    DEFAULT_IMAGE_EXPORT_SETTINGS = {
        "include_start_position": False,
        "add_info": True,
        "open_directory_on_export": True,
        "add_word": True,
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings.get(
            "image_export_settings", self.DEFAULT_IMAGE_EXPORT_SETTINGS
        )

    def get_image_export_setting(self, key, default=None):
        return self.settings.get(key, default)

    def set_image_export_setting(self, key, value):
        self.settings[key] = value
        self.settings_manager.save_settings()
