# PropTypeSelector.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QGroupBox, QFormLayout, QComboBox
from Enums.PropTypes import *

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from widgets.menu_bar.preferences_dialog import PreferencesDialog


class PropTypeSelector(QGroupBox):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__("Prop Type Selector")
        self.main_widget = main_widget
        self._setup_prop_type_combobox()
        self._setup_layout()

    def _setup_prop_type_combobox(self) -> None:
        self.prop_type_combobox = QComboBox()
        self.prop_type_combobox.addItems(
            [
                PropTypes.Staff.name,
                PropTypes.BigStaff.name,
                PropTypes.Club.name,
                PropTypes.Buugeng.name,
                PropTypes.EightRings.name,
                PropTypes.Fan.name,
                PropTypes.Triad.name,
                PropTypes.MiniHoop.name,
                PropTypes.BigHoop.name,
                PropTypes.DoubleStar.name,
                PropTypes.Quiad.name,
                PropTypes.Sword.name,
                PropTypes.Guitar.name,
                PropTypes.Ukulele.name,
            ]
        )

    def prop_type_changed(self, new_prop_type: str) -> None:
        new_prop_type = new_prop_type or self.prop_type_combobox.currentText()
        self.main_widget.main_window.settings_manager.set_prop_type(new_prop_type)
        self.main_widget.main_window.settings_manager.save_settings()
        self.main_widget.main_window.settings_manager.apply_settings()
        if hasattr(self.main_widget.main_window.menu_bar, "preferences_dialog"):
            self.main_widget.main_window.menu_bar.preferences_dialog.apply_button.setEnabled(
                True
            )

    def _setup_layout(self) -> None:
        layout = QFormLayout()
        layout.addRow(QLabel("Select Prop Type:"), self.prop_type_combobox)
        self.setLayout(layout)

    def load_initial_settings(self) -> None:
        initial_prop_type = (
            self.main_widget.main_window.settings_manager.get_prop_type()
        )
        self.prop_type_combobox.setCurrentText(initial_prop_type.name)
        self.prop_type_combobox.currentTextChanged.connect(self.prop_type_changed)
        # activate the apply button
