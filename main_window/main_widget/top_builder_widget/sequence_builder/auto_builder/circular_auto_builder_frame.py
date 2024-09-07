from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
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

from main_window.main_widget.top_builder_widget.sequence_builder.auto_builder.base_auto_builder_frame import (
    BaseAutoBuilderFrame,
)

from .circular_auto_builder import CircularAutoBuilder

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_builder.auto_builder.auto_builder import (
        AutoBuilder,
    )
    from main_window.main_widget.top_builder_widget.sequence_widget.sequence_widget import (
        SequenceWidget,
    )


class CircularAutoBuilderFrame(BaseAutoBuilderFrame):
    def __init__(self, auto_builder: "AutoBuilder") -> None:
        super().__init__(auto_builder, "circular")
        self.builder = CircularAutoBuilder(self)
        self.prev_rotation_type = (
            None  # To store the previous rotation type when restricting
        )

        # Add Circular-specific widgets
        self.rotation_type_combo = QComboBox()
        self.rotation_type_combo.addItem("Quartered", "quartered")
        self.rotation_type_combo.addItem("Halved", "halved")
        self.rotation_type_combo.currentIndexChanged.connect(self._update_rotation_type)
        self.rotation_type_label = QLabel("Rotation Type")
        self.labels["rotation_type"] = self.rotation_type_label
        self.comboboxes["rotation_type"] = self.rotation_type_combo
        self._add_to_grid(self.rotation_type_label, self.rotation_type_combo, 4)

        self.permutation_type_combo = QComboBox()
        self.permutation_type_combo.addItem("Rotational", "rotational")
        self.permutation_type_combo.addItem("Mirrored", "mirrored")
        self.permutation_type_combo.currentIndexChanged.connect(
            self._update_permutation_type
        )
        self.permutation_type_label = QLabel("Permutation Type")
        self.labels["permutation_type"] = self.permutation_type_label
        self.comboboxes["permutation_type"] = self.permutation_type_combo
        self._add_to_grid(self.permutation_type_label, self.permutation_type_combo, 5)

        # Attach specific action for sequence creation
        self.create_sequence_button.clicked.connect(self._on_create_sequence)

        # Load settings
        self._load_settings()

    def _load_settings(self):
        """Load settings for Circular builder."""
        super()._load_settings()
        settings = self.auto_builder_settings.get_auto_builder_settings(
            self.builder_type
        )
        self.rotation_type_combo.setCurrentIndex(
            self.rotation_type_combo.findData(settings["rotation_type"])
        )
        self.permutation_type_combo.setCurrentIndex(
            self.permutation_type_combo.findData(settings["permutation_type"])
        )

        self._restrict_rotation_type()  # Apply rotation type restrictions
        self._restrict_sequence_length()  # Apply sequence length restrictions

    def _restrict_sequence_length(self):
        """Restrict sequence length options based on rotation type."""
        if self.rotation_type_combo.currentData() == "quartered":
            if self.sequence_length_spinbox.value() % 4 != 0:
                self.sequence_length_spinbox.setValue(
                    self.sequence_length_spinbox.value()
                    + 4
                    - self.sequence_length_spinbox.value() % 4
                )
            self.sequence_length_spinbox.setRange(4, 32)
            self.sequence_length_spinbox.setSingleStep(4)
        elif self.rotation_type_combo.currentData() == "halved":
            self.sequence_length_spinbox.setRange(2, 32)
            self.sequence_length_spinbox.setSingleStep(2)

    def _restrict_rotation_type(self):
        """Restrict rotation type if 'mirrored' permutation is selected."""
        if self.permutation_type_combo.currentData() == "mirrored":
            self.prev_rotation_type = self.rotation_type_combo.currentData()
            self.rotation_type_combo.setCurrentIndex(
                self.rotation_type_combo.findData("halved")
            )
            self.rotation_type_combo.setEnabled(False)
        else:
            self.rotation_type_combo.setEnabled(True)
            if self.prev_rotation_type:
                self.rotation_type_combo.setCurrentIndex(
                    self.rotation_type_combo.findData(self.prev_rotation_type)
                )

    def _update_rotation_type(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "rotation_type", self.rotation_type_combo.currentData(), self.builder_type
        )
        self._restrict_sequence_length()

    def _update_permutation_type(self):
        self.auto_builder_settings.set_auto_builder_setting(
            "permutation_type",
            self.permutation_type_combo.currentData(),
            self.builder_type,
        )
        self._restrict_rotation_type()

    def _on_create_sequence(self):
        """Trigger sequence creation for Circular."""
        self.builder.build_sequence(
            self.sequence_length_spinbox.value(),
            float(self.max_turn_intensity_combo.currentText()),
            self.sequence_level_combo.currentData(),
            self.max_turns_spinbox.value(),
            self.rotation_type_combo.currentData(),
            self.permutation_type_combo.currentData(),
            self.continuous_rotation_checkbox.isChecked(),
        )
        self.auto_builder.sequence_builder.manual_builder.option_picker.update_option_picker()


    def _resize_circular_auto_builder_frame(self):
        """Resize the frame based on the parent widget size."""
        font = self.font()
        font_size = self.auto_builder.sequence_builder.width() // 30
        font.setPointSize(font_size)

        widget_dicts: list[dict[str, QWidget]] = [
            self.labels,
            self.spinboxes,
            self.comboboxes,
            self.buttons,
            self.checkboxes,
        ]
        for widget_dict in widget_dicts:
            for widget in widget_dict.values():
                widget.setFont(font)
                widget.setStyleSheet(f"QWidget {{ font-size: {font_size}px; }}")
                widget.updateGeometry()
                widget.repaint()

        self.updateGeometry()
        self.repaint()