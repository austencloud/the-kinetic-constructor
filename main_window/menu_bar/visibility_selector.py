# visibility_selector.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QCheckBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from .base_selector import ButtonSelector

if TYPE_CHECKING:
    from main_window.menu_bar.menu_bar import MenuBarWidget


class VisibilitySelector(ButtonSelector):
    def __init__(self, menu_bar: "MenuBarWidget"):
        super().__init__(menu_bar, "Visibility")
        self.settings_manager = self.main_widget.settings_manager
        self.glyph_visibility_manager = self.settings_manager.visibility.glyph
        self.grid_visibility_manager = self.settings_manager.visibility.grid

    def on_button_clicked(self):
        self.show_visibility_dialog()

    def show_visibility_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        dialog.setStyleSheet(
            """
            QDialog {
                border: 2px solid black;
                border-radius: 5px;
                background-color: white;
            }
            QCheckBox {
                padding: 5px;
            }
            """
        )

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(5, 5, 5, 5)

        glyph_types = ["TKA", "VTG", "Elemental", "Positions", "Reversals"]
        options = {
            f"{glyph}": self.glyph_visibility_manager.should_glyph_be_visible(glyph)
            for glyph in glyph_types
        }
        options["non_radial_points"] = self.grid_visibility_manager.non_radial_visible

        font = QFont()
        self.selector_font_size = self.main_widget.height() // 50
        font.setPointSize(self.selector_font_size)

        for option_text, checked in options.items():
            checkbox = QCheckBox(option_text)
            checkbox.setChecked(checked)
            checkbox.setFont(font)
            checkbox.stateChanged.connect(
                lambda state, o=option_text: self.option_toggled(o, state)
            )
            layout.addWidget(checkbox)

        dialog.setLayout(layout)
        dialog.adjustSize()

        global_pos = self.button.mapToGlobal(self.button.rect().bottomLeft())
        dialog.move(global_pos)
        dialog.exec()

    def option_toggled(self, option: str, state):
        is_checked = state == Qt.CheckState.Checked.value
        if option == "non_radial_points":
            self.grid_visibility_manager.set_non_radial_visibility(is_checked)
        else:
            self.settings_manager.visibility.set_glyph_visibility(option, is_checked)
