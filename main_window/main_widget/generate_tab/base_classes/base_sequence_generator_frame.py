from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtCore import Qt


from ..widgets.continuous_rotation_toggle import ContinuousRotationToggle
from ..widgets.length_adjuster import LengthAdjuster
from ..widgets.level_selector import LevelSelector
from ..widgets.turn_intensity_adjuster import TurnIntensityAdjuster

if TYPE_CHECKING:
    from ..generate_tab import GenerateTab


class BaseSequenceGeneratorFrame(QFrame):
    def __init__(
        self, sequence_generator_tab: "GenerateTab", builder_type: str
    ) -> None:
        super().__init__(sequence_generator_tab)
        self.sequence_generator_widget = sequence_generator_tab
        self.builder_type = builder_type
        self.sequence_generator_settings = (
            sequence_generator_tab.main_widget.main_window.settings_manager.builder_settings.sequence_generator
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
        level = self.sequence_generator_settings.get_sequence_generator_setting(
            "sequence_level", self.builder_type
        )
        length = self.sequence_generator_settings.get_sequence_generator_setting(
            "sequence_length", self.builder_type
        )
        intensity = self.sequence_generator_settings.get_sequence_generator_setting(
            "max_turn_intensity", self.builder_type
        )
        continuous_rotation = (
            self.sequence_generator_settings.get_sequence_generator_setting(
                "continuous_rotation", self.builder_type
            )
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

    def _resize_sequence_generator_frame(self):
        """Resize the auto builder frame based on the parent widget size."""
        self._resize_widgets()

    def _resize_widgets(self):
        self.continuous_rotation_toggle.resize_continuous_rotation_toggle()
        self.level_selector.resize_level_selector()
        self.length_adjuster.resize_length_adjuster()
        self.turn_intensity_adjuster.resize_max_turn_intensity_adjuster()

    def _update_sequence_length(self, length: int):
        self.sequence_generator_settings.set_sequence_generator_setting(
            "sequence_length", length, self.builder_type
        )

    def _update_sequence_level(self, level: int):
        self.sequence_generator_settings.set_sequence_generator_setting(
            "sequence_level", level, self.builder_type
        )

    def _update_max_turn_intensity(self, intensity: int):
        self.sequence_generator_settings.set_sequence_generator_setting(
            "max_turn_intensity", intensity, self.builder_type
        )

    def _update_continuous_rotation(self, state: bool):
        self.sequence_generator_settings.set_sequence_generator_setting(
            "continuous_rotation", state, self.builder_type
        )
