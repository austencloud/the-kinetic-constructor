from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from main_window.main_widget.top_builder_widget.sequence_builder.auto_builder.base_auto_builder_frame import (
    BaseAutoBuilderFrame,
)
from pytoggle import PyToggle

from .circular_auto_builder import CircularAutoBuilder

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_builder.auto_builder.auto_builder import (
        AutoBuilder,
    )


class CircularAutoBuilderFrame(BaseAutoBuilderFrame):
    def __init__(self, auto_builder: "AutoBuilder") -> None:
        super().__init__(auto_builder, "circular")
        self.builder = CircularAutoBuilder(self)

        # Add Circular-specific widgets
        self._setup_circular_specific_ui()

        # Attach specific action for sequence creation
        self.create_sequence_button.clicked.connect(self._on_create_sequence)
        self.apply_settings()

    def apply_settings(self):
        super().apply_settings()
        rotation_type = self.auto_builder_settings.get_auto_builder_setting(
            "rotation_type", self.builder_type
        )
        permutation_type = self.auto_builder_settings.get_auto_builder_setting(
            "permutation_type", self.builder_type
        )

        # check them accordingly
        self.rotation_type_toggle.setChecked(rotation_type == "quartered")
        self.permutation_type_toggle.setChecked(permutation_type == "rotational")

        self._update_rotation_type(rotation_type == "quartered")
        self._update_permutation_type(permutation_type == "rotational")

    def _setup_circular_specific_ui(self):
        """Setup specific UI elements for the Circular builder."""
        # Rotation Type Toggle

        self.rotation_type_toggle_layout = self._create_rotation_type_toggle_layout()

        # Permutation Type Toggle

        self.permutation_type_toggle_layout = (
            self._create_permutation_type_toggle_layout()
        )

        self.layout.addLayout(self.rotation_type_toggle_layout)
        self.layout.addStretch(1)
        self.layout.addLayout(self.permutation_type_toggle_layout)
        self.layout.addStretch(1)

        self.layout.addWidget(
            self.create_sequence_button, alignment=Qt.AlignmentFlag.AlignCenter
        )
        # self.layout.addStretch(1)

    def _create_rotation_type_toggle_layout(self) -> PyToggle:
        """Create toggle for rotation type."""
        self.rotation_type_toggle = PyToggle()
        self.rotation_type_toggle.stateChanged.connect(self._update_rotation_type)
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add labels to self.labels dict
        self.halved_label = QLabel("Halved")
        self.quartered_label = QLabel("Quartered")
        self.labels["rotation_type_halved"] = self.halved_label
        self.labels["rotation_type_quartered"] = self.quartered_label

        layout.addWidget(self.halved_label)
        layout.addWidget(self.rotation_type_toggle)
        layout.addWidget(self.quartered_label)
        return layout

    def _create_permutation_type_toggle_layout(self) -> PyToggle:
        """Create toggle for permutation type."""
        self.permutation_type_toggle = PyToggle()
        self.permutation_type_toggle.stateChanged.connect(self._update_permutation_type)
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add labels to self.labels dict
        self.mirrored_label = QLabel("Mirrored")
        self.rotational_label = QLabel("Rotated")
        self.labels["permutation_type_mirrored"] = self.mirrored_label
        self.labels["permutation_type_rotated"] = self.rotational_label

        layout.addWidget(self.mirrored_label)
        layout.addWidget(self.permutation_type_toggle)
        layout.addWidget(self.rotational_label)
        return layout

    def _update_rotation_type(self, state):
        """Update the rotation type based on toggle."""
        rotation_type = "quartered" if state else "halved"
        self.auto_builder_settings.set_auto_builder_setting(
            "rotation_type", rotation_type, self.builder_type
        )

    def _update_permutation_type(self, state):
        """Update the permutation type based on toggle."""
        permutation_type = "rotational" if state else "mirrored"
        self.auto_builder_settings.set_auto_builder_setting(
            "permutation_type", permutation_type, self.builder_type
        )
        # if it's mirrored, hide the continuous rotation option
        if permutation_type == "mirrored":
            self.auto_builder_settings.set_auto_builder_setting(
                "continuous_rotation", False, self.builder_type
            )
            # self.continuous_rotation_toggle.hide()
            # self.continuous_label.hide()
            # self.random_label.hide()

            self.halved_label.hide()
            self.quartered_label.hide()
            self.rotation_type_toggle.hide()
        else:
            # if they are hidden, show them
            # self.continuous_rotation_toggle.show()
            # self.continuous_label.show()
            # self.random_label.show()

            self.halved_label.show()
            self.quartered_label.show()
            self.rotation_type_toggle.show()

    def _on_create_sequence(self):
        """Trigger sequence creation for Circular."""
        self.builder.build_sequence(
            self.auto_builder_settings.get_auto_builder_setting(
                "sequence_length", self.builder_type
            ),
            float(
                self.auto_builder_settings.get_auto_builder_setting(
                    "max_turn_intensity", self.builder_type
                )
            ),
            self.auto_builder_settings.get_auto_builder_setting(
                "sequence_level", self.builder_type
            ),
            self.auto_builder_settings.get_auto_builder_setting(
                "rotation_type", self.builder_type
            ),
            self.auto_builder_settings.get_auto_builder_setting(
                "permutation_type", self.builder_type
            ),
            self.auto_builder_settings.get_auto_builder_setting(
                "continuous_rotation", self.builder_type
            ),
        )
        self.auto_builder.sequence_builder.manual_builder.option_picker.update_option_picker()
