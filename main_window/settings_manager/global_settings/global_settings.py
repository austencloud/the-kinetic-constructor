from typing import Optional, TYPE_CHECKING
from Enums.PropTypes import PropType
from main_window.menu_bar_widget.background_selector.backgrounds.aurora.aurora_background import (
    AuroraBackground,
)
from main_window.menu_bar_widget.background_selector.backgrounds.aurora_borealis_background import (
    AuroraBorealisBackground,
)
from main_window.menu_bar_widget.background_selector.backgrounds.base_background import (
    BaseBackground,
)
from main_window.menu_bar_widget.background_selector.backgrounds.bubbles_background import (
    BubblesBackground,
)
from main_window.menu_bar_widget.background_selector.backgrounds.snowfall.snowfall_background import (
    SnowfallBackground,
)
from main_window.menu_bar_widget.background_selector.backgrounds.starfield.starfield_background import (
    StarfieldBackground,
)
from .prop_type_changer import PropTypeChanger
from .main_widget_font_color_updater import MainWidgetFontColorUpdater

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from ..settings_manager import SettingsManager


class GlobalSettings:
    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings = settings_manager.settings
        self.settings_manager = settings_manager
        self.prop_type_changer = PropTypeChanger(self.settings_manager)
        self.main_widget: "MainWidget" = None

    # Getter and Setter for Grow Sequence
    def get_grow_sequence(self) -> bool:
        return self.settings.value("global/grow_sequence", True, type=bool)

    def set_grow_sequence(self, grow_sequence: bool) -> None:
        self.settings.setValue("global/grow_sequence", grow_sequence)

    # Getter and Setter for Prop Type
    def get_prop_type(self) -> PropType:
        prop_type_key = self.settings.value("global/prop_type", "Staff").capitalize()
        return PropType[prop_type_key]

    def set_prop_type(self, prop_type: PropType) -> None:
        self.settings.setValue("global/prop_type", prop_type.name)
        self.prop_type_changer.apply_prop_type()  # PropTypeChanger usage

    # Getter and Setter for Background Type
    def get_background_type(self) -> str:
        return self.settings.value("global/background_type", "Aurora")

    def set_background_type(self, background_type: str) -> None:
        self.settings.setValue("global/background_type", background_type)
        self.settings_manager.background_changed.emit(background_type)

    # Font Color Management
    def get_current_font_color(self) -> str:
        return self.main_widget.font_color_updater.get_font_color(
            self.get_background_type()
        )

    # Getter and Setter for Current Tab
    def get_current_tab(self) -> str:
        return self.settings.value("global/current_tab", "sequence_builder")

    def set_current_tab(self, tab: str) -> None:
        self.settings.setValue("global/current_tab", tab)

    # Getter and Setter for Grid Mode
    def get_grid_mode(self) -> str:
        return self.settings.value("global/grid_mode", "diamond")

    def set_grid_mode(self, grid_mode: str) -> None:
        self.settings.setValue("global/grid_mode", grid_mode)

    # Getter and Setter for Welcome Screen Visibility
    def get_show_welcome_screen(self) -> bool:
        return self.settings.value("global/show_welcome_screen", True, type=bool)

    def set_show_welcome_screen(self, show_welcome_screen: bool) -> None:
        self.settings.setValue("global/show_welcome_screen", show_welcome_screen)
