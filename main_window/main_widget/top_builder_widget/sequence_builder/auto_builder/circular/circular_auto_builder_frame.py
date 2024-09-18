from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from ..base_classes.base_auto_builder_frame import BaseAutoBuilderFrame
from ..widgets.permutation_type_toggle import PermutationTypeToggle
from ..widgets.rotation_type_toggle import RotationTypeToggle
from .circular_auto_builder import CircularAutoBuilder

if TYPE_CHECKING:
    from ..auto_builder import AutoBuilder


class CircularAutoBuilderFrame(BaseAutoBuilderFrame):
    def __init__(self, auto_builder: "AutoBuilder") -> None:
        super().__init__(auto_builder, "circular")
        self.builder = CircularAutoBuilder(self)

        # Instantiate Circular-specific widgets
        self.rotation_type_toggle = RotationTypeToggle(self)
        self.permutation_type_toggle = PermutationTypeToggle(self)

        # Attach specific action for sequence creation
        self.create_sequence_button.clicked.connect(self._on_create_sequence)

        # Add Widgets to Layout
        self.layout.addWidget(self.rotation_type_toggle)
        self.layout.addStretch(1)
        self.layout.addWidget(self.permutation_type_toggle)
        self.layout.addStretch(1)
        self.layout.addWidget(
            self.create_sequence_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Apply Settings
        self.apply_settings()

    def apply_settings(self):
        """Apply settings to the modular widgets."""
        super().apply_settings()

        rotation_type = self.auto_builder_settings.get_auto_builder_setting(
            "rotation_type", self.builder_type
        )
        permutation_type = self.auto_builder_settings.get_auto_builder_setting(
            "permutation_type", self.builder_type
        )

        # Update state of the toggles
        self.rotation_type_toggle.set_state(rotation_type == "quartered")
        self.permutation_type_toggle.set_state(permutation_type == "rotated")

    def _update_rotation_type(self, rotation_type: str):
        """Update the rotation type based on the toggle."""
        self.auto_builder_settings.set_auto_builder_setting(
            "rotation_type", rotation_type, self.builder_type
        )

    def _update_permutation_type(self, permutation_type: str):
        """Update the permutation type based on the toggle."""
        self.auto_builder_settings.set_auto_builder_setting(
            "permutation_type", permutation_type, self.builder_type
        )
        if permutation_type == "mirrored":
            # Hide rotation type toggle when mirrored
            self.rotation_type_toggle.hide()
        else:
            # Show rotation type toggle when not mirrored
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

    def _resize_auto_builder_frame(self):
        super()._resize_auto_builder_frame()
        self.permutation_type_toggle.resize_permutation_type_toggle()
        self.rotation_type_toggle.resize_rotation_type_toggle()
