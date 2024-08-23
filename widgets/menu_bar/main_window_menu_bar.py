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

        self.user_profiles_menu = UserProfileMenu(self)
        self.backgrounds_menu = BackgroundsMenu(self)
        self.prop_type_menu = PropTypeMenu(self)
        self.settings_menu = SettingsMenu(self)
        self.visibility_menu = VisibilityMenu(self)

        self.addMenu(self.settings_menu)
        self.addMenu(self.prop_type_menu)
        self.addMenu(self.visibility_menu)
        self.addMenu(self.backgrounds_menu)
        self.addMenu(self.user_profiles_menu)

    def resize_menu_bar(self):
        # Set the height of the menu bar
        self.setFixedHeight(self.main_widget.height() // 30)
        self.setFixedWidth(self.main_widget.width())

        # Set the font size based on a percentage of the main widget's height
        font = self.font()
        calculated_font_size = max(
            8, min(self.main_widget.height() // 40, 14)
        )  # Ensures the font size stays between 8 and 20
        font.setPointSize(calculated_font_size)
        self.setFont(font)

        # Ensure the menu bar is correctly positioned and visible
        self.move(0, 0)
        self.show()
