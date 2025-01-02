from typing import TYPE_CHECKING

from Enums.letters import LetterType
from .letter_type_picker_widget import LetterTypePickerWidget
from main_window.main_widget.generate_tab.freeform.freeform_sequence_generator import (
    FreeFormSequenceGenerator,
)
from ..base_classes.base_sequence_generator_frame import BaseSequenceGeneratorFrame

if TYPE_CHECKING:
    from ..generate_tab import GenerateTab


class FreeformSequenceGeneratorFrame(BaseSequenceGeneratorFrame):
    def __init__(self, sequence_generator_tab: "GenerateTab") -> None:
        super().__init__(sequence_generator_tab, "freeform")

        self.letter_type_picker = LetterTypePickerWidget(self)
        self.layout.addWidget(self.letter_type_picker)

        self.builder = FreeFormSequenceGenerator(self)
        self.letter_type_picker.apply_settings()
        self.beat_deleter = (
            self.generate_tab.main_widget.sequence_widget.beat_frame.sequence_widget.beat_deleter
        )

    def on_create_sequence(self, overwrite_sequence: bool):
        if overwrite_sequence:
            self.beat_deleter.reset_widgets(False)

        self.builder.build_sequence(
            int(
                self.generate_tab_settings.get_sequence_generator_setting(
                    "sequence_length", self.builder_type
                )
            ),
            float(
                self.generate_tab_settings.get_sequence_generator_setting(
                    "max_turn_intensity", self.builder_type
                )
            ),
            int(
                self.generate_tab_settings.get_sequence_generator_setting(
                    "sequence_level", self.builder_type
                )
            ),
            self.generate_tab_settings.get_sequence_generator_setting(
                "continuous_rotation", self.builder_type
            ),
        )

    def get_selected_letter_types(self) -> list[LetterType]:
        return self.letter_type_picker.get_selected_letter_types()

    def resizeEvent(self, event):
        self.layout.setSpacing(self.height() // 50)
        super().resizeEvent(event)

    def show(self):
        """Display Freeform frame by setting it in the stacked layout."""
        self.generate_tab.stacked_layout.setCurrentWidget(self)
        self.generate_tab.current_sequence_generator = "freeform"
        self.generate_tab.button_manager.update_button_styles()

        if self.generate_tab.overwrite_connected:
            try:
                self.generate_tab.overwrite_checkbox.checkbox.stateChanged.disconnect()
            except TypeError:
                pass
            self.generate_tab.overwrite_connected = False

        overwrite_value = self.generate_tab_settings.get_sequence_generator_setting(
            "overwrite_sequence",
            self.generate_tab.current_sequence_generator,
        )

        if isinstance(overwrite_value, bool):
            overwrite_bool = overwrite_value
        elif isinstance(overwrite_value, str):
            overwrite_bool = overwrite_value.lower() == "true"
        else:
            overwrite_bool = False

        self.generate_tab.overwrite_checkbox.setChecked(overwrite_bool)

        self.generate_tab.overwrite_checkbox.checkbox.stateChanged.connect(
            lambda state: self.generate_tab_settings.set_sequence_generator_setting(
                "overwrite_sequence",
                state == 2,
                self.generate_tab.current_sequence_generator,
            )
        )
        self.overwrite_connected = True

        self.generate_tab.generate_sequence_button.clicked.disconnect()
        self.generate_tab.generate_sequence_button.clicked.connect(
            lambda: self.on_create_sequence(
                self.generate_tab.overwrite_checkbox.isChecked()
            )
        )
