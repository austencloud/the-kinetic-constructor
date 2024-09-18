from typing import TYPE_CHECKING
from main_window.main_widget.top_builder_widget.sequence_builder.auto_builder.base_classes.base_auto_builder_frame import (
    BaseAutoBuilderFrame,
)

from .freeform_auto_builder import FreeFormAutoBuilder

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_builder.auto_builder.auto_builder import (
        AutoBuilder,
    )


class FreeformAutoBuilderFrame(BaseAutoBuilderFrame):
    def __init__(self, auto_builder: "AutoBuilder") -> None:
        super().__init__(auto_builder, "freeform")
        self.builder = FreeFormAutoBuilder(self)

        # Attach specific action for sequence creation
        self.create_sequence_button.clicked.connect(self._on_create_sequence)
        self.apply_settings()

    def _on_create_sequence(self):
        """Trigger sequence creation for Freeform."""
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
                "continuous_rotation", self.builder_type
            ),
        )
        self.auto_builder.sequence_builder.manual_builder.option_picker.update_option_picker()
