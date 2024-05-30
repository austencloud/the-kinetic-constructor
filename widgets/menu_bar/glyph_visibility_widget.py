from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MainWindow


class GlyphVisibilityWidget(QWidget):
    def __init__(self, main_window: "MainWindow"):
        super().__init__()
        self.main_window = main_window
        self.glyph_visibility_manager = (
            main_window.settings_manager.visibility.glyph_visibility_manager
        )
        self._setup_widgets()
        self._setup_layout()

    def _setup_widgets(self):
        self.vtg_checkbox = QCheckBox("VTG")
        self.tka_checkbox = QCheckBox("TKA")
        self.elemental_checkbox = QCheckBox("Elemental")

    def _setup_layout(self):
        layout = QVBoxLayout()
        layout.addWidget(self.vtg_checkbox)
        layout.addWidget(self.tka_checkbox)
        layout.addWidget(self.elemental_checkbox)
        self.setLayout(layout)

    def load_initial_settings(self):
        self.vtg_checkbox.setChecked(
            self.glyph_visibility_manager.get_glyph_visibility("VTG")
        )
        self.tka_checkbox.setChecked(
            self.glyph_visibility_manager.get_glyph_visibility("TKA")
        )
        self.elemental_checkbox.setChecked(
            self.glyph_visibility_manager.get_glyph_visibility("Elemental")
        )

    def apply_settings(self):
        self.glyph_visibility_manager.set_glyph_visibility(
            "VTG", self.vtg_checkbox.isChecked()
        )
        self.glyph_visibility_manager.set_glyph_visibility(
            "TKA", self.tka_checkbox.isChecked()
        )
        self.glyph_visibility_manager.set_glyph_visibility(
            "Elemental", self.elemental_checkbox.isChecked()
        )
        self.glyph_visibility_manager.apply_glyph_visibility()
