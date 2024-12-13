from typing import TYPE_CHECKING

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
            self.sequence_generator_widget.main_widget.sequence_widget.beat_frame.beat_deletion_manager.delete_all_beats()

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
        self.sequence_generator_widget.main_widget.manual_builder.option_picker.update_option_picker()

    def get_selected_letter_types(self) -> list[LetterType]:
        return self.letter_type_picker.get_selected_letter_types()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        font_size = self.height() // 30
        self.layout.setSpacing(self.height() // 50)
        # Adjust if needed

    def show(self):
        """Display Freeform frame by setting it in the stacked layout."""
        self.sequence_generator_widget.stacked_layout.setCurrentWidget(self)
        self.sequence_generator_widget.current_sequence_generator = "freeform"
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

        self.sequence_generator_widget.overwrite_checkbox.stateChanged.connect(
            lambda state: self.sequence_generator_settings.set_sequence_generator_setting(
                "overwrite_sequence",
                state == 2,
                self.sequence_generator_widget.current_sequence_generator,
            )
        )
        self.overwrite_connected = True

        self.sequence_generator_widget.generate_sequence_button.clicked.disconnect()
        self.sequence_generator_widget.generate_sequence_button.clicked.connect(
            lambda: self.on_create_sequence(
                self.sequence_generator_widget.overwrite_checkbox.isChecked()
            )
        )
