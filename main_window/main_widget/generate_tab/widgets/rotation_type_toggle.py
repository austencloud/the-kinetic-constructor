from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from pytoggle import PyToggle
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.generate_tab import GenerateTab


class RotationTypeToggle(QWidget):
    def __init__(self, generate_tab: "GenerateTab"):
        super().__init__()
        self.generate_tab = generate_tab
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.halved_label = QLabel("Halved")
        self.quartered_label = QLabel("Quartered")
        self.rotation_type_toggle = PyToggle()
        self.rotation_type_toggle.stateChanged.connect(self._toggle_changed)

        # Add labels and toggle to layout
        self.layout.addWidget(self.halved_label)
        self.layout.addWidget(self.rotation_type_toggle)
        self.layout.addWidget(self.quartered_label)

    def _toggle_changed(self, state):
        # If we REALLY need to force True, check if it’s already True:
        rot_type = "quartered" if state else "halved"
        self.rotation_type_toggle.blockSignals(True)
        self.rotation_type_toggle.setChecked(state)
        self.rotation_type_toggle.blockSignals(False)
        self.update_mode_label_styles()
        self.generate_tab.settings.set_setting(
            "rotation_type", rot_type
        )

    def update_mode_label_styles(self):
        """Update the styles of the labels to indicate the selected rotation type."""
        font_color_updater = self.generate_tab.main_widget.font_color_updater
        font_color = font_color_updater.get_font_color(
            self.generate_tab.main_widget.settings_manager.global_settings.get_background_type()
        )
        if self.rotation_type_toggle.isChecked():
            self.halved_label.setStyleSheet("font-weight: normal; color: gray;")
            self.quartered_label.setStyleSheet(
                f"font-weight: bold; color: {font_color};"
            )
        else:
            self.halved_label.setStyleSheet(f"font-weight: bold; color: {font_color};")
            self.quartered_label.setStyleSheet("font-weight: normal; color: gray;")
        self.halved_label.repaint()
        self.quartered_label.repaint()

    def set_state(self, state):
        """Set the toggle state when loading settings."""
        if state == True:
            self.rotation_type_toggle.setChecked(True)
        else:
            self.rotation_type_toggle.setChecked(False)
        self.update_mode_label_styles()

    def resizeEvent(self, event):
        font_size = self.generate_tab.main_widget.width() // 75
        font = self.halved_label.font()
        font.setPointSize(font_size)
        self.halved_label.setFont(font)
        self.quartered_label.setFont(font)

        self.halved_label.updateGeometry()
        self.quartered_label.updateGeometry()
        self.halved_label.repaint()
        self.quartered_label.repaint()
