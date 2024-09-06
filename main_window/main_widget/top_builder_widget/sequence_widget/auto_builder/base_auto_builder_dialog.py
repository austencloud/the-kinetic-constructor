from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QComboBox,
    QSpinBox,
    QLabel,
    QWidget,
    QGridLayout,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.sequence_widget import (
        SequenceWidget,
    )


class AutoBuilderDialogBase(QDialog):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.auto_builder_settings = (
            sequence_widget.main_widget.main_window.settings_manager.auto_builder
        )
        self.builder = None  # Should be set in subclass
        self.builder_type = None  # Should be set in subclass
        self.spinboxes: dict[str, QSpinBox] = {}
        self.comboboxes: dict[str, QComboBox] = {}
        self.labels: dict[str, QLabel] = {}
        self.buttons: dict[str, QPushButton] = {}

        self._init_ui()

    def _init_ui(self):
        """Common UI setup for all auto-builder dialogs using a grid layout."""
        self.grid_layout = QGridLayout()

        # Sequence Length Spinbox
        self.sequence_length_spinbox = QSpinBox()
        self.sequence_length_spinbox.valueChanged.connect(self._update_sequence_length)
        self.sequence_length_label = QLabel("Sequence Length (beats):")
        self.labels["sequence_length"] = self.sequence_length_label
        self.spinboxes["sequence_length"] = self.sequence_length_spinbox
        self._add_to_grid(self.sequence_length_label, self.sequence_length_spinbox, 0)

        # Sequence Level Combobox
        self.sequence_level_combo = QComboBox()
        self.sequence_level_combo.addItem("Level 1: Base", 1)
        self.sequence_level_combo.addItem("Level 2: Turns", 2)
        self.sequence_level_combo.addItem("Level 3: Non-radial", 3)
        self.sequence_level_combo.currentIndexChanged.connect(
            self._update_sequence_level
        )
        self.sequence_level_label = QLabel("Sequence Level:")
        self.labels["sequence_level"] = self.sequence_level_label
        self.comboboxes["sequence_level"] = self.sequence_level_combo
        self._add_to_grid(self.sequence_level_label, self.sequence_level_combo, 1)

        # Max Turn Intensity Combobox
        self.max_turn_intensity_combo = QComboBox()
        self.max_turn_intensity_label = QLabel("Maximum Turn Intensity:")
        self.labels["max_turn_intensity"] = self.max_turn_intensity_label
        self.comboboxes["max_turn_intensity"] = self.max_turn_intensity_combo
        # connect the signal to the slot
        self.max_turn_intensity_combo.currentIndexChanged.connect(
            self._update_max_turn_intensity
        )
        self._add_to_grid(
            self.max_turn_intensity_label, self.max_turn_intensity_combo, 2
        )

        # Max Turns Spinbox
        self.max_turns_spinbox = QSpinBox()
        self.max_turns_spinbox.valueChanged.connect(self._update_max_turns)
        self.max_turns_label = QLabel("Max Number of Turns:")
        self.labels["max_turns"] = self.max_turns_label
        self.spinboxes["max_turns"] = self.max_turns_spinbox
        self._add_to_grid(self.max_turns_label, self.max_turns_spinbox, 3)
        # connect the signal to the slot
        self.max_turns_spinbox.valueChanged.connect(self._update_max_turns)

        # Spacer to push buttons to the bottom
        self.grid_layout.setRowStretch(4, 1)

        # Action Buttons
        self._setup_action_buttons()

        # Set the grid layout as the main layout of the dialog
        self.setLayout(self.grid_layout)

    def _add_to_grid(self, label: QLabel, widget: QWidget, row: int):
        """Helper to add label and widget to grid layout."""
        self.grid_layout.addWidget(label, row, 0, Qt.AlignmentFlag.AlignRight)
        self.grid_layout.addWidget(widget, row, 1, Qt.AlignmentFlag.AlignLeft)

    def _update_sequence_level(self):
        """Update sequence level and adjust turn intensity options accordingly."""
        level = self.sequence_level_combo.currentData()

        all_turns = ["0.5", "1", "1.5", "2", "2.5", "3"]
        whole_turns = ["1", "2", "3"]
        settings = self.auto_builder_settings.get_auto_builder_settings(
            self.builder_type
        )
        current_intensity_in_settings = settings["max_turn_intensity"]
        if level == 3:
            self.max_turn_intensity_combo.clear()
            self.max_turn_intensity_combo.addItems(all_turns)
            self.max_turn_intensity_combo.setCurrentText(
                str(current_intensity_in_settings)
                if current_intensity_in_settings
                else self.get_closest_value_in_combobox(
                    current_intensity_in_settings,
                    self.max_turn_intensity_combo,
                    all_turns,
                )
            )
        elif level == 2:
            self.max_turn_intensity_combo.clear()
            self.max_turn_intensity_combo.addItems(whole_turns)
            self.max_turn_intensity_combo.setCurrentText(
                str(current_intensity_in_settings)
                if current_intensity_in_settings
                else self.get_closest_value_in_combobox(
                    current_intensity_in_settings,
                    self.max_turn_intensity_combo,
                    whole_turns,
                )
            )

        self._update_visibility_based_on_level()
        self.auto_builder_settings.set_auto_builder_setting(
            "sequence_level", self.sequence_level_combo.currentData(), self.builder_type
        )

    def get_closest_value_in_combobox(
        self, value: float, combobox: QComboBox, items: list[str]
    ) -> str:
        """Get the closest value to the given value in the combobox items."""
        # if the value is 2.5, we'll want to round it down to 2.
        # if the value is 1.5, we'll want to round it down to 1.
        if value % 1 == 0:
            return str(int(value))
        return str(round(value)) if round(value) in items else str(int(value))

    def _update_max_turn_intensity(self):
        """Update the max turns based on selected intensity."""
        current_intensity = self.max_turn_intensity_combo.currentText()
        if not current_intensity:
            return
        current_intensity = float(current_intensity)

        # Display integer values without decimal places, and floats when applicable
        if current_intensity.is_integer():
            self.max_turn_intensity_combo.setCurrentText(f"{int(current_intensity)}")
        else:
            self.max_turn_intensity_combo.setCurrentText(f"{current_intensity:.1f}")
        # resize the combobox to be wide enough to accommodate a float, regardless of the current value
        self.max_turn_intensity_combo.setMinimumContentsLength(2)
        self.auto_builder_settings.set_auto_builder_setting(
            "max_turn_intensity",
            (
                float(self.max_turn_intensity_combo.currentText())
                if not current_intensity.is_integer()
                else int(current_intensity)
            ),
            self.builder_type,
        )

    def _setup_action_buttons(self):
        """Add action buttons (Create and Cancel) to the layout."""
        button_layout = QHBoxLayout()
        create_button = QPushButton("Create Sequence")
        create_button.clicked.connect(self._on_create_sequence)
        cancel_button = QPushButton("Cancel")
        self.buttons["create"] = create_button
        self.buttons["cancel"] = cancel_button
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        button_layout.addWidget(create_button)

        # Add buttons at the bottom of the grid
        button_widget = QWidget()
        button_widget.setLayout(button_layout)
        self.grid_layout.addWidget(
            button_widget, 6, 0, 1, 2, Qt.AlignmentFlag.AlignBottom
        )

    def _update_visibility_based_on_level(self):
        """Update visibility of turn settings based on selected sequence level."""
        is_visible = self.sequence_level_combo.currentData() > 1
        self.max_turn_intensity_label.setVisible(is_visible)
        self.max_turn_intensity_combo.setVisible(is_visible)
        self.max_turns_label.setVisible(is_visible)
        self.max_turns_spinbox.setVisible(is_visible)

    def _load_settings(self):
        """To be implemented in subclass for loading specific settings."""
        raise NotImplementedError

    def _update_sequence_length(self):
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

        # Adjust font size based on dialog width
        font = self.font()
        font_size = width // 25
        font.setPointSize(font_size)

        # Apply font and stylesheet to all relevant widgets
        widget_dicts: list[dict[str, QWidget]] = [
            self.labels,
            self.spinboxes,
            self.comboboxes,
            self.buttons,
        ]
        for widget_dict in widget_dicts:
            for widget in widget_dict.values():
                widget.setFont(font)
                widget.setStyleSheet(f"QWidget {{ font-size: {font_size}px; }}")
                widget.updateGeometry()
                widget.repaint()

        self.updateGeometry()
        self.repaint()
