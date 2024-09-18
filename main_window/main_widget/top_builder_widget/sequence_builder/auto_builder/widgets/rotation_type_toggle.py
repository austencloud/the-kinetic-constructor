from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from pytoggle import PyToggle
from PyQt6.QtCore import Qt

if TYPE_CHECKING:
    from ..circular.circular_auto_builder_frame import CircularAutoBuilderFrame


class RotationTypeToggle(QWidget):
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

        # Add labels and toggle to layout
        self.layout.addWidget(self.halved_label)
        self.layout.addWidget(self.rotation_type_toggle)
        self.layout.addWidget(self.quartered_label)

        # Add everything to the main layout

    def _toggle_changed(self, state):
        rotation_type = "quartered" if state else "halved"
        self.circular_builder_frame._update_rotation_type(rotation_type)
        self.circular_builder_frame.length_adjuster.limit_length(state)

    def set_state(self, state):
        """Set the toggle state when loading settings."""
        self.rotation_type_toggle.setChecked(state)

    def resize_rotation_type_toggle(self):
        font_size = self.circular_builder_frame.auto_builder.main_widget.width() // 60
        self.halved_label.setStyleSheet(f"font-size: {font_size}px;")
        self.quartered_label.setStyleSheet(f"font-size: {font_size}px;")
        self.halved_label.updateGeometry()
        self.quartered_label.updateGeometry()

        self.halved_label.repaint()
        self.quartered_label.repaint()
