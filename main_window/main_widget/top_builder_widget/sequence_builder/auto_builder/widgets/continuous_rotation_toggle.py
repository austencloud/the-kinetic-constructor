from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from pytoggle import PyToggle
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..base_classes.base_auto_builder_frame import BaseAutoBuilderFrame


class ContinuousRotationToggle(QWidget):
    def __init__(self, auto_builder_frame: "BaseAutoBuilderFrame"):
        super().__init__()
        self.auto_builder_frame = auto_builder_frame
        self.layout: QHBoxLayout = QHBoxLayout()
        self.setLayout(self.layout)
        self._create_rotation_toggle()

    def _create_rotation_toggle(self):
        self.random_label = QLabel("Random")
        self.continuous_label = QLabel("Continuous")
        self.toggle = PyToggle()
        self.toggle.stateChanged.connect(self._toggle_changed)

        self.layout.addWidget(self.random_label)
        self.layout.addWidget(self.toggle)
        self.layout.addWidget(self.continuous_label)

        # Initial style update
        self.update_mode_label_styles()

    def _toggle_changed(self, state):
        self.auto_builder_frame._update_continuous_rotation(bool(state))
        self.update_mode_label_styles()

    def update_mode_label_styles(self):
        """Update the styles of the labels to indicate the selected rotation type."""
        font_color_updater = (
            self.auto_builder_frame.auto_builder.main_widget.settings_manager.global_settings.font_color_updater
        )
        font_color = font_color_updater.get_font_color(
            self.auto_builder_frame.auto_builder.main_widget.settings_manager.global_settings.get_background_type()
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
        """Set the initial state when loading settings."""
        self.toggle.setChecked(state)
        self.update_mode_label_styles()

    def resize_continuous_rotation_toggle(self):
        font_size = self.auto_builder_frame.auto_builder.main_widget.width() // 75
        font = self.random_label.font()
        font.setPointSize(font_size)
        self.random_label.setFont(font)
        self.continuous_label.setFont(font)

        self.random_label.updateGeometry()
        self.continuous_label.updateGeometry()

        self.random_label.repaint()
        self.continuous_label.repaint()
