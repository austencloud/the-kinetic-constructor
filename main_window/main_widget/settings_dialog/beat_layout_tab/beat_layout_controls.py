from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSpinBox,
)
from PyQt6.QtCore import Qt, pyqtSignal

if TYPE_CHECKING:
    from .beat_layout_tab import BeatLayoutTab


class BeatLayoutControls(QWidget):
    sequence_length_changed = pyqtSignal(int)
    layout_selected = pyqtSignal(str)

    def __init__(self, layout_tab: "BeatLayoutTab"):
        super().__init__(layout_tab)
        self.layout_tab = layout_tab
        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        # Sequence Length Controls
        self.sequence_length_label = QLabel("Sequence Length:", self)
        self.sequence_length_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.num_beats_spinbox = QSpinBox(self)
        self.num_beats_spinbox.setRange(1, 128)

        self.num_beats_spinbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.num_beats_spinbox.valueChanged.connect(
            lambda value: self.sequence_length_changed.emit(value)
        )

        self.minus_button = QPushButton("-", self)
        self.minus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.minus_button.clicked.connect(self._decrease_sequence_length)

        self.plus_button = QPushButton("+", self)
        self.plus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.plus_button.clicked.connect(self._increase_sequence_length)

        # Layout Dropdown and Navigation
        self.layout_dropdown_label = QLabel("Select Layout:", self)
        self.layout_dropdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_dropdown = QComboBox(self)
        self.layout_dropdown.setCursor(Qt.CursorShape.PointingHandCursor)
        self.layout_dropdown.addItems(
            [f"{rows} x {cols}" for rows, cols in self.layout_tab.valid_layouts]
        )
        self.layout_dropdown.currentTextChanged.connect(
            lambda layout: self.layout_selected.emit(layout)
        )

        self.num_beats_spinbox.setValue(
            len(
                self.layout_tab.sequence_widget.main_widget.json_manager.loader_saver.load_current_sequence_json()
            )
            - 2
        )

    def _setup_layout(self):
        controls_layout = QHBoxLayout()
        controls_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_layout.addWidget(self.minus_button)
        controls_layout.addWidget(self.num_beats_spinbox)
        controls_layout.addWidget(self.plus_button)

        dropdown_layout = QHBoxLayout()
        dropdown_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dropdown_layout.addWidget(self.layout_dropdown)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.sequence_length_label)
        self.layout.addLayout(controls_layout)
        self.layout.addWidget(self.layout_dropdown_label)
        self.layout.addLayout(dropdown_layout)

    def resizeEvent(self, event):
        """Dynamically adjust font sizes on resize."""
        font_size = max(10, self.width() // 50)
        font = self.sequence_length_label.font()
        font.setPointSize(font_size)

        widgets: list[QWidget] = [
            self.sequence_length_label,
            self.layout_dropdown_label,
            self.minus_button,
            self.plus_button,
            self.layout_dropdown,
        ]
        for widget in widgets:
            widget.setFont(font)

        # Adjust spin box font separately
        spinbox_font = self.num_beats_spinbox.font()
        spinbox_font.setPointSize(font_size)
        self.num_beats_spinbox.setFont(spinbox_font)

    def _decrease_sequence_length(self):
        """Decrease the sequence length and emit the change."""
        current_value = self.num_beats_spinbox.value()
        if current_value > 1:
            self.num_beats_spinbox.setValue(current_value - 1)

    def _increase_sequence_length(self):
        """Increase the sequence length and emit the change."""
        self.num_beats_spinbox.setValue(self.num_beats_spinbox.value() + 1)
