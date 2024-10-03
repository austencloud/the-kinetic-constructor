from typing import TYPE_CHECKING
from ..base_classes.base_auto_builder_frame import BaseAutoBuilderFrame
from PyQt6.QtCore import Qt
from ..widgets.letter_type_picker import LetterTypePicker
from .freeform_auto_builder import FreeFormAutoBuilder

if TYPE_CHECKING:
    from ..auto_builder import AutoBuilder


class FreeformAutoBuilderFrame(BaseAutoBuilderFrame):
    def __init__(self, auto_builder: "AutoBuilder") -> None:
        super().__init__(auto_builder, "freeform")
        self.builder = FreeFormAutoBuilder(self)

        # Attach specific action for sequence creation
        self.create_sequence_button.clicked.connect(self._on_create_sequence)
        self.letter_type_picker = LetterTypePicker(self)  # Instantiate LetterTypePicker
        self.layout.addWidget(self.letter_type_picker)  # Add LetterTypePicker to layout
        self.layout.addStretch(1)
        self.layout.addWidget(
            self.create_sequence_button, alignment=Qt.AlignmentFlag.AlignCenter
        )
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

    def apply_settings(self):
        super().apply_settings()
        self.letter_type_picker.apply_settings()  # Apply settings to LetterTypePicker

    def _resize_widgets(self):
        super()._resize_widgets()
        self.letter_type_picker.resize_letter_type_picker()  # Resize LetterTypePicker
