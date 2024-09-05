from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QComboBox, QLabel
from main_window.main_widget.top_builder_widget.sequence_widget.auto_builder.base_auto_builder_dialog import (
    AutoBuilderDialogBase,
)
from main_window.main_widget.top_builder_widget.sequence_widget.auto_builder.circular_auto_builder import (
    CircularAutoBuilder,
)

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.sequence_widget import (
        SequenceWidget,
    )


class CircularAutoBuilderDialog(AutoBuilderDialogBase):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.auto_builder_settings = (
            sequence_widget.main_widget.main_window.settings_manager.auto_builder
        )
        self.builder = CircularAutoBuilder(self)
        self.prev_rotation_type = None
        self._init_additional_ui()
        self._load_settings()
        # set the window title to Circular Auto Builder
        self.setWindowTitle("Circular Auto Builder")
        self._resize_dialog()

    def _init_additional_ui(self):
        """Setup Circular-specific UI components."""
        # Rotation Type
        self.rotation_type_combo = QComboBox()
        self.rotation_type_combo.addItem("Quartered", "quartered")
        self.rotation_type_combo.addItem("Halved", "halved")
        self.rotation_type_combo.currentIndexChanged.connect(self._update_rotation_type)
        self.rotation_type_label = QLabel("Rotation Type:")
        self.layout.insertLayout(
            3, self._create_row(self.rotation_type_label, self.rotation_type_combo)
        )

        # Permutation Type
        self.permutation_type_combo = QComboBox()
        self.permutation_type_combo.addItem("Rotational", "rotational")
        self.permutation_type_combo.addItem("Mirrored", "mirrored")
        self.permutation_type_combo.currentIndexChanged.connect(
            self._update_permutation_type
        )
        self.permutation_type_label = QLabel("Permutation Type:")
        self.layout.insertLayout(
            4,
            self._create_row(self.permutation_type_label, self.permutation_type_combo),
        )

    def _load_settings(self):
        """Load settings for Circular builder."""
        settings = self.auto_builder_settings.get_auto_builder_settings("circular")
        self.sequence_length_spinbox.setValue(settings["sequence_length"])
        self.sequence_level_combo.setCurrentIndex(
            self.sequence_level_combo.findData(settings["sequence_level"])
        )
        self.turn_intensity_slider.setValue(settings["turn_intensity"])
        self.max_turns_spinbox.setValue(settings["max_turns"])
        self.rotation_type_combo.setCurrentIndex(
            self.rotation_type_combo.findData(settings["rotation_type"])
        )
        self.permutation_type_combo.setCurrentIndex(
            self.permutation_type_combo.findData(settings["permutation_type"])
        )

        # Adjust visibility based on level and permutation type
        self._update_visibility_based_on_level()
        self._restrict_rotation_type()
        self._resize_dialog()

    def _update_sequence_length(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "sequence_length", self.sequence_length_spinbox.value(), "circular"
        )

    def _update_sequence_level(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "sequence_level", self.sequence_level_combo.currentData(), "circular"
        )
        self._update_visibility_based_on_level()

    def _update_turn_intensity(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "turn_intensity", self.turn_intensity_slider.value(), "circular"
        )

    def _update_max_turns(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "max_turns", self.max_turns_spinbox.value(), "circular"
        )

    def _update_rotation_type(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "rotation_type", self.rotation_type_combo.currentData(), "circular"
        )
        self._restrict_sequence_length()

    def _update_permutation_type(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "permutation_type", self.permutation_type_combo.currentData(), "circular"
        )
        self._restrict_rotation_type()

    def _restrict_sequence_length(self):
        """Restrict sequence length options based on rotation type."""
        if self.rotation_type_combo.currentData() == "quartered":
            self.sequence_length_spinbox.setRange(4, 32)
            self.sequence_length_spinbox.setSingleStep(4)
        elif self.rotation_type_combo.currentData() == "halved":
            self.sequence_length_spinbox.setRange(2, 32)
            self.sequence_length_spinbox.setSingleStep(2)

    def _restrict_rotation_type(self):
        """Restrict rotation type if mirrored permutation is selected."""
        if self.permutation_type_combo.currentData() == "mirrored":
            self.prev_rotation_type = self.rotation_type_combo.currentData()
            self.rotation_type_combo.setCurrentIndex(
                self.rotation_type_combo.findData("halved")
            )
            self.rotation_type_label.hide()
            self.rotation_type_combo.hide()
        else:
            self.rotation_type_label.show()
            self.rotation_type_combo.show()
            (
                self.rotation_type_combo.setCurrentIndex(
                    self.rotation_type_combo.findData(self.prev_rotation_type)
                )
                if self.prev_rotation_type
                else self.sequence_widget.settings_manager.auto_builder.get_auto_builder_settings(
                    "circular"
                ).get(
                    "rotation_type"
                )
            )
        self._resize_dialog()

    def _on_create_sequence(self):
        """Trigger sequence creation based on settings."""
        self.builder.build_sequence(
            self.sequence_length_spinbox.value(),
            self.turn_intensity_slider.value(),
            self.sequence_level_combo.currentData(),
            self.max_turns_spinbox.value(),
            self.rotation_type_combo.currentData(),
            self.permutation_type_combo.currentData(),
        )
        self.accept()
