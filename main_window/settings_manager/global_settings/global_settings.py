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
from .prop_type_changer import PropTypeChanger
from PyQt6.QtGui import QFont

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from splash_screen import SplashScreen
    from ..settings_manager import SettingsManager


class GlobalSettings:
    DEFAULT_GLOBAL_SETTINGS = {
        "prop_type": "staff",
        "background_type": "Aurora",
        "grow_sequence": True,
        "current_tab": "sequence_builder",
    }

    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings_manager = settings_manager
        self.settings: dict = self.settings_manager.settings.get(
            "global", self.DEFAULT_GLOBAL_SETTINGS
        )
        self.prop_type_changer = PropTypeChanger(self.settings_manager)
        self.main_widget: "MainWidget" = None

    def get_grow_sequence(self) -> bool:
        return self.settings.get("grow_sequence", False)

    def set_grow_sequence(self, grow_sequence: bool) -> None:
        self.settings["grow_sequence"] = grow_sequence
        self.settings_manager.save_settings()

    def get_prop_type(self) -> PropType:
        # Ensure the key is in the correct case
        prop_type_key = self.settings.get("prop_type", "Staff").capitalize()
        return PropType[prop_type_key]

    def set_prop_type(self, prop_type: PropType) -> None:
        self.settings["prop_type"] = prop_type.name
        self.settings_manager.save_settings()

    def get_background_type(self) -> str:
        return self.settings.get("background_type", "Aurora")

    def set_background_type(self, background_type: str) -> None:
        self.settings["background_type"] = background_type
        self.settings_manager.save_settings()
        self.settings_manager.background_changed.emit(background_type)

    def setup_background_manager(
        self, widget, is_splash_screen=False
    ) -> BackgroundManager:
        if not is_splash_screen:
            if not self.main_widget:
                self.main_widget = self.settings_manager.main_window.main_widget
        bg_type = self.get_background_type()
        return self.get_background_manager(bg_type, widget, is_splash_screen)

    def get_background_manager(
        self, bg_type: str, widget, is_splash_screen=False
    ) -> Optional[BackgroundManager]:
        if not is_splash_screen:
            self.update_main_widget_font_colors(bg_type)
        else:
            self.update_splash_screen_font_colors(widget, bg_type)
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

    def update_main_widget_font_colors(self, bg_type):
        font = QFont()

        self.main_widget.top_builder_widget.sequence_widget.current_word_label.setStyleSheet(
            f"color: {self.get_font_color(bg_type)};"
        )
        self.main_widget.top_builder_widget.sequence_widget.difficulty_label.setStyleSheet(
            f"color: {self.get_font_color(bg_type)};"
        )
        self.main_widget.top_builder_widget.sequence_builder.manual_builder.start_pos_picker.choose_your_start_pos_label.setStyleSheet(
            f"color: {self.get_font_color(bg_type)};"
        )
        # update the auto builder fonts, both circular and freeform

        self.main_widget.top_builder_widget.sequence_builder.auto_builder.freeform_builder_frame.update_font_colors(
            self.get_font_color(bg_type)
        )
        self.main_widget.top_builder_widget.sequence_builder.auto_builder.circular_builder_frame.update_font_colors(
            self.get_font_color(bg_type)
        )

        self.main_widget.dictionary_widget.browser.options_widget.sort_widget.sort_by_label.setStyleSheet(
            f"color: {self.get_font_color(bg_type)};"
        )
        self.main_widget.dictionary_widget.browser.options_widget.sort_widget.style_buttons()
        self.main_widget.dictionary_widget.browser.nav_sidebar.set_styles()
        self.main_widget.dictionary_widget.preview_area.image_label.style_placeholder()

    def update_splash_screen_font_colors(
        self, splash_screen: "SplashScreen", bg_type: str
    ):
        splash_screen.title_label.setStyleSheet(
            f"color: {self.get_font_color(bg_type)};"
        )
        splash_screen.currently_loading_label.setStyleSheet(
            f"color: {self.get_font_color(bg_type)};"
        )
        splash_screen.created_by_label.setStyleSheet(
            f"color: {self.get_font_color(bg_type)};"
        )
        splash_screen.progress_bar.percentage_label.setStyleSheet(
            f"color: {self.get_font_color(bg_type)};"
        )
        splash_screen.progress_bar.loading_label.setStyleSheet(
            f"color: {self.get_font_color(bg_type)};"
        )

    def get_font_color(self, bg_type: str) -> str:
        if bg_type in ["Rainbow", "AuroraBorealis", "Aurora"]:
            return "black"
        return "white"

    def set_current_tab(self, tab: str) -> None:
        self.settings["current_tab"] = tab
        self.settings_manager.save_settings()

    def get_current_tab(self) -> str:
        return self.settings.get("current_tab")
