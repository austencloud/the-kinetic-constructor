from typing import Optional, TYPE_CHECKING
from Enums.PropTypes import PropType
from main_window.menu_bar_widget.background_selector.background_managers.aurora.aurora_background_manager import (
    AuroraBackgroundManager,
)
from main_window.menu_bar_widget.background_selector.background_managers.aurora_borealis_background_manager import (
    AuroraBorealisBackgroundManager,
)
from main_window.menu_bar_widget.background_selector.background_managers.background_manager import (
    BackgroundManager,
)
from main_window.menu_bar_widget.background_selector.background_managers.bubbles_background_manager import (
    BubblesBackgroundManager,
)
from main_window.menu_bar_widget.background_selector.background_managers.snowfall.snowfall_background_manager import (
    SnowfallBackgroundManager,
)
from main_window.menu_bar_widget.background_selector.background_managers.starfield.starfield_background_manager import (
    StarfieldBackgroundManager,
)
from .prop_type_changer import PropTypeChanger
from .font_color_updater import FontColorUpdater

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget
    from ..settings_manager import SettingsManager


class GlobalSettings:
    def __init__(self, settings_manager: "SettingsManager") -> None:
        self.settings = settings_manager.settings
        self.settings_manager = settings_manager
        self.prop_type_changer = PropTypeChanger(self.settings_manager)
        self.font_color_updater = FontColorUpdater()
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

    # Background Manager Setup
    def setup_background_manager(
        self, widget, is_splash_screen=False
    ) -> BackgroundManager:
        bg_type = self.get_background_type()
        return self.get_background_manager(bg_type, widget, is_splash_screen)

    def get_background_manager(
        self, bg_type: str, widget, is_splash_screen=False
    ) -> Optional[BackgroundManager]:
        if not is_splash_screen:
            main_widget = getattr(
                self.settings_manager.main_window, "main_widget", None
            )
            if main_widget:
                self.font_color_updater.update_main_widget_font_colors(
                    main_widget, bg_type
                )
            else:
                # main_widget is not set yet; skip updating font colors
                pass
        else:
            self.font_color_updater.apply_splash_screen_font_colors(widget, bg_type)

        # Map the background type to the respective manager
        background_manager_map = {
            "Starfield": StarfieldBackgroundManager,
            "Aurora": AuroraBackgroundManager,
            "AuroraBorealis": AuroraBorealisBackgroundManager,
            "Snowfall": SnowfallBackgroundManager,
            "Bubbles": BubblesBackgroundManager,
        }
        manager_class = background_manager_map.get(bg_type)
        return manager_class(widget) if manager_class else None

    # Font Color Management
    def get_current_font_color(self) -> str:
        return self.font_color_updater.get_font_color(self.get_background_type())

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
