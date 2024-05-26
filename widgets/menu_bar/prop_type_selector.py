# PropTypeSelector.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QLabel,
    QComboBox,
    QWidget,
    QVBoxLayout,
)
from Enums.PropTypes import *

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class PropTypeSelector(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.prop_type_changer = (
            self.main_widget.main_window.settings_manager.prop_type_changer
        )
        self._setup_prop_type_combobox()
        self._setup_layout()

    def _setup_prop_type_combobox(self) -> None:
        self.prop_type_combobox = QComboBox()
        self.prop_type_combobox.addItems([prop_type.name for prop_type in PropType])

    def _setup_layout(self) -> None:
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select Prop Type:"))
        layout.addWidget(self.prop_type_combobox)
        self.setLayout(layout)

    def load_initial_settings(self) -> None:
        initial_prop_type = (
            self.main_widget.main_window.settings_manager.get_prop_type()
        )
        self.prop_type_combobox.setCurrentText(initial_prop_type.name)

    def apply_settings(self) -> None:
        new_prop_type = self.prop_type_combobox.currentText()
        self.on_prop_type_changed(new_prop_type)

    def on_prop_type_changed(self, new_prop_type: PropType) -> None:
        self.main_widget.main_window.settings_manager.set_prop_type(new_prop_type)
        self.main_widget.main_window.settings_manager.save_settings()
        self.prop_type_changer.apply_prop_type()
        if hasattr(self.main_widget.main_window.menu_bar, "preferences_dialog"):
            self.main_widget.main_window.menu_bar.preferences_dialog.apply_button.setEnabled(
                True
            )

    def reset_settings(self) -> None:
        initial_prop_type = PropType.Hand.name
        self.prop_type_combobox.setCurrentText(initial_prop_type)
