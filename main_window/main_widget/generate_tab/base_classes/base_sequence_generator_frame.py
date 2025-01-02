from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtCore import Qt



from ..widgets.continuous_rotation_toggle import ContinuousRotationToggle
from ..widgets.length_adjuster import LengthAdjuster
from ..widgets.level_selector import LevelSelector
from ..widgets.turn_intensity_adjuster import TurnIntensityAdjuster

if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.freeform.letter_type_picker_widget import LetterTypePickerWidget
    from main_window.main_widget.generate_tab.widgets.permutation_type_toggle import PermutationTypeToggle
    from main_window.main_widget.generate_tab.widgets.rotation_type_toggle import RotationTypeToggle
    from ..generate_tab import GenerateTab


class BaseSequenceGeneratorFrame(QFrame):
    letter_type_picker: "LetterTypePickerWidget" = None
    rotation_type_toggle: "RotationTypeToggle" = None
    permutation_type_toggle: "PermutationTypeToggle" = None
    
    def __init__(self, generate_tab: "GenerateTab", builder_type: str) -> None:
        super().__init__(generate_tab)
        self.generate_tab = generate_tab
        self.builder_type = builder_type
        self.generate_tab_settings = (
            generate_tab.main_widget.main_window.settings_manager.generate_tab_settings
        )

        # Create Layout
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

        # Modular widgets
        self.level_selector = LevelSelector(self)
        self.length_adjuster = LengthAdjuster(self)
        self.turn_intensity_adjuster = TurnIntensityAdjuster(self)
        self.continuous_rotation_toggle = ContinuousRotationToggle(self)

        self.layout.addStretch(1)
        self.layout.addWidget(self.level_selector)
        self.layout.addStretch(1)
        self.layout.addWidget(self.length_adjuster)
        self.layout.addStretch(1)
        self.layout.addWidget(self.turn_intensity_adjuster)
        self.layout.addStretch(1)
        self.layout.addWidget(self.continuous_rotation_toggle)
        self.layout.addStretch(1)

    def apply_settings(self):
        """Apply settings to modular widgets."""
        level = self.generate_tab_settings.get_sequence_generator_setting(
            "sequence_level", self.builder_type
        )
        length = self.generate_tab_settings.get_sequence_generator_setting(
            "sequence_length", self.builder_type
        )
        intensity = self.generate_tab_settings.get_sequence_generator_setting(
            "max_turn_intensity", self.builder_type
        )
        continuous_rotation = self.generate_tab_settings.get_sequence_generator_setting(
            "continuous_rotation", self.builder_type
        )
        continuous_rotation = (
            continuous_rotation.lower() == "true"
            if isinstance(continuous_rotation, str)
            else bool(continuous_rotation)
        )

        self.level_selector._on_level_change(int(level))
        self.length_adjuster.set_length(int(length))
        self.turn_intensity_adjuster.set_intensity(intensity)
        self.continuous_rotation_toggle.set_state(continuous_rotation)
        self.continuous_rotation_toggle.update_mode_label_styles()


    def _update_sequence_length(self, length: int):
        self.generate_tab_settings.set_sequence_generator_setting(
            "sequence_length", length, self.builder_type
        )

    def _update_sequence_level(self, level: int):
        self.generate_tab_settings.set_sequence_generator_setting(
            "sequence_level", level, self.builder_type
        )

    def _update_max_turn_intensity(self, intensity: int):
        self.generate_tab_settings.set_sequence_generator_setting(
            "max_turn_intensity", intensity, self.builder_type
        )

    def _update_continuous_rotation(self, state: bool):
        self.generate_tab_settings.set_sequence_generator_setting(
            "continuous_rotation", state, self.builder_type
        )

    def on_create_sequence(self, overwrite_sequence: bool):
        """Trigger sequence creation for the specific builder."""
        raise NotImplementedError

    def resizeEvent(self, event):
        """Resize the auto builder frame based on the parent widget size."""
        self.continuous_rotation_toggle.resize_continuous_rotation_toggle()
        self.level_selector.resize_level_selector()
        self.length_adjuster.resize_length_adjuster()
        self.turn_intensity_adjuster.resize_max_turn_intensity_adjuster()

    def show(self):
        """Display Freeform frame by setting it in the stacked layout."""
        self.generate_tab.stacked_layout.setCurrentWidget(self)
        self.generate_tab.current_sequence_generator = self.builder_type
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