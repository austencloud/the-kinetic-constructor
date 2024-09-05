from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QComboBox,
    QSpinBox,
    QSlider,
    QLabel,
)
from PyQt6.QtCore import Qt


if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.sequence_widget import (
        SequenceWidget,
    )


class AutoBuilderDialogBase(QDialog):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.auto_builder_settings = None  # Should be set in subclass
        self.builder = None  # Should be set in subclass
        self._init_ui()

    def _init_ui(self):
        """Common UI setup for all auto-builder dialogs."""
        self.layout: QVBoxLayout = QVBoxLayout(self)

        # Sequence Length
        self.sequence_length_spinbox = QSpinBox()
        self.sequence_length_spinbox.valueChanged.connect(self._update_sequence_length)
        self.sequence_length_label = QLabel("Sequence Length (beats):")
        self.layout.addLayout(
            self._create_row(self.sequence_length_label, self.sequence_length_spinbox)
        )

        # Sequence Level
        self.sequence_level_combo = QComboBox()
        self.sequence_level_combo.addItem("Level 1: Radial", 1)
        self.sequence_level_combo.addItem("Level 2: Radial with Turns", 2)
        self.sequence_level_combo.addItem("Level 3: Non-Radial", 3)
        self.sequence_level_combo.currentIndexChanged.connect(
            self._update_sequence_level
        )
        self.sequence_level_label = QLabel("Sequence Level:")
        self.layout.addLayout(
            self._create_row(self.sequence_level_label, self.sequence_level_combo)
        )

        # Turn Intensity
        self.turn_intensity_slider = QSlider(Qt.Orientation.Horizontal)
        self.turn_intensity_slider.valueChanged.connect(self._update_turn_intensity)
        self.turn_intensity_label = QLabel("Turn Intensity:")
        self.layout.addLayout(
            self._create_row(self.turn_intensity_label, self.turn_intensity_slider)
        )

        # Max Turns
        self.max_turns_spinbox = QSpinBox()
        self.max_turns_spinbox.valueChanged.connect(self._update_max_turns)
        self.max_turns_label = QLabel("Max Number of Turns:")
        self.layout.addLayout(
            self._create_row(self.max_turns_label, self.max_turns_spinbox)
        )

        # Action Buttons
        self._setup_action_buttons()

        self.setLayout(self.layout)

    def _create_row(self, label, widget):
        """Helper to create a row with label and widget."""
        row = QHBoxLayout()
        row.addWidget(label)
        row.addWidget(widget)
        return row

    def _setup_action_buttons(self):
        """Add action buttons (Create and Cancel) to the layout."""
        button_layout = QHBoxLayout()
        create_button = QPushButton("Create Sequence")
        create_button.clicked.connect(self._on_create_sequence)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(create_button)
        self.layout.addLayout(button_layout)

    def _update_visibility_based_on_level(self):
        """Update visibility of turn settings based on selected sequence level."""
        is_visible = self.sequence_level_combo.currentData() > 1
        self.turn_intensity_label.setVisible(is_visible)
        self.turn_intensity_slider.setVisible(is_visible)
        self.max_turns_label.setVisible(is_visible)
        self.max_turns_spinbox.setVisible(is_visible)

    def _load_settings(self):
        """To be implemented in subclass for loading specific settings."""
        raise NotImplementedError

    def _update_sequence_length(self):
        """To be implemented in subclass for saving specific settings."""
        raise NotImplementedError

    def _update_sequence_level(self):
        """To be implemented in subclass for saving specific settings."""
        raise NotImplementedError

    def _update_turn_intensity(self):
        """To be implemented in subclass for saving specific settings."""
        raise NotImplementedError

    def _update_max_turns(self):
        """To be implemented in subclass for saving specific settings."""
        raise NotImplementedError

    def _on_create_sequence(self):
        """To be implemented in subclass for creating the sequence."""
        raise NotImplementedError

    def _resize_dialog(self):
        """Resize the dialog based on the parent widget size."""
        width, height = (
            int(self.sequence_widget.width() / 2),
            int(self.sequence_widget.height() / 3),
        )
        self.resize(width, height)

        # Increase the size of all the labels programmatically
        font = self.font()
        font_size = width // 40
        font.setPointSize(font_size)
        self.setFont(font)

        # Update font size for all labels and widgets
        for label in self.findChildren(QLabel):
            label.setFont(font)

        for widget in self.findChildren((QSpinBox, QComboBox)):
            widget.setFont(font)

        # Update button fonts
        for button in self.findChildren(QPushButton):
            button.setFont(font)
