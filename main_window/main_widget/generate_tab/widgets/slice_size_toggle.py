from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from pytoggle import PyToggle
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from ..generate_tab import GenerateTab


class SliceSizeToggle(QWidget):
    def __init__(self, generate_tab: "GenerateTab"):
        super().__init__()
        self.generate_tab = generate_tab
        self.main_widget = self.generate_tab.main_widget

        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.halved_label = QLabel("Halved")
        self.quartered_label = QLabel("Quartered")
        self.toggle = PyToggle()
        self.toggle.stateChanged.connect(self._toggle_changed)

        self.layout.addWidget(self.halved_label)
        self.layout.addWidget(self.toggle)
        self.layout.addWidget(self.quartered_label)

    def _toggle_changed(self, state):
        rot_type = "quartered" if state else "halved"
        self.toggle.blockSignals(True)
        self.toggle.setChecked(state)
        self.toggle.blockSignals(False)
        self.update_mode_label_styles()
        self.generate_tab.settings.set_setting("rotation_type", rot_type)

    def update_mode_label_styles(self):
        font_color_updater = self.generate_tab.main_widget.font_color_updater
        font_color = font_color_updater.get_font_color(
            self.generate_tab.main_widget.settings_manager.global_settings.get_background_type()
        )
        if self.toggle.isChecked():
            self.halved_label.setStyleSheet("font-weight: normal; color: gray;")
            self.quartered_label.setStyleSheet(
                f"font-weight: bold; color: {font_color};"
            )
        else:
            self.halved_label.setStyleSheet(f"font-weight: bold; color: {font_color};")
            self.quartered_label.setStyleSheet("font-weight: normal; color: gray;")

    def set_state(self, state):
        self.toggle.setChecked(state)
        self.update_mode_label_styles()

    def resizeEvent(self, event) -> None:
        font_size = self.main_widget.width() // 75
        font = self.halved_label.font()
        font.setPointSize(font_size)
        self.halved_label.setFont(font)
        self.quartered_label.setFont(font)

        self.halved_label.updateGeometry()
        self.quartered_label.updateGeometry()
        self.halved_label.repaint()
        self.quartered_label.repaint()
