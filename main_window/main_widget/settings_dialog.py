from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QListWidget,
    QListWidgetItem,
    QWidget,
    QLabel,
    QCheckBox,
    QComboBox,
    QPushButton,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from Enums.PropTypes import PropType

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class SettingsDialog(QDialog):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.setWindowTitle("Settings")
        self.setMinimumSize(600, 400)
        self._setup_ui()

    def _setup_ui(self):
        # Main layout
        self.main_layout = QHBoxLayout(self)
        self.setLayout(self.main_layout)

        # Left: Category list
        self.category_list = QListWidget(self)
        self.category_list.setFixedWidth(200)
        self.category_list.itemClicked.connect(self._on_category_selected)
        self.main_layout.addWidget(self.category_list)

        # Right: Scrollable content area
        self.content_scroll_area = QScrollArea(self)
        self.content_scroll_area.setWidgetResizable(True)
        self.content_container = QWidget(self.content_scroll_area)
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_container.setLayout(self.content_layout)
        self.content_scroll_area.setWidget(self.content_container)
        self.main_layout.addWidget(self.content_scroll_area)

        # Populate categories
        self._add_categories()

    def _add_categories(self):
        categories = ["User Profile", "Prop Type", "Background", "Visibility"]
        for category in categories:
            item = QListWidgetItem(category)
            self.category_list.addItem(item)

        # Load the first category by default
        if self.category_list.count() > 0:
            self.category_list.setCurrentRow(0)
            self._load_category("User Profile")

    def _on_category_selected(self, item: QListWidgetItem):
        self._load_category(item.text())

    def _load_category(self, category: str):
        # Clear the existing content
        while self.content_layout.count():
            widget = self.content_layout.takeAt(0).widget()
            if widget:
                widget.deleteLater()

        # Populate with new content based on the category
        if category == "User Profile":
            self._load_user_profile_settings()
        elif category == "Prop Type":
            self._load_prop_type_settings()
        elif category == "Background":
            self._load_background_settings()
        elif category == "Visibility":
            self._load_visibility_settings()

    def _load_user_profile_settings(self):
        user_manager = self.main_widget.settings_manager.users.user_manager
        users = user_manager.get_all_users()
        current_user = user_manager.get_current_user()

        font = QFont()
        font.setPointSize(14)

        for user in users:
            button = QPushButton(user)
            button.setFont(font)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setStyleSheet("margin: 5px;")
            button.clicked.connect(lambda _, u=user: self._set_current_user(u))
            self.content_layout.addWidget(button)

        edit_users_button = QPushButton("Edit Users")
        edit_users_button.setFont(font)
        edit_users_button.setCursor(Qt.CursorShape.PointingHandCursor)
        edit_users_button.clicked.connect(user_manager.open_edit_users_dialog)
        self.content_layout.addWidget(edit_users_button)

    def _set_current_user(self, user_name: str):
        user_manager = self.main_widget.settings_manager.users.user_manager
        user_manager.set_current_user(user_name)
        self.main_widget.sequence_properties_manager.update_sequence_properties()

    def _load_prop_type_settings(self):
        settings_manager = self.main_widget.settings_manager
        prop_types = [
            "Hand",
            "Staff",
            "Club",
            "Fan",
            "Triad",
            "Minihoop",
            "Buugeng",
            "Sword",
            "Ukulele",
        ]
        current_prop_type = settings_manager.global_settings.get_prop_type().name

        font = QFont()
        font.setPointSize(14)

        for prop in prop_types:
            button = QPushButton(prop)
            button.setFont(font)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setStyleSheet("margin: 5px;")
            button.clicked.connect(
                lambda _, p=prop: self._set_current_prop_type(PropType.get_prop_type(p))
            )
            self.content_layout.addWidget(button)

    def _set_current_prop_type(self, prop_type: str):
        settings_manager = self.main_widget.settings_manager
        settings_manager.global_settings.set_prop_type(prop_type)
        self.main_widget.settings_manager.global_settings.prop_type_changer.apply_prop_type()

    def _load_background_settings(self):
        settings_manager = self.main_widget.settings_manager
        current_background = settings_manager.global_settings.get_background_type()

        backgrounds = [
            "Starfield",
            "Aurora",
            "Snowfall",
            "Bubbles",
        ]
        font = QFont()
        font.setPointSize(14)

        for background in backgrounds:
            button = QPushButton(background)
            button.setFont(font)
            button.setCursor(Qt.CursorShape.PointingHandCursor)
            button.setStyleSheet("margin: 5px;")
            button.clicked.connect(lambda _, b=background: self._set_background(b))
            self.content_layout.addWidget(button)

    def _set_background(self, background: str):
        settings_manager = self.main_widget.settings_manager
        settings_manager.global_settings.set_background_type(background)
        self.main_widget.background_widget.apply_background()

    def _load_visibility_settings(self):
        glyph_visibility_manager = (
            self.main_widget.settings_manager.visibility.glyph_visibility_manager
        )
        grid_visibility_manager = (
            self.main_widget.settings_manager.visibility.grid_visibility_manager
        )

        font = QFont()
        font.setPointSize(14)

        glyph_types = ["TKA", "VTG", "Elemental", "Positions", "Reversals"]
        for glyph in glyph_types:
            checkbox = QCheckBox(glyph)
            checkbox.setChecked(glyph_visibility_manager.should_glyph_be_visible(glyph))
            checkbox.setFont(font)
            checkbox.stateChanged.connect(
                lambda state, g=glyph: self._toggle_glyph_visibility(g, state)
            )
            self.content_layout.addWidget(checkbox)

        non_radial_checkbox = QCheckBox("Non-Radial Points")
        non_radial_checkbox.setChecked(grid_visibility_manager.non_radial_visible)
        non_radial_checkbox.setFont(font)
        non_radial_checkbox.stateChanged.connect(
            lambda state: self._toggle_non_radial_visibility(state)
        )
        self.content_layout.addWidget(non_radial_checkbox)

    def _toggle_glyph_visibility(self, glyph: str, state: int):
        is_checked = state == Qt.CheckState.Checked.value
        self.main_widget.settings_manager.visibility.set_glyph_visibility(
            glyph, is_checked
        )

    def _toggle_non_radial_visibility(self, state: int):
        is_checked = state == Qt.CheckState.Checked.value
        grid_visibility_manager = (
            self.main_widget.settings_manager.visibility.grid_visibility_manager
        )
        grid_visibility_manager.set_non_radial_visibility(is_checked)
