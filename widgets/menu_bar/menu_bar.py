from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QMenuBar
from Enums.PropTypes import PropType
from PyQt6.QtGui import QIcon, QAction, QActionGroup

if TYPE_CHECKING:
    from ..main_widget.main_widget import MainWidget


class MainWindowMenuBar(QMenuBar):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__()
        self.main_widget = main_widget
        self.glyph_visibility_manager = (
            self.main_widget.main_window.settings_manager.glyph_visibility_manager
        )
        self.grid_visibility_manager = (
            self.main_widget.main_window.settings_manager.grid_visibility_manager
        )

        self._setup_menu()
        self._setup_settings_menu()
        self._setup_visibility_menu()
        self._setup_prop_type_menu()
        self._setup_backgrounds_menu()

    def _setup_backgrounds_menu(self):
        backgrounds_menu = self.addMenu("Backgrounds")
        background_action_group = QActionGroup(self)
        background_action_group.setExclusive(True)

        # List of background managers available
        background_types = [
            "Rainbow",
            "Starfield",
            "Particle",
            "Aurora",
            "AttractionParticles",
            "AuroraBorealis",
            "WaterRipples",
        ]
        current_bg = self.main_widget.main_window.settings_manager.get_setting(
            "background_type", default="Rainbow"
        )

        for bg_type in background_types:
            action = QAction(bg_type, self, checkable=True)
            action.setChecked(current_bg == bg_type)
            action.triggered.connect(
                lambda checked, bg=bg_type: (
                    self.set_background_type(bg) if checked else None
                )
            )
            backgrounds_menu.addAction(action)
            background_action_group.addAction(action)

    def set_background_type(self, bg_type: str):
        self.main_widget.main_window.settings_manager.set_setting(
            "background_type", bg_type
        )
        self.main_widget.apply_background(bg_type)

    def _setup_prop_type_menu(self):
        prop_type_menu = self.addMenu("Set Prop Type")
        prop_type_action_group = QActionGroup(self)
        prop_type_action_group.setExclusive(True)

        for prop_type in PropType:
            action = QAction(prop_type.name, self, checkable=True)
            action.triggered.connect(
                lambda checked, pt=prop_type: self.set_prop_type(pt)
            )
            prop_type_menu.addAction(action)
            prop_type_action_group.addAction(action)

            if self.main_widget.prop_type == prop_type:
                action.setChecked(True)

    def _setup_settings_menu(self):
        settings_menu = self.addMenu("Settings")
        preferences_action = QAction("Preferences", self)
        preferences_action.triggered.connect(self.open_preferences_dialog)
        settings_menu.addAction(preferences_action)

    def _setup_visibility_menu(self):
        visibility_menu = self.addMenu("Visibility")

        # Glyph visibility toggles
        for glyph_type in ["VTG", "TKA", "Elemental", "EndPosition"]:
            action = QAction(f"{glyph_type} Glyph", self, checkable=True)
            action.setChecked(
                self.glyph_visibility_manager.get_glyph_visibility(glyph_type)
            )
            action.triggered.connect(
                lambda checked, gt=glyph_type: self.toggle_glyph_visibility(gt, checked)
            )
            visibility_menu.addAction(action)

        non_radial_action = QAction("Non-Radial Points", self, checkable=True)
        non_radial_action.setChecked(
            self.main_widget.main_window.settings_manager.grid_visibility_manager.non_radial_visible
        )
        non_radial_action.triggered.connect(
            self.grid_visibility_manager.toggle_visibility
        )
        visibility_menu.addAction(non_radial_action)

    def toggle_glyph_visibility(self, glyph_type: str, visible: bool):
        self.glyph_visibility_manager = self.glyph_visibility_manager
        self.glyph_visibility_manager.set_glyph_visibility(glyph_type, visible)
        self.glyph_visibility_manager.apply_glyph_visibility()

    def set_prop_type(self, prop_type: PropType):
        self.main_widget.prop_type_selector.on_prop_type_changed(prop_type.name)
        print(f"Prop type set to: {prop_type.name}")

    def open_preferences_dialog(self):
        self.preferences_dialog = self.main_widget.preferences_dialog
        self.preferences_dialog.load_initial_settings()
        self.preferences_dialog.exec()

    def _setup_menu(self):
        font = self.font()
        font.setPointSize(12)
        self.setFont(font)
