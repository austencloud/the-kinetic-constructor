from typing import TYPE_CHECKING, Optional
from Enums.PropTypes import PropType
from background_managers.aurora_background_manager import AuroraBackgroundManager
from background_managers.aurora_borealis_background_manager import (
    AuroraBorealisBackgroundManager,
)
from background_managers.background_manager import BackgroundManager
from background_managers.particle_background_manager import ParticleBackgroundManager
from background_managers.rainbow_background_manager import RainbowBackgroundManager
from background_managers.startfield_background_manager import StarfieldBackgroundManager

from settings_manager.prop_type_changer import PropTypeChanger

if TYPE_CHECKING:
    from settings_manager.settings_manager import SettingsManager


class GlobalSettings:
    DEFAULT_GLOBAL_SETTINGS = {
        "prop_type": "staff",
        "background_type": "Aurora",
        "grow_sequence": True,
        "current_tab": "sequence_builder",
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings = self.settings_manager.settings.get(
            "global", self.DEFAULT_GLOBAL_SETTINGS
        )
        self.prop_type_changer = PropTypeChanger(self.settings_manager)
        self.main_widget = None

    def get_grow_sequence(self) -> bool:
        return self.settings.get("grow_sequence", False)

    def set_grow_sequence(self, grow_sequence: bool) -> None:
        self.settings["grow_sequence"] = grow_sequence
        self.settings_manager.save_settings()

    def get_prop_type(self) -> PropType:
        return PropType[self.settings.get("prop_type", "staff")]

    def set_prop_type(self, prop_type: PropType) -> None:
        self.settings["prop_type"] = prop_type.name
        self.settings_manager.save_settings()

    def get_background_type(self) -> str:
        return self.settings.get("background_type", "Aurora")

    def set_background_type(self, background_type: str) -> None:
        self.settings["background_type"] = background_type
        self.settings_manager.save_settings()
        self.settings_manager.background_changed.emit(background_type)

    def setup_background_manager(self, widget) -> BackgroundManager:
        if not self.main_widget:
            self.main_widget = self.settings_manager.main_window.main_widget
        bg_type = self.get_background_type()
        return self.get_background_manager(bg_type, widget)

    def get_background_manager(
        self, bg_type: str, widget
    ) -> Optional[BackgroundManager]:
        self.update_font_colors(bg_type)
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
        return None

    def update_font_colors(self, bg_type):
        self.main_widget.top_builder_widget.sequence_widget.current_word_label.setStyleSheet(
            f"color: {self.get_font_color(bg_type)};"
        )
        self.main_widget.top_builder_widget.sequence_widget.difficulty_label.setStyleSheet(
            f"color: {self.get_font_color(bg_type)};"
        )
        self.main_widget.top_builder_widget.sequence_builder.start_pos_picker.choose_your_start_pos_label.setStyleSheet(
            f"color: {self.get_font_color(bg_type)};"
        )
        self.main_widget.dictionary_widget.browser.options_widget.sort_by_label.setStyleSheet(
            f"color: {self.get_font_color(bg_type)};"
        )
        self.main_widget.dictionary_widget.browser.options_widget.style_buttons()
        self.main_widget.dictionary_widget.browser.nav_sidebar.set_styles()
        self.main_widget.dictionary_widget.preview_area.image_label.style_placeholder()

    def get_font_color(self, bg_type: str) -> str:
        if bg_type in ["Rainbow", "AuroraBorealis", "Aurora"]:
            return "black"
        return "white"

    def set_current_tab(self, tab: str) -> None:
        self.settings["current_tab"] = tab
        self.settings_manager.save_settings()

    def get_current_tab(self) -> str:
        return self.settings.get("current_tab")
