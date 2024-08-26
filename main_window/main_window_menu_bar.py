from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMenuBar
from widgets.menu_bar.user_profile_menu import UserProfileMenu
from widgets.menu_bar.backgrounds_menu import BackgroundsMenu
from widgets.menu_bar.prop_type_menu import PropTypeMenu
from widgets.menu_bar.settings_menu import SettingsMenu
from widgets.menu_bar.visibility_menu import VisibilityMenu
from PyQt6.QtWidgets import QMenu

if TYPE_CHECKING:
    from main_window.main_window import MainWindow
    from main_window.main_widget.main_widget import MainWidget


class MainWindowMenuBar(QMenuBar):
    def __init__(self, main_window: "MainWindow"):
        super().__init__()
        self.main_widget = main_window.main_widget

        self.user_profiles_menu = UserProfileMenu(self)
        self.backgrounds_menu = BackgroundsMenu(self)
        self.prop_type_menu = PropTypeMenu(self)
        self.visibility_menu = VisibilityMenu(self)

        self.addMenu(self.prop_type_menu)
        self.addMenu(self.visibility_menu)
        self.addMenu(self.backgrounds_menu)
        self.addMenu(self.user_profiles_menu)

    def resize_menu_bar(self):
        self.setFixedHeight(self.main_widget.height() // 30)
        self.setFixedWidth(self.main_widget.width())

        # Set the font size based on a percentage of the main widget's height
        font = self.font()
        font_size = 14
        font.setPointSize(font_size)
        self.setFont(font)

        # Apply the same font size to each menu's actions (dropdown items)
        for menu in self.findChildren(QMenu):
            menu_font = menu.font()
            menu_font.setPointSize(font_size)
            menu.setFont(menu_font)
            for action in menu.actions():
                action_font = action.font()
                action_font.setPointSize(font_size)
                action.setFont(action_font)

        # Ensure the menu bar is correctly positioned and visible
        self.move(0, 0)
        self.show()
