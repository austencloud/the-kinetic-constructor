from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QComboBox,
)
from PyQt6.QtCore import Qt
from .layout_preview_beat_frame import LayoutPreviewBeatFrame

if TYPE_CHECKING:
    from main_window.main_widget.settings_dialog.settings_dialog import SettingsDialog


class BeatLayoutTab(QWidget):
    """Tab for configuring default beat layouts."""

    def __init__(self, settings_dialog: "SettingsDialog"):
        super().__init__(settings_dialog)
        self.settings_dialog = settings_dialog
        self.settings_manager = settings_dialog.main_widget.settings_manager
        self.sequence_widget = settings_dialog.main_widget.sequence_widget
        self.current_num_beats = 16  # Default to 16 beats
        self.valid_layouts = self._calculate_valid_layouts(self.current_num_beats)
        self.current_layout = self.valid_layouts[0]

        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Sequence Length Controls
        self.sequence_length_label = QLabel("Sequence Length:")
        self.sequence_length_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(self.sequence_length_label)

        controls_layout = QHBoxLayout()
        self.minus_button = QPushButton("-")
        self.minus_button.clicked.connect(self._decrease_sequence_length)
        self.plus_button = QPushButton("+")
        self.plus_button.clicked.connect(self._increase_sequence_length)
        self.num_beats_label = QLabel(str(self.current_num_beats))
        self.num_beats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_layout.addWidget(self.minus_button)
        controls_layout.addWidget(self.num_beats_label)
        controls_layout.addWidget(self.plus_button)
        layout.addLayout(controls_layout)

        # Dropdown for Layouts
        self.layout_dropdown_label = QLabel("Select Layout:")
        self.layout_dropdown_label.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(self.layout_dropdown_label)

        self.layout_dropdown = QComboBox()
        self.layout_dropdown.addItems(
            [f"{rows} x {cols}" for rows, cols in self.valid_layouts]
        )
        self.layout_dropdown.currentTextChanged.connect(self._on_layout_selected)
        layout.addWidget(self.layout_dropdown)

        # Add the preview frame
        self.preview_frame = LayoutPreviewBeatFrame(self)
        layout.addWidget(self.preview_frame, stretch=1)

    def _calculate_valid_layouts(self, num_beats: int):
        """Calculate all valid row/column combinations for a given number of beats."""
        layouts = [
            (rows, cols)
            for rows in range(1, num_beats + 1)
            for cols in range(1, num_beats + 1)
            if rows * cols >= num_beats
        ]
        return sorted(layouts, key=lambda x: (x[0] * x[1], abs(x[0] - x[1])))

    def _decrease_sequence_length(self):
        """Decrease the sequence length and update valid layouts."""
        if self.current_num_beats > 1:
            self.current_num_beats -= 1
            self.valid_layouts = self._calculate_valid_layouts(self.current_num_beats)
            self.layout_dropdown.clear()
            self.layout_dropdown.addItems(
                [f"{rows} x {cols}" for rows, cols in self.valid_layouts]
            )
            self.current_layout = self.valid_layouts[0]
            self.num_beats_label.setText(str(self.current_num_beats))
            self._update_layout()

    def _increase_sequence_length(self):
        """Increase the sequence length and update valid layouts."""
        self.current_num_beats += 1
        self.valid_layouts = self._calculate_valid_layouts(self.current_num_beats)
        self.layout_dropdown.clear()
        self.layout_dropdown.addItems(
            [f"{rows} x {cols}" for rows, cols in self.valid_layouts]
        )
        self.current_layout = self.valid_layouts[0]
        self.num_beats_label.setText(str(self.current_num_beats))
        self._update_layout()

    def _on_layout_selected(self, layout_text: str):
        """Handle layout selection from the dropdown."""
        if layout_text:
            rows, cols = map(int, layout_text.split(" x "))
            self.current_layout = (rows, cols)
            self._update_layout()

    def _update_layout(self):
        """Update the preview frame and the sequence widget beat frame layout."""
        self.preview_frame.update_preview()
        self.sequence_widget.beat_frame.layout_manager.configure_beat_frame(
            self.current_num_beats
        )
