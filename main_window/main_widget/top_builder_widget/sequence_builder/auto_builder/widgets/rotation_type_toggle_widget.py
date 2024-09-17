from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from pytoggle import PyToggle
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from ..circular_auto_builder_frame import CircularAutoBuilderFrame


class RotationTypeToggleWidget(QWidget):
    def __init__(self, circular_builder_frame: "CircularAutoBuilderFrame"):
        super().__init__()
        self.circular_builder_frame = circular_builder_frame
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.halved_label = QLabel("Halved")
        self.quartered_label = QLabel("Quartered")
        self.rotation_type_toggle = PyToggle()
        self.rotation_type_toggle.stateChanged.connect(self._toggle_changed)

        self.layout.addWidget(self.halved_label)
        self.layout.addWidget(self.rotation_type_toggle)
        self.layout.addWidget(self.quartered_label)

    def _toggle_changed(self, state):
        rotation_type = "quartered" if state else "halved"
        self.circular_builder_frame._update_rotation_type(rotation_type)

    def set_state(self, state):
        """Set the toggle state when loading settings."""
        self.rotation_type_toggle.setChecked(state)
