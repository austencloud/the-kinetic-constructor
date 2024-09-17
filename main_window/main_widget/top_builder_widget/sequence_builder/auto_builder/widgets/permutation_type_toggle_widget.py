from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from pytoggle import PyToggle
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from ..circular.circular_auto_builder_frame import CircularAutoBuilderFrame


class PermutationTypeToggleWidget(QWidget):
    def __init__(self, circular_builder_frame: "CircularAutoBuilderFrame"):
        super().__init__()
        self.circular_builder_frame = circular_builder_frame
        self.layout: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.layout)

        self.permutation_type_label = QLabel("Permutation Type:")
        self.permutation_type_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.toggle_layout = QHBoxLayout()
        self.toggle_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.mirrored_label = QLabel("Mirrored")
        self.rotational_label = QLabel("Rotated")
        self.permutation_type_toggle = PyToggle()
        self.permutation_type_toggle.stateChanged.connect(self._toggle_changed)

        # Add labels and toggle to layout
        self.toggle_layout.addWidget(self.mirrored_label)
        self.toggle_layout.addWidget(self.permutation_type_toggle)
        self.toggle_layout.addWidget(self.rotational_label)

        # Add everything to the main layout
        # self.layout.addWidget(self.permutation_type_label)
        self.layout.addLayout(self.toggle_layout)

    def _toggle_changed(self, state):
        permutation_type = "rotational" if state else "mirrored"
        self.circular_builder_frame._update_permutation_type(permutation_type)

    def set_state(self, state):
        """Set the toggle state when loading settings."""
        self.permutation_type_toggle.setChecked(state)

    def resize_permutation_type_toggle(self):
        font_size = self.circular_builder_frame.auto_builder.main_widget.width() // 60
        self.mirrored_label.setStyleSheet(f"font-size: {font_size}px;")
        self.rotational_label.setStyleSheet(f"font-size: {font_size}px;")
        self.permutation_type_label.setStyleSheet(f"font-size: {font_size}px;")
        self.mirrored_label.updateGeometry()
        self.rotational_label.updateGeometry()

        self.mirrored_label.repaint()
        self.rotational_label.repaint()
