from typing import TYPE_CHECKING
from main_window.main_widget.top_builder_widget.sequence_widget.auto_builder.base_auto_builder_dialog import (
    AutoBuilderDialogBase,
)
from .freeform_auto_builder import FreeFormAutoBuilder

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.sequence_widget import (
        SequenceWidget,
    )


class FreeformAutoBuilderDialog(AutoBuilderDialogBase):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.auto_builder_settings = (
            sequence_widget.main_widget.main_window.settings_manager.auto_builder
        )
        self.builder = FreeFormAutoBuilder(self)
        self._load_settings()
        self.setWindowTitle("Freeform Auto Builder")
        self._resize_dialog()

    def _load_settings(self):
        """Load settings for Freeform builder."""
        settings = self.auto_builder_settings.get_auto_builder_settings("freeform")
        self.sequence_length_spinbox.setValue(settings["sequence_length"])
        self.sequence_level_combo.setCurrentIndex(
            self.sequence_level_combo.findData(settings["sequence_level"])
        )
        self.turn_intensity_slider.setValue(settings["turn_intensity"])
        self.max_turns_spinbox.setValue(settings["max_turns"])

        # Adjust visibility based on level
        self._update_visibility_based_on_level()

        # Resize the dialog based on the parent widget size

    def _on_create_sequence(self):
        """Trigger sequence creation for Freeform."""
        self.builder.build_sequence(
            self.sequence_length_spinbox.value(),
            self.turn_intensity_slider.value(),
            self.sequence_level_combo.currentData(),
            self.max_turns_spinbox.value(),
        )
        self.accept()

    def _update_sequence_length(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "sequence_length", self.sequence_length_spinbox.value(), "freeform"
        )

    def _update_sequence_level(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "sequence_level", self.sequence_level_combo.currentData(), "freeform"
        )
        self._update_visibility_based_on_level()

    def _update_turn_intensity(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "turn_intensity", self.turn_intensity_slider.value(), "freeform"
        )

    def _update_max_turns(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "max_turns", self.max_turns_spinbox.value(), "freeform"
        )
