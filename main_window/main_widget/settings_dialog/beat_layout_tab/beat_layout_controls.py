from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt, pyqtSignal

if TYPE_CHECKING:
    from .beat_layout_tab import BeatLayoutTab


class BeatLayoutControls(QWidget):
    sequence_length_changed = pyqtSignal(int)
    layout_selected = pyqtSignal(str)

    def __init__(
        self, parent_tab: "BeatLayoutTab"
    ):
        super().__init__(parent_tab)
        self.parent_tab = parent_tab

        # Initialize components
        self.sequence_length_label = QLabel("Sequence Length:", self)
        self.sequence_length_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.minus_button = QPushButton("-", self)
        self.minus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.minus_button.clicked.connect(self._decrease_sequence_length)

        self.plus_button = QPushButton("+", self)
        self.plus_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.plus_button.clicked.connect(self._increase_sequence_length)

        self.num_beats_label = QLabel(str(self.parent_tab.current_num_beats), self)
        self.num_beats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_dropdown_label = QLabel("Select Layout:", self)
        self.layout_dropdown_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout_dropdown = QComboBox(self)
        self.layout_dropdown.setCursor(Qt.CursorShape.PointingHandCursor)
        self.layout_dropdown.addItems(
            [f"{rows} x {cols}" for rows, cols in self.parent_tab.valid_layouts]
        )
        self.layout_dropdown.currentTextChanged.connect(self._on_layout_selected)

        self._setup_layout()

    def _setup_layout(self):
        """Setup the layout of the controls."""
        controls_layout = QHBoxLayout()
        controls_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        controls_layout.addWidget(self.minus_button)
        controls_layout.addWidget(self.num_beats_label)
        controls_layout.addWidget(self.plus_button)

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.sequence_length_label)
        self.layout.addLayout(controls_layout)
        self.layout.addWidget(self.layout_dropdown_label)
        self.layout.addWidget(self.layout_dropdown)

    def resizeEvent(self, event):
        """Dynamically adjust font sizes on resize."""
        font_size = max(10, self.width() // 50)
        font = self.sequence_length_label.font()
        font.setPointSize(font_size)
        
        self.sequence_length_label.setFont(font)
        self.num_beats_label.setFont(font)
        self.layout_dropdown_label.setFont(font)
        self.layout_dropdown.setFont(font)
        self.minus_button.setFont(font)
        self.plus_button.setFont(font)

    def _decrease_sequence_length(self):
        """Decrease the sequence length and emit the change."""
        if self.parent_tab.current_num_beats > 1:
            self.sequence_length_changed.emit(self.parent_tab.current_num_beats - 1)

    def _increase_sequence_length(self):
        """Increase the sequence length and emit the change."""
        self.sequence_length_changed.emit(self.parent_tab.current_num_beats + 1)

    def _on_layout_selected(self, layout_text: str):
        """Emit the selected layout."""
        self.layout_selected.emit(layout_text)

