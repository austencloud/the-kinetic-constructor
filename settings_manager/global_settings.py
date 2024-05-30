from typing import TYPE_CHECKING
from Enums.PropTypes import PropType
from background_managers.aurora_background_manager import AuroraBackgroundManager
from background_managers.aurora_borealis_background_manager import (
    AuroraBorealisBackgroundManager,
)
from background_managers.particle_background_manager import ParticleBackgroundManager
from background_managers.rainbow_background_manager import RainbowBackgroundManager
from background_managers.startfield_background_manager import StarfieldBackgroundManager
from background_managers.water_ripple_background_manager import (
    WaterRipplesBackgroundManager,
)
from settings_manager.prop_type_changer import PropTypeChanger

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class GlobalSettings:
    DEFAULT_GLOBAL_SETTINGS = {
        "prop_type": "Staff",
        "background_type": "Aurora",
        "grow_sequence": True,
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings.get(
            "global_settings", self.DEFAULT_GLOBAL_SETTINGS
        )
        self.prop_type_changer = PropTypeChanger(self.settings_manager)

    def get_grow_sequence(self) -> bool:
        return self.settings.get("grow_sequence", False)

    def set_grow_sequence(self, grow_sequence: bool) -> None:
        self.settings["grow_sequence"] = grow_sequence
        self.settings_manager.save_settings()

    def get_prop_type(self) -> PropType:
        return PropType[self.settings.get("prop_type", "Staff")]

    def set_prop_type(self, prop_type: PropType) -> None:
        self.settings["prop_type"] = prop_type.name
        self.settings_manager.save_settings()

    def get_background_type(self) -> str:
        return self.settings.get("background_type", "Aurora")

    def set_background_type(self, background_type: str) -> None:
        self.settings["background_type"] = background_type
        self.settings_manager.save_settings()
        self.settings_manager.background_changed.emit(background_type)

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
