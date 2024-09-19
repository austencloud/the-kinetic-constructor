from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class DictionarySettings:
    DEFAULT_DICTIONARY_SETTINGS = {
        "sort_method": "sequence_length",
        "current_section": "starting_letter",
        "current_filter": {},
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings.get(
            "dictionary", self.DEFAULT_DICTIONARY_SETTINGS
        )

    def get_sort_method(self) -> str:
        return self.settings.get("sort_method", "sequence_length")

    def set_sort_method(self, sort_method: str) -> None:
        self.settings["sort_method"] = sort_method
        self.settings_manager.save_dictionary_settings(self.settings)

    def get_current_filter(self) -> dict:
        return self.settings.get("current_filter", {})

    def set_current_filter(self, current_filter: dict) -> None:
        self.settings["current_filter"] = current_filter
        self.settings_manager.save_dictionary_settings(self.settings)

    def get_current_section(self) -> str:
        return self.settings.get("current_section", "starting_letter")
    
    def set_current_section(self, section: str) -> None:
        self.settings["current_section"] = section
        self.settings_manager.save_dictionary_settings(self.settings)