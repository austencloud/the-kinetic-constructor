# MenuBar.py
from PyQt6.QtWidgets import QMenuBar, QMenu
from typing import TYPE_CHECKING
from PyQt6.QtGui import QAction, QActionGroup
from Enums.PropTypes import PropTypes

if TYPE_CHECKING:
    from ..main_widget.main_widget import MainWidget


class MainWindowMenuBar(QMenuBar):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self._setup_menu()
        self._setup_settings_menu()
        self._setup_glyph_visibility_menu()

    def _setup_settings_menu(self) -> None:
        settings_menu = self.addMenu("Settings")
        preferences_action = QAction("Preferences", self)
        preferences_action.triggered.connect(self.open_preferences_dialog)
        settings_menu.addAction(preferences_action)
        prop_type_menu = QMenu("Set Prop Type", self)
        settings_menu.addMenu(prop_type_menu)
        prop_type_action_group = QActionGroup(self)
        prop_type_action_group.setExclusive(True)
        for prop_type in PropTypes:
            action = QAction(prop_type.name, self, checkable=True)
            action.triggered.connect(
                lambda checked, pt=prop_type: self.set_prop_type(pt)
            )
            prop_type_menu.addAction(action)
            prop_type_action_group.addAction(action)

            if self.main_widget.prop_type == prop_type:
                action.setChecked(True)

    def _setup_glyph_visibility_menu(self):
        glyph_visibility_menu = self.addMenu("Glyph Visibility")
        for glyph_type in ["VTG", "TKA", "Elemental"]:
            action = QAction(f"{glyph_type} Glyph", self, checkable=True)
            action.setChecked(
                self.main_widget.main_window.settings_manager.glyph_visibility_manager.get_glyph_visibility(
                    glyph_type
                )
            )
            action.triggered.connect(
                lambda checked, gt=glyph_type: self.toggle_glyph_visibility(gt, checked)
            )
            glyph_visibility_menu.addAction(action)

    def toggle_glyph_visibility(self, glyph_type: str, visible: bool):
        self.main_widget.main_window.settings_manager.glyph_visibility_manager.set_glyph_visibility(
            glyph_type, visible
        )
        self.main_widget.main_window.settings_manager.glyph_visibility_manager.apply_glyph_visibility()

    def set_prop_type(self, prop_type: PropTypes):
        self.main_widget.prop_type_selector.prop_type_changed(prop_type.name)

        print(f"Prop type set to: {prop_type.name}")

    def open_preferences_dialog(self) -> None:
        self.preferences_dialog = self.main_widget.preferences_dialog
        self.preferences_dialog.setup_layout()
        self.preferences_dialog.load_initial_settings()
        self.preferences_dialog.exec()

    def _setup_menu(self) -> None:
        font = self.font()
        font.setPointSize(12)
        self.setFont(font)
