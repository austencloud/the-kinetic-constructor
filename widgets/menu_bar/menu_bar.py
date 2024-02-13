# MenuBar.py
from PyQt6.QtWidgets import QMenuBar, QMenu
from typing import TYPE_CHECKING
from PyQt6.QtGui import QAction, QActionGroup
from utilities.TypeChecking.prop_types import PropTypes
from widgets.menu_bar.preferences_dialog import PreferencesDialog

if TYPE_CHECKING:
    from ..main_widget.main_widget import MainWidget


class MainWindowMenuBar(QMenuBar):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self._setup_menu()
        self._setup_settings_menu()

    def _setup_settings_menu(self) -> None:
        # Create the settings menu
        settings_menu = self.addMenu("Settings")

        # Create the action for opening the preferences dialog
        preferences_action = QAction("Preferences", self)
        preferences_action.triggered.connect(self.open_preferences_dialog)
        settings_menu.addAction(preferences_action)

        # Create a submenu for prop types
        prop_type_menu = QMenu("Set Prop Type", self)
        settings_menu.addMenu(prop_type_menu)

        # Create action group for prop types to ensure exclusivity
        prop_type_action_group = QActionGroup(self)
        prop_type_action_group.setExclusive(True)

        # Populate the prop type submenu
        for prop_type in PropTypes:
            action = QAction(prop_type.name, self, checkable=True)
            action.triggered.connect(
                lambda checked, pt=prop_type: self.set_prop_type(pt)
            )
            prop_type_menu.addAction(action)
            prop_type_action_group.addAction(action)

            # Check the action if it matches current settings
            if self.main_widget.prop_type == prop_type:
                action.setChecked(True)

    def set_prop_type(self, prop_type: PropTypes):
        # Set the prop type in main_widget or settings_manager
        self.main_widget.prop_type_selector.prop_type_changed(prop_type.name)
        # Refresh the UI or specific components as needed
        # For example, re-rendering pictographs, updating settings, etc.
        print(f"Prop type set to: {prop_type.name}")

    def open_preferences_dialog(self) -> None:
        self.preferences_dialog = self.main_widget.preferences_dialog
        self.preferences_dialog.setup_layout()
        self.preferences_dialog.load_initial_settings()
        self.preferences_dialog.exec()

    def _setup_menu(self) -> None:
        refresh_action = QAction("Refresh Placements", self)
        refresh_action.triggered.connect(
            self.main_widget.special_placement_loader.refresh_placements
        )
        self.addAction(refresh_action)

        # Optionally, other menu items and actions can be added here.

        # Set the font size for the menu items
        font = self.font()  # Gets the current font
        font.setPointSize(12)  # Adjust the font size as desired
        self.setFont(font)
