from PyQt6.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout, QLabel
from pytoggle import PyToggle
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..base_classes.base_auto_builder_frame import BaseAutoBuilderFrame


class ContinuousRotationToggleWidget(QWidget):
    def __init__(self, auto_builder_frame: "BaseAutoBuilderFrame"):
        super().__init__()
        self.auto_builder_frame = auto_builder_frame
        self.layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.layout)

        self.rotation_label = QLabel("Continuous Rotation:")
        self.rotation_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.rotation_toggle_layout = QHBoxLayout()
        self.rotation_toggle_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._create_rotation_toggle(False)

        # Add the label and toggle layout to the main layout
        self.layout.addWidget(self.rotation_label)
        self.layout.addLayout(self.rotation_toggle_layout)

    def _create_rotation_toggle(self, initial_state):
        self.random_label = QLabel("Random")
        self.continuous_label = QLabel("Continuous")
        self.toggle = PyToggle()
        self.toggle.setChecked(initial_state)
        self.toggle.stateChanged.connect(self._toggle_changed)

        self.rotation_toggle_layout.addWidget(self.random_label)
        self.rotation_toggle_layout.addWidget(self.toggle)
        self.rotation_toggle_layout.addWidget(self.continuous_label)

    def _toggle_changed(self, state):
        self.auto_builder_frame._update_continuous_rotation(bool(state))

    def set_state(self, state):
        """Set the initial state when loading settings."""
        self.toggle.setChecked(state)
