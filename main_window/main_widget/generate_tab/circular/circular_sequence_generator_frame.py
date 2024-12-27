from typing import TYPE_CHECKING
from ..base_classes.base_sequence_generator_frame import BaseSequenceGeneratorFrame
from ..widgets.permutation_type_toggle import PermutationTypeToggle
from ..widgets.rotation_type_toggle import RotationTypeToggle
from .circular_sequence_generator import CircularSequenceGenerator

if TYPE_CHECKING:
    from ..generate_tab import GenerateTab


class CircularSequenceGeneratorFrame(BaseSequenceGeneratorFrame):
    def __init__(self, sequence_generator_tab: "GenerateTab") -> None:
        super().__init__(sequence_generator_tab, "circular")
        self.builder = CircularSequenceGenerator(self)

        self.rotation_type_toggle = RotationTypeToggle(self)
        self.permutation_type_toggle = PermutationTypeToggle(self)

        self.layout.addWidget(self.rotation_type_toggle)
        self.layout.addStretch(1)

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
            self.sequence_generator_widget.main_widget.sequence_widget.beat_frame.deletion_manager.delete_all_beats()

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

    def show(self):
        """Display Circular frame by setting it in the stacked layout."""
        self.sequence_generator_widget.stacked_layout.setCurrentWidget(self)
        self.sequence_generator_widget.current_sequence_generator = "circular"
        self.sequence_generator_widget.update_button_styles()

        if self.sequence_generator_widget.overwrite_connected:
            try:
                self.sequence_generator_widget.overwrite_checkbox.stateChanged.disconnect()
            except TypeError:
                pass
            self.sequence_generator_widget.overwrite_connected = False

        overwrite_value = (
            self.sequence_generator_settings.get_sequence_generator_setting(
                "overwrite_sequence",
                self.sequence_generator_widget.current_sequence_generator,
            )
        )

        if isinstance(overwrite_value, bool):
            overwrite_bool = overwrite_value
        elif isinstance(overwrite_value, str):
            overwrite_bool = overwrite_value.lower() == "true"
        else:
            overwrite_bool = False

        self.sequence_generator_widget.overwrite_checkbox.setChecked(overwrite_bool)

        self.sequence_generator_widget.overwrite_checkbox.checkbox.stateChanged.connect(
            lambda state: self.sequence_generator_settings.set_sequence_generator_setting(
                "overwrite_sequence",
                state == 2,
                self.sequence_generator_widget.current_sequence_generator,
            )
        )
        self.sequence_generator_widget.overwrite_connected = True

        self.sequence_generator_widget.generate_sequence_button.clicked.disconnect()
        self.sequence_generator_widget.generate_sequence_button.clicked.connect(
            lambda: self.on_create_sequence(
                self.sequence_generator_widget.overwrite_checkbox.isChecked()
            )
        )
