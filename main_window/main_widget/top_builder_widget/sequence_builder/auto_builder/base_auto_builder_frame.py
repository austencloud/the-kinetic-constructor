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

        # Widget dictionaries for easy access
        self.spinboxes: dict[str, QSpinBox] = {}
        self.comboboxes: dict[str, QComboBox] = {}
        self.labels: dict[str, QLabel] = {}
        self.buttons: dict[str, QPushButton] = {}
        self.checkboxes: dict[str, QCheckBox] = {}

        # Set up the layout
        self.grid_layout = QGridLayout()
        self.setLayout(self.grid_layout)

        self._init_ui()

    def _init_ui(self):
        """Initialize all UI components."""
        self._setup_ui_elements()
        self._populate_grid_layout()

    def _setup_ui_elements(self):
        """Setup the individual UI elements and add them to dictionaries."""
        # Create Spinbox for sequence length
        self._create_spinbox(
            "sequence_length", "Sequence Length", 1, 32, self._update_sequence_length
        )

        # Create ComboBox for sequence level
        self._create_combobox(
            "sequence_level",
            "Sequence Level",
            items=[
                ("Level 1: Base", 1),
                ("Level 2: Turns", 2),
                ("Level 3: Non-radial", 3),
            ],
            handler=self._update_sequence_level,
        )

        # Create ComboBox for max turn intensity
        self._create_combobox(
            "max_turn_intensity",
            "Max Turn Intensity",
            items=[str(i) for i in range(0, 4)],
            handler=self._update_max_turn_intensity,
        )

        # Create Checkbox for continuous rotation
        self._create_checkbox(
            "continuous_rotation",
            "Continuous Rotation",
            self._update_continuous_rotation,
        )

        # Create Button for creating sequence
        self._create_button("create_sequence", "Create Sequence")

    def _create_spinbox(
        self, key: str, label_text: str, min_val: int, max_val: int, handler
    ) -> None:
        """Create a SpinBox and associated label."""
        spinbox = QSpinBox()
        spinbox.setRange(min_val, max_val)
        spinbox.valueChanged.connect(handler)
        self.spinboxes[key] = spinbox

        label = QLabel(label_text)
        self.labels[key] = label

    def _create_combobox(self, key: str, label_text: str, items: list, handler) -> None:
        """Create a ComboBox with specified items and a label."""
        combobox = QComboBox()

        # Check if items are tuples (label, value) or just values
        if isinstance(items[0], tuple):
            for text, data in items:
                combobox.addItem(text, data)
        else:
            for item in items:
                combobox.addItem(item, item)  # Use item as both label and data

        combobox.currentIndexChanged.connect(handler)
        self.comboboxes[key] = combobox

        label = QLabel(label_text)
        self.labels[key] = label

    def _create_checkbox(self, key: str, text: str, handler) -> None:
        """Create a CheckBox with the specified text."""
        checkbox = QCheckBox(text)
        checkbox.stateChanged.connect(handler)
        self.checkboxes[key] = checkbox

    def _create_button(self, key: str, text: str) -> None:
        """Create a QPushButton."""
        button = QPushButton(text)
        self.buttons[key] = button

    def _populate_grid_layout(self):
        """Add UI elements to the grid layout."""
        self._add_to_grid("sequence_length", 0)
        self._add_to_grid("sequence_level", 1)
        self._add_to_grid("max_turn_intensity", 2)

        # Add other widgets separately
        self.grid_layout.addWidget(self.checkboxes["continuous_rotation"], 6, 1)
        self.grid_layout.addWidget(self.buttons["create_sequence"], 7, 0, 1, 2)

    def _add_to_grid(self, key: str, row: int):
        """Helper to add label and widget to the grid layout."""
        self.grid_layout.addWidget(
            self.labels[key], row, 0, Qt.AlignmentFlag.AlignRight
        )
        self.grid_layout.addWidget(
            self.spinboxes.get(key, self.comboboxes.get(key)),
            row,
            1,
            Qt.AlignmentFlag.AlignLeft,
        )

    def _load_settings(self):
        """Load and apply the settings for the builder."""
        settings = self.auto_builder_settings.get_auto_builder_settings(
            self.builder_type
        )
        self._apply_settings_to_ui(settings)

    def _apply_settings_to_ui(self, settings: dict):
        """Apply the settings to UI components."""
        self.spinboxes["sequence_length"].setValue(settings["sequence_length"])
        self.comboboxes["sequence_level"].setCurrentIndex(
            self.comboboxes["sequence_level"].findData(settings["sequence_level"])
        )
        self.comboboxes["max_turn_intensity"].setCurrentText(
            str(settings["max_turn_intensity"])
        )
        self.checkboxes["continuous_rotation"].setChecked(
            settings["continuous_rotation"]
        )
        self._update_visibility_based_on_level()

    def _update_sequence_length(self):
        """Handle updates to the sequence length."""
        self._set_builder_setting(
            "sequence_length", self.spinboxes["sequence_length"].value()
        )

    def _update_sequence_level(self):
        """Handle updates to the sequence level and adjust visibility."""
        level = self.comboboxes["sequence_level"].currentData()
        self._adjust_turn_intensity_based_on_level(level)
        self._set_builder_setting("sequence_level", level)

    def _adjust_turn_intensity_based_on_level(self, level: int):
        """Adjust turn intensity options based on sequence level."""
        all_turns = ["0.5", "1", "1.5", "2", "2.5", "3"]
        whole_turns = ["1", "2", "3"]
        intensity_options = all_turns if level == 3 else whole_turns

        self.comboboxes["max_turn_intensity"].clear()
        self.comboboxes["max_turn_intensity"].addItems(intensity_options)

    def _update_visibility_based_on_level(self):
        """Update visibility of turn settings based on sequence level."""
        is_visible = self.comboboxes["sequence_level"].currentData() > 1
        self.labels["max_turn_intensity"].setVisible(is_visible)
        self.comboboxes["max_turn_intensity"].setVisible(is_visible)

    def _update_max_turn_intensity(self):
        """Handle updates to the max turn intensity."""
        intensity = self.comboboxes["max_turn_intensity"].currentText()
        self._set_builder_setting("max_turn_intensity", float(intensity))

    def _update_continuous_rotation(self):
        """Handle updates to the continuous rotation setting."""
        self._set_builder_setting(
            "continuous_rotation", self.checkboxes["continuous_rotation"].isChecked()
        )

    def _set_builder_setting(self, setting_key: str, value):
        """Set a specific setting in the builder settings."""
        self.auto_builder_settings.set_auto_builder_setting(
            setting_key, value, self.builder_type
        )

    def update_font_colors(self, color: str):
        """Update the font colors for the labels."""
        for label in self.labels.values():
            label.setStyleSheet(f"color: {color};")
        self._resize_auto_builder_frame()

    def _resize_auto_builder_frame(self):
        """Resize the UI elements dynamically based on the window size."""
        font_size = self.auto_builder.sequence_builder.width() // 30
        for widget_dict in [
            self.labels,
            self.spinboxes,
            self.comboboxes,
            self.buttons,
            self.checkboxes,
        ]:
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
