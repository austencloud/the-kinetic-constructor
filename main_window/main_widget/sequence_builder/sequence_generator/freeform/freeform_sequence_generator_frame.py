from typing import TYPE_CHECKING
from PyQt6.QtGui import QFont

from Enums.letters import LetterType
from .letter_type_picker_widget import LetterTypePickerWidget
from main_window.main_widget.sequence_builder.sequence_generator.freeform.freeform_sequence_generator import (
    FreeFormSequenceGenerator,
)
from ..base_classes.base_sequence_generator_frame import BaseSequenceGeneratorFrame

if TYPE_CHECKING:
    from ..sequence_generator_widget import SequenceGeneratorWidget


class FreeformSequenceGeneratorFrame(BaseSequenceGeneratorFrame):
    def __init__(self, sequence_generator_tab: "SequenceGeneratorWidget") -> None:
        super().__init__(sequence_generator_tab, "freeform")

        self.letter_type_picker = LetterTypePickerWidget(self)
        self.layout.addWidget(self.letter_type_picker)

        self.builder = FreeFormSequenceGenerator(self)
        self.letter_type_picker.apply_settings()

    def on_create_sequence(self, overwrite_sequence: bool):
        if overwrite_sequence:
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

    def get_selected_letter_types(self) -> list[LetterType]:
        return self.letter_type_picker.get_selected_letter_types()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        font_size = self.height() // 30
        self.layout.setSpacing(self.height() // 50)
        # Adjust if needed
