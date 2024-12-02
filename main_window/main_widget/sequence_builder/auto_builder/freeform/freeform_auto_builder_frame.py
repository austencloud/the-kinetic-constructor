from typing import TYPE_CHECKING
from ..base_classes.base_auto_builder_frame import BaseAutoBuilderFrame
from ..widgets.letter_type_picker import LetterTypePicker
from .freeform_auto_builder import FreeFormAutoBuilder

if TYPE_CHECKING:
    from ..sequence_generator_widget import SequenceGeneratorWidget


class FreeformAutoBuilderFrame(BaseAutoBuilderFrame):
    def __init__(self, sequence_generator_tab: "SequenceGeneratorWidget") -> None:
        super().__init__(sequence_generator_tab, "freeform")
        self.builder = FreeFormAutoBuilder(self)

        # Attach specific action for sequence creation

        self.letter_type_picker = LetterTypePicker(self)  # Instantiate LetterTypePicker
        self.layout.addWidget(self.letter_type_picker)  # Add LetterTypePicker to layout
        self.layout.addStretch(1)

        self.apply_settings()

    def on_create_sequence(self):
        """Trigger sequence creation for Freeform."""
        self.builder.build_sequence(
            int(
                self.auto_builder_settings.get_auto_builder_setting(
                    "sequence_length", self.builder_type
                )
            ),
            float(
                self.auto_builder_settings.get_auto_builder_setting(
                    "max_turn_intensity", self.builder_type
                )
            ),
           int(self.auto_builder_settings.get_auto_builder_setting(
                "sequence_level", self.builder_type
            )),
            self.auto_builder_settings.get_auto_builder_setting(
                "continuous_rotation", self.builder_type
            ),
        )
        self.sequence_generator_tab.main_widget.manual_builder.option_picker.update_option_picker()

    def apply_settings(self):
        super().apply_settings()
        self.letter_type_picker.apply_settings()  # Apply settings to LetterTypePicker

    def _resize_widgets(self):
        super()._resize_widgets()
        # self.letter_type_picker.resize_letter_type_picker()  # Resize LetterTypePicker
