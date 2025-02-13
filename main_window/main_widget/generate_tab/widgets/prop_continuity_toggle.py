from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from pytoggle import PyToggle
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from ..generate_tab import GenerateTab


class PropContinuityToggle(QWidget):
    def __init__(self, generate_tab: "GenerateTab"):
        super().__init__()
        self.generate_tab = generate_tab
        self.main_widget = self.generate_tab.main_widget
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setLayout(self.layout)
        self._create_rotation_toggle()

    def _create_rotation_toggle(self):
        self.random_label = QLabel("Random")
        self.continuous_label = QLabel("Continuous")
        self.toggle = PyToggle()
        self.toggle.stateChanged.connect(self._toggle_changed)
        self.layout.addStretch(1)
        self.layout.addWidget(self.random_label)
        self.layout.addWidget(self.toggle)
        self.layout.addWidget(self.continuous_label)
        self.layout.addStretch(1)

    def _toggle_changed(self, state):
        rotation = "continuous" if state else "random"
        self.toggle.blockSignals(True)
        self.toggle.setChecked(state)
        self.toggle.blockSignals(False)
        self.update_mode_label_styles()
        self.generate_tab.settings.set_setting("continuous_rotation", rotation)

    def update_mode_label_styles(self):
        settings_manager = self.main_widget.settings_manager
        font_color_updater = self.main_widget.font_color_updater
        font_color = font_color_updater.get_font_color(
            settings_manager.global_settings.get_background_type()
        )
        if self.toggle.isChecked():
            self.random_label.setStyleSheet("font-weight: normal; color: gray;")
            self.continuous_label.setStyleSheet(
                f"font-weight: bold; color: {font_color};"
            )
        else:
            self.random_label.setStyleSheet(f"font-weight: bold; color: {font_color};")
            self.continuous_label.setStyleSheet("font-weight: normal; color: gray;")

    def set_state(self, state):
        self.toggle.setChecked(state)
        self.update_mode_label_styles()

    def resizeEvent(self, event):
        font_size = self.main_widget.width() // 75
        font = self.random_label.font()
        font.setPointSize(font_size)
        self.random_label.setFont(font)
        self.continuous_label.setFont(font)

        self.random_label.updateGeometry()
        self.continuous_label.updateGeometry()
        self.random_label.repaint()
        self.continuous_label.repaint()
