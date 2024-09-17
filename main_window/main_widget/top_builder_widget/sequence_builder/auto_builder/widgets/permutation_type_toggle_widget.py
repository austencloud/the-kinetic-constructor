from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from pytoggle import PyToggle
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from ..circular_auto_builder_frame import CircularAutoBuilderFrame


class PermutationTypeToggleWidget(QWidget):
    def __init__(self, circular_builder_frame: "CircularAutoBuilderFrame"):
        super().__init__()
        self.circular_builder_frame = circular_builder_frame
        self.layout: QHBoxLayout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        self.mirrored_label = QLabel("Mirrored")
        self.rotational_label = QLabel("Rotated")
        self.permutation_type_toggle = PyToggle()
        self.permutation_type_toggle.stateChanged.connect(self._toggle_changed)

        self.layout.addWidget(self.mirrored_label)
        self.layout.addWidget(self.permutation_type_toggle)
        self.layout.addWidget(self.rotational_label)

    def _toggle_changed(self, state):
        permutation_type = "rotational" if state else "mirrored"
        self.circular_builder_frame._update_permutation_type(permutation_type)

    def set_state(self, state):
        """Set the toggle state when loading settings."""
        self.permutation_type_toggle.setChecked(state)
