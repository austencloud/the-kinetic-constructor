# PropTypeSelector.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QGroupBox, QFormLayout, QComboBox
from utilities.TypeChecking.prop_types import *

if TYPE_CHECKING:
    from widgets.menu_bar.preferences_dialog import PreferencesDialog


class PropTypeSelector(QGroupBox):
    def __init__(self, preferences_dialog: "PreferencesDialog") -> None:
        super().__init__("Prop Type Selector")
        self.preferences_dialog = preferences_dialog
        self._setup_prop_type_combobox()
        self._setup_layout()

    def _setup_prop_type_combobox(self) -> None:
        self.prop_type_combobox = QComboBox()
        self.prop_type_combobox.addItems(
            [
                STAFF,
                BIGSTAFF,
                CLUB,
                BUUGENG,
                FAN,
                TRIAD,
                MINIHOOP,
                BIGHOOP,
                DOUBLESTAR,
                QUIAD,
                SWORD,
                GUITAR,
                UKULELE,
            ]
        )
        self.prop_type_combobox.currentIndexChanged.connect(self.prop_type_changed)

    def prop_type_changed(self) -> None:
        new_prop_type = self.prop_type_combobox.currentText()
        self.preferences_dialog.settings_manager.set_prop_type(new_prop_type)
        self.preferences_dialog.settings_manager.save_settings()
        self.preferences_dialog.settings_manager.apply_settings()

    def _setup_layout(self) -> None:
        layout = QFormLayout()
        layout.addRow(QLabel("Select Prop Type:"), self.prop_type_combobox)
        self.setLayout(layout)

    def load_initial_settings(self) -> None:
        initial_prop_type = self.preferences_dialog.settings_manager.get_prop_type()
        self.prop_type_combobox.setCurrentText(initial_prop_type)
