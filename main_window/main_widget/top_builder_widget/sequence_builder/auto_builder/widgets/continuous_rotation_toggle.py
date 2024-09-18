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

    def _toggle_changed(self, state):
        self.auto_builder_frame._update_continuous_rotation(bool(state))

    def set_state(self, state):
        """Set the initial state when loading settings."""
        self.toggle.setChecked(state)

    def resize_continuous_rotation_toggle(self):
        font_size = self.auto_builder_frame.auto_builder.main_widget.width() // 60
        self.random_label.setStyleSheet(f"font-size: {font_size}px;")
        self.continuous_label.setStyleSheet(f"font-size: {font_size}px;")

        self.random_label.updateGeometry()
        self.continuous_label.updateGeometry()

        self.random_label.repaint()
        self.continuous_label.repaint()
