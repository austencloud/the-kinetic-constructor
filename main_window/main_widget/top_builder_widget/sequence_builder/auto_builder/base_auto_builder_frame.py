from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QWidget,
    QSlider,
)
from PyQt6.QtCore import Qt
from pytoggle import PyToggle

if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_builder.auto_builder.auto_builder import (
        AutoBuilder,
    )


from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSlider,
)
from PyQt6.QtCore import Qt

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
        self.labels: dict[str, QLabel] = {}
        self.turn_intensity_buttons: dict[str, QPushButton] = {}
        self.level_buttons: dict[str, QPushButton] = {}
        self.length_buttons: dict[str, QPushButton] = {}
        self.turn_intensity_buttons: dict[str, QPushButton] = {}
        self.layout: QVBoxLayout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)
        self.init_shared_ui()

    def init_shared_ui(self):
        """Initialize the shared UI elements for all Auto Builders."""
        self._setup_ui_elements()

    def _setup_ui_elements(self):
        """Setup the UI elements."""
        self.level_buttons_layout = self._create_level_buttons_layout()
        self.length_adjustment_layout = self._create_length_adjustment_layout()
        self.max_turn_intensity_layout = (
            self._create_max_turn_intensity_adjustment_layout()
        )
        self.continuous_rotation_layout = self.setup_continuous_rotation_toggle()

        self.create_sequence_button = QPushButton("Create Sequence")
        self.create_sequence_button.setCursor(Qt.CursorShape.PointingHandCursor)

        self.sequence_level_label = QLabel("Level:")
        self.sequence_length_label = QLabel("Length:")
        self.max_turn_intensity_label = QLabel("Max Turn Intensity:")
        self.sequence_level_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.sequence_length_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.max_turn_intensity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.labels["sequence_level"] = self.sequence_level_label
        self.labels["sequence_length"] = self.sequence_length_label
        self.labels["max_turn_intensity"] = self.max_turn_intensity_label

        # Adding components to layout
        self.layout.addWidget(self.sequence_level_label)
        self.layout.addLayout(self.level_buttons_layout)
        self.layout.addStretch(1)
        self.layout.addWidget(self.sequence_length_label)
        self.layout.addLayout(self.length_adjustment_layout)
        self.layout.addStretch(1)
        self.layout.addWidget(self.max_turn_intensity_label)
        self.layout.addLayout(self.max_turn_intensity_layout)
        self.layout.addStretch(1)
        self.layout.addLayout(self.continuous_rotation_layout)
        self.layout.addStretch(1)
        self.layout.addWidget(
            self.create_sequence_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

    def _create_length_adjustment_layout(self) -> QHBoxLayout:
        """Create plus and minus buttons for adjusting sequence length."""
        layout = QHBoxLayout()

        self.minus_button = QPushButton("-")
        self.minus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.minus_button.clicked.connect(self._decrement_sequence_length)

        self.length_label = QLabel("8")  # Default sequence length
        self.length_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.length_label.setFixedWidth(40)

        self.plus_button = QPushButton("+")
        self.plus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.plus_button.clicked.connect(self._increment_sequence_length)

        self.length_buttons["minus"] = self.minus_button
        self.length_buttons["plus"] = self.plus_button

        self.labels["sequence_length_value"] = self.length_label

        layout.addStretch(8)
        layout.addWidget(self.minus_button)
        layout.addStretch(1)
        layout.addWidget(self.length_label)
        layout.addStretch(1)
        layout.addWidget(self.plus_button)
        layout.addStretch(8)

        return layout

    def _increment_sequence_length(self):
        """Increment the sequence length."""
        current_length = int(self.length_label.text())
        if current_length < 32:  # Limit the max value to 32
            new_length = current_length + 1
            self.length_label.setText(str(new_length))
            self._update_sequence_length(new_length)

    def _decrement_sequence_length(self):
        """Decrement the sequence length."""
        current_length = int(self.length_label.text())
        if current_length > 4:  # Limit the min value to 4
            new_length = current_length - 1
            self.length_label.setText(str(new_length))
            self._update_sequence_length(new_length)

    def apply_settings(self):
        """Press the buttons based on the settings."""
        level = self.auto_builder_settings.get_auto_builder_setting(
            "sequence_level", self.builder_type
        )
        length = self.auto_builder_settings.get_auto_builder_setting(
            "sequence_length", self.builder_type
        )
        turn_intensity = self.auto_builder_settings.get_auto_builder_setting(
            "max_turn_intensity", self.builder_type
        )
        self.level_buttons[f"sequence_level_{level}"].setChecked(True)
        self.length_label.setText(str(length))
        self.turn_intensity_label.setText(str(turn_intensity))
        self._update_sequence_level(level)
        self._update_sequence_length(length)
        self._update_max_turn_intensity(turn_intensity)

    def _create_max_turn_intensity_adjustment_layout(self) -> QHBoxLayout:
        """Create plus and minus buttons for adjusting Max Turn Intensity."""
        layout = QHBoxLayout()

        self.turn_minus_button = QPushButton("-")
        self.turn_minus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.turn_minus_button.clicked.connect(self._decrement_max_turn_intensity)

        self.turn_intensity_label = QLabel("1")  # Default turn intensity
        self.turn_intensity_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turn_intensity_label.setFixedWidth(40)

        self.turn_plus_button = QPushButton("+")
        self.turn_plus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.turn_plus_button.clicked.connect(self._increment_max_turn_intensity)

        self.turn_intensity_buttons["turn_minus"] = self.turn_minus_button
        self.turn_intensity_buttons["turn_plus"] = self.turn_plus_button

        self.labels["turn_intensity_value"] = self.turn_intensity_label

        layout.addStretch(8)
        layout.addWidget(self.turn_minus_button)
        layout.addStretch(1)
        layout.addWidget(self.turn_intensity_label)
        layout.addStretch(1)
        layout.addWidget(self.turn_plus_button)
        layout.addStretch(8)

        return layout

    def _increment_max_turn_intensity(self):
        """Increment the max turn intensity."""
        current_intensity = float(self.turn_intensity_label.text())
        if current_intensity < 30:  # Set a max limit for turn intensity
            new_intensity = int(current_intensity) + 1
            self.turn_intensity_label.setText(str(new_intensity))
            self._update_max_turn_intensity(new_intensity)

    def _decrement_max_turn_intensity(self):
        """Decrement the max turn intensity."""
        current_intensity = float(self.turn_intensity_label.text())
        if current_intensity > 0:  # Set a min limit for turn intensity
            new_intensity = int(current_intensity) - 1
            self.turn_intensity_label.setText(str(new_intensity))
            self._update_max_turn_intensity(new_intensity)

    def setup_continuous_rotation_toggle(self):
        """Setup the continuous rotation toggle."""
        self.continuous_label = QLabel("Continuous")
        self.random_label = QLabel("Random")
        self.labels["random_rotation"] = self.random_label
        self.labels["continuous_rotation"] = self.continuous_label
        layout = QHBoxLayout()
        self.continuous_rotation_toggle = PyToggle()
        self.continuous_rotation_toggle.stateChanged.connect(
            self._update_continuous_rotation
        )

        layout.addStretch(1)
        layout.addWidget(self.random_label)
        layout.addWidget(self.continuous_rotation_toggle)
        layout.addWidget(self.continuous_label)
        layout.addStretch(1)

        return layout

    def _create_level_buttons_layout(self) -> QHBoxLayout:
        """Create buttons for selecting sequence levels."""
        layout = QHBoxLayout()
        layout.addStretch(1)
        levels = [1, 2, 3]  # Level options
        for level in levels:
            level_button = QPushButton(f"{level}")
            level_button.setCursor(Qt.CursorShape.PointingHandCursor)
            level_button.setCheckable(True)
            level_button.clicked.connect(
                lambda _, l=level: self._update_sequence_level(l)
            )
            layout.addWidget(level_button)
            layout.addStretch(1)
            self.level_buttons[f"sequence_level_{level}"] = level_button
        return layout

    def _update_sequence_length(self, length: int):
        """Update the sequence length."""
        self.auto_builder_settings.set_auto_builder_setting(
            "sequence_length", length, self.builder_type
        )

    def _update_sequence_level(self, level: int):
        """Update sequence level based on button click."""
        self.auto_builder_settings.set_auto_builder_setting(
            "sequence_level", level, self.builder_type
        )

        for level_button in self.level_buttons.values():
            level_button.setChecked(False)
        self.level_buttons[f"sequence_level_{level}"].setChecked(True)

        if level == 1:
            self.max_turn_intensity_label.hide()
            self.turn_minus_button.hide()
            self.turn_plus_button.hide()
            self.turn_intensity_label.hide()
        else:
            self.max_turn_intensity_label.show()
            self.turn_minus_button.show()
            self.turn_plus_button.show()
            self.turn_intensity_label.show()

    def _update_max_turn_intensity(self, value: float):
        """Update Max Turn Intensity."""
        self.auto_builder_settings.set_auto_builder_setting(
            "max_turn_intensity", value, self.builder_type
        )

    def _update_continuous_rotation(self, state):
        """Update continuous rotation state."""
        self.auto_builder_settings.set_auto_builder_setting(
            "continuous_rotation", bool(state), self.builder_type
        )

    def _update_font_colors(self, color: str):
        """Update the font colors and optionally the font size for the labels."""
        self.font_color = color
        font_size = self.auto_builder.sequence_builder.width() // 30
        style = f"color: {color}; font-size: {font_size}px;"
        for label in self.labels.values():
            label.setStyleSheet(style)

    def _resize_auto_builder_frame(self):
        """Resize the auto builder frame based on the parent widget size."""
        font_size = self.auto_builder.sequence_builder.width() // 30

        # Update font size for labels and buttons
        for label in self.labels.values():
            label.setStyleSheet(f"font-size: {font_size}px;")
            label.updateGeometry()
            label.repaint()

        for level_button in self.level_buttons.values():
            level_button.setStyleSheet(f"font-size: {font_size}px;")
            level_button.updateGeometry()
            level_button.repaint()

        for sequence_length_button in self.length_buttons.values():
            sequence_length_button.setStyleSheet(f"font-size: {font_size}px;")
            sequence_length_button.updateGeometry()
            sequence_length_button.repaint()

        for max_turn_intensity_button in self.turn_intensity_buttons.values():
            max_turn_intensity_button.setStyleSheet(f"font-size: {font_size}px;")
            max_turn_intensity_button.updateGeometry()
            max_turn_intensity_button.repaint()

        self.create_sequence_button.setStyleSheet(f"font-size: {font_size}px;")
        self.create_sequence_button.updateGeometry()
        self.create_sequence_button.repaint()
        self.create_sequence_button.setFixedWidth(
            self.auto_builder.sequence_builder.width() // 3
        )
        self.create_sequence_button.setFixedHeight(
            self.auto_builder.sequence_builder.height() // 10
        )

        self.updateGeometry()
        self.repaint()
