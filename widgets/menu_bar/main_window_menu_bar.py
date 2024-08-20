from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMenuBar
from widgets.menu_bar.user_profile_menu import UserProfileMenu
from widgets.menu_bar.backgrounds_menu import BackgroundsMenu
from widgets.menu_bar.prop_type_menu import PropTypeMenu
from widgets.menu_bar.settings_menu import SettingsMenu
from widgets.menu_bar.visibility_menu import VisibilityMenu

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class MainWindowMenuBar(QMenuBar):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__()
        self.main_widget = main_widget
        
        self.user_menu = UserProfileMenu(self)
        self.backgrounds_menu = BackgroundsMenu(self)
        self.prop_type_menu = PropTypeMenu(self)
        self.settings_menu = SettingsMenu(self)
        self.visibility_menu = VisibilityMenu(self)

        self.addMenu(self.settings_menu)
        self.addMenu(self.prop_type_menu)
        self.addMenu(self.visibility_menu)
        self.addMenu(self.backgrounds_menu)
        self.addMenu(self.user_menu)
