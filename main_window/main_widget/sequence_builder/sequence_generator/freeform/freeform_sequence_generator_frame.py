from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QCheckBox
from ..base_classes.base_sequence_generator_frame import BaseSequenceGeneratorFrame
from ..widgets.letter_type_picker import LetterTypePicker
from .freeform_sequence_generator import FreeFormSequenceGenerator

if TYPE_CHECKING:
    from ..sequence_generator_widget import SequenceGeneratorWidget


class FreeformSequenceGeneratorFrame(BaseSequenceGeneratorFrame):
    def __init__(self, sequence_generator_tab: "SequenceGeneratorWidget") -> None:
        super().__init__(sequence_generator_tab, "freeform")
        self.builder = FreeFormSequenceGenerator(self)

        # Attach specific action for sequence creation

        self.letter_type_picker = LetterTypePicker(self)  # Instantiate LetterTypePicker
        self.layout.addWidget(self.letter_type_picker)  # Add LetterTypePicker to layout
        self.layout.addStretch(1)

        self.apply_settings()

    def on_create_sequence(self, overwrite_sequence: bool):
        """Trigger sequence creation for Freeform."""
        if overwrite_sequence:
            # ask the beat frame to remove all the beats first
            self.sequence_generator_tab.main_widget.sequence_widget.beat_frame.beat_deletion_manager.delete_all_beats()

        self.builder.build_sequence(
            int(
                self.sequence_generator_settings.get_sequence_generator_setting(
                    "sequence_length", self.builder_type
                )
            ),
            float(
                self.sequence_generator_settings.get_sequence_generator_setting(
                    "max_turn_intensity", self.builder_type
                )
            ),
            int(
                self.sequence_generator_settings.get_sequence_generator_setting(
                    "sequence_level", self.builder_type
                )
            ),
            self.sequence_generator_settings.get_sequence_generator_setting(
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
