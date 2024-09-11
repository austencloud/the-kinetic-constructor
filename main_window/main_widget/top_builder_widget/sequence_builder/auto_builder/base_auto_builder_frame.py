from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QComboBox,
    QSpinBox,
    QCheckBox,
    QPushButton,
    QGridLayout,
    QWidget,
)
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_builder.auto_builder.auto_builder import (
        AutoBuilder,
    )


class BaseAutoBuilderFrame(QFrame):
    def __init__(self, auto_builder: "AutoBuilder", builder_type: str) -> None:
        super().__init__(auto_builder)
        self.auto_builder = auto_builder
        self.builder_type = builder_type
        self.auto_builder_settings = (
            auto_builder.main_widget.main_window.settings_manager.builder_settings.auto_builder
        )

        # Widget dictionaries
        self.spinboxes: dict[str, QSpinBox] = {}
        self.comboboxes: dict[str, QComboBox] = {}
        self.labels: dict[str, QLabel] = {}
        self.buttons: dict[str, QPushButton] = {}
        self.checkboxes: dict[str, QCheckBox] = {}
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)
        self.font_color = "black"
        self.init_shared_ui()

    def init_shared_ui(self):
        """Initialize the shared UI elements for all Auto Builders."""
        self._setup_ui_elements()
        self._add_ui_elements_to_grid()

    def _setup_ui_elements(self):
        """Setup the UI elements."""
        # Sequence Length Spinbox
        self.sequence_length_spinbox = QSpinBox()
        self.sequence_length_spinbox.setMinimum(1)
        self.sequence_length_spinbox.setMaximum(32)
        self.sequence_length_spinbox.valueChanged.connect(self._update_sequence_length)
        self.sequence_length_label = QLabel("Sequence Length")
        self.labels["sequence_length"] = self.sequence_length_label
        self.spinboxes["sequence_length"] = self.sequence_length_spinbox

        # Sequence Level ComboBox
        self.sequence_level_combo = QComboBox()
        self.sequence_level_combo.addItem("Level 1: Base", 1)
        self.sequence_level_combo.addItem("Level 2: Turns", 2)
        self.sequence_level_combo.addItem("Level 3: Non-radial", 3)
        self.sequence_level_combo.currentIndexChanged.connect(
            self._update_sequence_level
        )
        self.sequence_level_label = QLabel("Sequence Level")
        self.labels["sequence_level"] = self.sequence_level_label
        self.comboboxes["sequence_level"] = self.sequence_level_combo

        # Max Turn Intensity ComboBox
        self.max_turn_intensity_combo = QComboBox()
        self.max_turn_intensity_combo.addItems([str(i) for i in range(0, 4)])
        self.max_turn_intensity_combo.currentIndexChanged.connect(
            self._update_max_turn_intensity
        )
        self.max_turn_intensity_label = QLabel("Max Turn Intensity")
        self.labels["max_turn_intensity"] = self.max_turn_intensity_label
        self.comboboxes["max_turn_intensity"] = self.max_turn_intensity_combo

        # Continuous Rotation Checkbox
        self.continuous_rotation_checkbox = QCheckBox("Continuous Rotation")
        self.continuous_rotation_checkbox.stateChanged.connect(
            self._update_continuous_rotation
        )
        self.checkboxes["continuous_rotation"] = self.continuous_rotation_checkbox

        # Create Sequence Button
        self.create_sequence_button = QPushButton("Create Sequence")
        self.buttons["create_sequence"] = self.create_sequence_button

    def _add_ui_elements_to_grid(self):
        """Add the UI elements to the grid layout."""
        self._add_to_grid(self.sequence_length_label, self.sequence_length_spinbox, 0)
        self._add_to_grid(self.sequence_level_label, self.sequence_level_combo, 1)
        self._add_to_grid(
            self.max_turn_intensity_label, self.max_turn_intensity_combo, 2
        )
        self.grid_layout.addWidget(self.continuous_rotation_checkbox, 6, 1)
        self.grid_layout.addWidget(self.create_sequence_button, 7, 0, 1, 2)

    def _add_to_grid(self, label: QLabel, widget: QWidget, row: int):
        """Helper function to add label and widget to the grid layout."""
        self.grid_layout.addWidget(label, row, 0, Qt.AlignmentFlag.AlignRight)
        self.grid_layout.addWidget(widget, row, 1, Qt.AlignmentFlag.AlignLeft)

    def _load_settings(self):
        """Load settings for the builder."""
        settings = self.auto_builder_settings.get_auto_builder_settings(
            self.builder_type
        )
        self.sequence_length_spinbox.setValue(settings["sequence_length"])
        self.sequence_level_combo.setCurrentIndex(
            self.sequence_level_combo.findData(settings["sequence_level"])
        )
        self.max_turn_intensity_combo.setCurrentText(
            str(settings["max_turn_intensity"])
        )
        self.continuous_rotation_checkbox.setChecked(settings["continuous_rotation"])
        self._update_visibility_based_on_level()

    def _update_sequence_length(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "sequence_length", self.sequence_length_spinbox.value(), self.builder_type
        )

    def _update_sequence_level(self):
        """Update sequence level and adjust turn intensity options accordingly."""
        level = self.sequence_level_combo.currentData()
        all_turns = ["0.5", "1", "1.5", "2", "2.5", "3"]
        whole_turns = ["1", "2", "3"]

        current_intensity_in_settings = (
            self.auto_builder_settings.get_auto_builder_settings(self.builder_type)[
                "max_turn_intensity"
            ]
        )
        if level == 3:
            self.max_turn_intensity_combo.clear()
            self.max_turn_intensity_combo.addItems(all_turns)
        elif level == 2:
            self.max_turn_intensity_combo.clear()
            self.max_turn_intensity_combo.addItems(whole_turns)

        self.max_turn_intensity_combo.setCurrentText(str(current_intensity_in_settings))
        self._update_visibility_based_on_level()

        self.auto_builder_settings.set_auto_builder_setting(
            "sequence_level", self.sequence_level_combo.currentData(), self.builder_type
        )

    def _update_visibility_based_on_level(self):
        """Update visibility of turn settings based on selected sequence level."""
        is_visible = self.sequence_level_combo.currentData() > 1
        self.max_turn_intensity_label.setVisible(is_visible)
        self.max_turn_intensity_combo.setVisible(is_visible)

    def _update_max_turn_intensity(self):
        intensity = self.max_turn_intensity_combo.currentText()
        if intensity:
            self.auto_builder_settings.set_auto_builder_setting(
                "max_turn_intensity", float(intensity), self.builder_type
            )

    def _update_continuous_rotation(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "continuous_rotation",
            self.continuous_rotation_checkbox.isChecked(),
            self.builder_type,
        )

    def _update_font_colors(self, color: str):
        """Update the font colors and optionally the font size for the labels."""
        self.font_color = color
        font_size = self.auto_builder.sequence_builder.width() // 30
        style = f"color: {color}; font-size: {font_size}px;"
        for widget in list(self.labels.values()) + [self.continuous_rotation_checkbox]:
            widget.setStyleSheet(style)

    def _resize_auto_builder_frame(self):
        """Resize the frame based on the parent widget size."""
        font_size = self.auto_builder.sequence_builder.width() // 30

        widget_dicts: list[dict[str, QWidget]] = [
            self.labels,
            self.checkboxes,
        ]
        for widget_dict in widget_dicts:
            for widget in widget_dict.values():
                widget.setStyleSheet(
                    f"QWidget {{ font-size: {font_size}px; color: {self.font_color}; }}"
                )
                widget.updateGeometry()
                widget.repaint()

        other_widgets: list[dict[str, QWidget]] = [
            self.spinboxes,
            self.comboboxes,
            self.buttons,
        ]

        for widget_dict in other_widgets:
            for widget in widget_dict.values():
                widget.setStyleSheet(f"QWidget {{ font-size: {font_size}px; }}")
                widget.updateGeometry()
                widget.repaint()

        for combobox in self.comboboxes.values():
            text = combobox.currentText()
            metrics = combobox.fontMetrics()
            width = metrics.horizontalAdvance(text)
            combobox.setMinimumWidth(width + 25)

        self.updateGeometry()
        self.repaint()
