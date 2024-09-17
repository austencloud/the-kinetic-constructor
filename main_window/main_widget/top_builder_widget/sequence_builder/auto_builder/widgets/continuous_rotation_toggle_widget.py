from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from pytoggle import PyToggle
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..base_auto_builder_frame import BaseAutoBuilderFrame



class ContinuousRotationToggleWidget(QWidget):
    def __init__(self, auto_builder_frame: "BaseAutoBuilderFrame"):
        super().__init__()
        self.auto_builder_frame = auto_builder_frame
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self._create_rotation_toggle(False)

    def _create_rotation_toggle(self, initial_state):
        self.random_label = QLabel("Random")
        self.continuous_label = QLabel("Continuous")
        self.toggle = PyToggle()
        self.toggle.setChecked(initial_state)
        self.toggle.stateChanged.connect(self._toggle_changed)

        self.layout.addWidget(self.random_label)
        self.layout.addWidget(self.toggle)
        self.layout.addWidget(self.continuous_label)

    def _toggle_changed(self, state):
        self.auto_builder_frame._update_continuous_rotation(bool(state))

    def set_state(self, state):
        """Set the initial state when loading settings."""
        self.toggle.setChecked(state)
