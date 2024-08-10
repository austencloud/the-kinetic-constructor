from typing import TYPE_CHECKING
from Enums.PropTypes import PropType
from background_managers.aurora_background_manager import AuroraBackgroundManager
from background_managers.aurora_borealis_background_manager import (
    AuroraBorealisBackgroundManager,
)
from background_managers.particle_background_manager import ParticleBackgroundManager
from background_managers.rainbow_background_manager import RainbowBackgroundManager
from background_managers.startfield_background_manager import StarfieldBackgroundManager

from settings_manager.prop_type_changer import PropTypeChanger

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class DictionarySettings:
    DEFAULT_DICTIONARY_SETTINGS = {
        "sort_method": "sequence_length",
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
        self.settings_manager.save_dictionary_settings(
            self.settings
        )
