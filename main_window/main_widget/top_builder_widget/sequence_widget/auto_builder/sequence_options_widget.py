from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSpinBox, QComboBox, QLabel

from main_window.main_widget.top_builder_widget.sequence_widget.auto_builder.turn_settings_widget import TurnSettingsWidget


class SequenceOptionsWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Sequence Length
        layout.addWidget(QLabel("Sequence Length (beats):"))
        self.sequence_length_spinbox = QSpinBox()
        layout.addWidget(self.sequence_length_spinbox)

        # Sequence Level
        layout.addWidget(QLabel("Select Sequence Level:"))
        self.sequence_level_combo = QComboBox()
        self.sequence_level_combo.addItems(
            ["Level 1: Radial", "Level 2: Radial with Turns", "Level 3: Non-Radial"]
        )
        layout.addWidget(self.sequence_level_combo)

        # Turn Settings
        self.turn_settings_widget = TurnSettingsWidget()
        layout.addWidget(self.turn_settings_widget)

        # Connect sequence level changes to update the visibility of turn settings
        self.sequence_level_combo.currentIndexChanged.connect(self._update_turn_settings_visibility)

    def _update_turn_settings_visibility(self):
        level = self.sequence_level_combo.currentIndex() + 1
        if level == 1:
            self.turn_settings_widget.setVisible(False)
        else:
            self.turn_settings_widget.setVisible(True)
            if level == 2:
                self.turn_settings_widget.turn_intensity_slider.setRange(0, 3)
            elif level == 3:
                self.turn_settings_widget.turn_intensity_slider.setRange(0, 6)
