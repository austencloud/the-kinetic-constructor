from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

from .generate_tab_layout_manager import GenerateTabLayoutManager
from .generate_tab_controller import GenerateTabController

from .widgets.generator_type_toggle import GeneratorTypeToggle
from .widgets.level_selector import LevelSelector
from .widgets.length_adjuster import LengthAdjuster
from .widgets.turn_intensity_adjuster import TurnIntensityAdjuster
from .widgets.continuous_rotation_toggle import ContinuousRotationToggle
from .widgets.rotation_type_toggle import RotationTypeToggle

# from .widgets.permutation_type_toggle import PermutationTypeToggle
from .freeform.letter_type_picker_widget import LetterTypePickerWidget
from .customize_your_sequence_label import CustomizeSequenceLabel
from .generate_sequence_button import (
    GenerateSequenceButton,
)  # If you still want a custom class

from .freeform.freeform_sequence_builder import FreeFormSequenceBuilder
from .circular.circular_sequence_builder import CircularSequenceBuilder

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class GenerateTab(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget

        # Access your settings
        self.settings = main_widget.main_window.settings_manager.generate_tab_settings

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        # The controller that handles logic
        self.controller = GenerateTabController(self)

        # 1) Create all sub-widgets
        self._create_widgets()

        # 2) Layout them with a manager
        self.layout_manager = GenerateTabLayoutManager(self)
        self.layout_manager.arrange_layout()

        # 3) Create your sequence builders
        self.freeform_builder = FreeFormSequenceBuilder(self)
        self.circular_builder = CircularSequenceBuilder(self)

        # 4) Finally load settings, set up initial states
        self.controller.init_from_settings()

    def _create_widgets(self):
        """Instantiate child widgets."""

        self.customize_sequence_label = CustomizeSequenceLabel(self)

        # We now have two buttons for sequence creation:
        self.auto_complete_button = GenerateSequenceButton(self, "Auto-Complete")
        self.generate_button = GenerateSequenceButton(self, "Generate New")

        # Connect them: pass overwrite=False for auto-complete, True for new
        self.auto_complete_button.clicked.connect(
            lambda: self.controller.handle_generate_sequence(overwrite=False)
        )
        self.generate_button.clicked.connect(
            lambda: self.controller.handle_generate_sequence(overwrite=True)
        )

        # The rest of your config widgets:
        self.mode_toggle = GeneratorTypeToggle(self)
        self.level_selector = LevelSelector(self)
        self.length_adjuster = LengthAdjuster(self)
        self.turn_intensity = TurnIntensityAdjuster(self)
        self.rotation_toggle = ContinuousRotationToggle(self)
        self.letter_picker = LetterTypePickerWidget(self)
        self.rotation_type = RotationTypeToggle(self)
        # self.permutation_type = PermutationTypeToggle(self)  # If you bring it back

    def on_generator_type_changed(self, new_type: str):
        """Called by GeneratorTypeToggle._toggle_changed()"""
        self.controller.on_mode_changed(new_type)
