from typing import TYPE_CHECKING
from ..base_classes.base_sequence_generator_frame import BaseSequenceGeneratorFrame
from ..widgets.permutation_type_toggle import PermutationTypeToggle
from ..widgets.rotation_type_toggle import RotationTypeToggle
from .circular_sequence_generator import CircularSequenceGenerator

if TYPE_CHECKING:
    from ..sequence_generator_widget import SequenceGeneratorWidget


class CircularSequenceGeneratorFrame(BaseSequenceGeneratorFrame):
    def __init__(self, sequence_generator_tab: "SequenceGeneratorWidget") -> None:
        super().__init__(sequence_generator_tab, "circular")
        self.builder = CircularSequenceGenerator(self)

        # Instantiate Circular-specific widgets
        self.rotation_type_toggle = RotationTypeToggle(self)
        self.permutation_type_toggle = PermutationTypeToggle(self)

        # Add Widgets to Layout
        self.layout.addWidget(self.rotation_type_toggle)
        self.layout.addStretch(1)
        # self.layout.addWidget(self.permutation_type_toggle)
        # self.layout.addStretch(1)

        # Apply Settings
        self.apply_settings()

    def apply_settings(self):
        """Apply settings to the modular widgets."""
        super().apply_settings()

        rotation_type = self.sequence_generator_settings.get_sequence_generator_setting(
            "rotation_type", self.builder_type
        )
        permutation_type = (
            self.sequence_generator_settings.get_sequence_generator_setting(
                "permutation_type", self.builder_type
            )
        )

        # Update state of the toggles
        self.rotation_type_toggle.set_state(rotation_type == "quartered")
        self.permutation_type_toggle.set_state(permutation_type == "rotated")
        # Ensure the label styles are updated correctly based on the toggle state

    def _update_rotation_type(self, rotation_type: str):
        """Update the rotation type based on the toggle."""
        self.sequence_generator_settings.set_sequence_generator_setting(
            "rotation_type", rotation_type, self.builder_type
        )

    def _update_permutation_type(self, permutation_type: str):
        """Update the permutation type based on the toggle."""
        self.sequence_generator_settings.set_sequence_generator_setting(
            "permutation_type", permutation_type, self.builder_type
        )
        if permutation_type == "mirrored":
            # Hide rotation type toggle when mirrored
            self.rotation_type_toggle.hide()
            self.length_adjuster.limit_length(False)
        else:
            # Show rotation type toggle when not mirrored
            self.rotation_type_toggle.show()
            self.length_adjuster.limit_length(True)

    def on_create_sequence(self, overwrite_sequence: bool):
        """Trigger sequence creation for Circular."""
        if overwrite_sequence:
            self.sequence_generator_tab.main_widget.sequence_widget.beat_frame.beat_deletion_manager.delete_all_beats()

        self.builder.build_sequence(
            self.sequence_generator_settings.get_sequence_generator_setting(
                "sequence_length", self.builder_type
            ),
            float(
                self.sequence_generator_settings.get_sequence_generator_setting(
                    "max_turn_intensity", self.builder_type
                )
            ),
            self.sequence_generator_settings.get_sequence_generator_setting(
                "sequence_level", self.builder_type
            ),
            self.sequence_generator_settings.get_sequence_generator_setting(
                "rotation_type", self.builder_type
            ),
            self.sequence_generator_settings.get_sequence_generator_setting(
                "permutation_type", self.builder_type
            ),
            self.sequence_generator_settings.get_sequence_generator_setting(
                "continuous_rotation", self.builder_type
            ),
        )
        # self.sequence_generator.sequence_builder.manual_builder.option_picker.update_option_picker()

    def _resize_sequence_generator_frame(self):
        super()._resize_sequence_generator_frame()
        self.permutation_type_toggle.resize_permutation_type_toggle()
        self.rotation_type_toggle.resize_rotation_type_toggle()
