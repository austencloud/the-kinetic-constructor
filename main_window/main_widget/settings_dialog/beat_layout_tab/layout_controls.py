from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QComboBox,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QSpinBox,
    QFrame,
)
from PyQt6.QtCore import Qt, pyqtSignal
from matplotlib.pylab import f
from data.beat_frame_layout_options import beat_frame_layout_options

if TYPE_CHECKING:
    from .beat_layout_tab import BeatLayoutTab


class LayoutControls(QWidget):
    layout_selected = pyqtSignal(str)
    update_default_layout = pyqtSignal()

    def __init__(self, layout_tab: "BeatLayoutTab"):
        super().__init__(layout_tab)
        self.layout_tab = layout_tab
        self.json_loader = (
            self.layout_tab.sequence_widget.main_widget.json_manager.loader_saver
        )
        self.beat_frame = layout_tab.beat_frame
        self.layout_settings = layout_tab.layout_settings
        self.settings_manager = layout_tab.settings_dialog.main_widget.settings_manager
        self._setup_components()
        self._setup_layout()

    def _setup_components(self):
        # Sequence Length Controls
        self.sequence_length_label = QLabel("Sequence Length:", self)
        self.sequence_length_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.num_beats_spinbox = QSpinBox(self)
        self.num_beats_spinbox.setRange(1, 64)
        self.num_beats_spinbox.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.num_beats_spinbox.setValue(self.layout_tab.num_beats)
        self.num_beats_spinbox.valueChanged.connect(
            lambda: self._on_sequence_length_changed(self.num_beats_spinbox.value())
        )

        self.minus_button = QPushButton("-", self)
        self.minus_button.clicked.connect(self._decrease_sequence_length)

        self.plus_button = QPushButton("+", self)
        self.plus_button.clicked.connect(self._increase_sequence_length)

        # Layout Dropdown
        self.layout_dropdown_label = QLabel("Options:", self)
        self.layout_dropdown_label.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.layout_dropdown = QComboBox(self)
        self.layout_dropdown.addItems(
            [f"{rows} x {cols}" for rows, cols in self.layout_tab.valid_layouts]
        )
        self.layout_dropdown.currentTextChanged.connect(
            lambda layout: self.layout_selected.emit(layout)
        )

        # Update Button and Default Layout Label
        self.update_button = QPushButton("Set as Default", self)
        self.update_button.clicked.connect(
            lambda: self.set_default_layout(self.layout_dropdown.currentText())
        )

        self.default_layout_label = QLabel(
            f"Default: {self.layout_tab.current_layout[0]} x {self.layout_tab.current_layout[1]}",
            self,
        )
        self.default_layout_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = self.default_layout_label.font()
        font.setBold(True)
        self.default_layout_label.setFont(font)

    def _apply_default_layout(self):
        """Update the default layout setting."""
        self.update_default_layout_label(self.current_layout)
        self.settings_manager.sequence_layout.set_layout_setting(
            str(self.layout_tab.num_beats), list(self.current_layout)
        )

    def set_default_layout(self, layout_text: str):
        self.layout_tab.num_beats = self.num_beats_spinbox.value()
        self.update_default_layout_label(layout_text)
        layout_tuple = tuple(map(int, layout_text.split(" x ")))
        self.layout_settings.set_layout_setting(
            str(self.layout_tab.num_beats), list(layout_tuple)
        )

    def get_default_layout_text(self):
        current_layout = self.layout_settings.get_layout_setting(
            str(self.layout_tab.num_beats)
        )
        return f"Default: {current_layout[0]} x {current_layout[1]}"

    def _setup_layout(self):
        # Sequence Length Section
        sequence_length_layout = QHBoxLayout()
        sequence_length_layout.setSpacing(10)
        sequence_length_layout.addWidget(self.minus_button)
        sequence_length_layout.addWidget(self.num_beats_spinbox)
        sequence_length_layout.addWidget(self.plus_button)
        sequence_length_frame = QFrame()
        sequence_length_frame.setLayout(sequence_length_layout)

        # Layout Dropdown Section
        layout_dropdown_layout = QHBoxLayout()
        layout_dropdown_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_dropdown_layout.setSpacing(10)
        layout_dropdown_layout.addWidget(self.layout_dropdown_label)
        layout_dropdown_layout.addWidget(self.layout_dropdown)
        layout_dropdown_frame = QFrame()
        layout_dropdown_frame.setLayout(layout_dropdown_layout)

        # Main Layout
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(20)
        self.layout.addWidget(self.sequence_length_label)
        self.layout.addWidget(sequence_length_frame)
        self.layout.addWidget(self.default_layout_label)
        self.layout.addWidget(layout_dropdown_frame)
        self.layout.addWidget(self.update_button)

    def _decrease_sequence_length(self):
        """Decrease the sequence length and emit the change."""
        current_value = self.num_beats_spinbox.value()
        if current_value > 1:
            self.num_beats_spinbox.setValue(current_value - 1)

    def _increase_sequence_length(self):
        """Increase the sequence length and emit the change."""
        self.num_beats_spinbox.setValue(self.num_beats_spinbox.value() + 1)

    def update_default_layout_label(self, layout_text):
        """Update the default layout label."""
        self.default_layout_label.setText(f"Default: {layout_text}")

    def _on_sequence_length_spinbox_changed(self, new_length: int):
        """Handle updates to the sequence length."""
        self.layout_tab.num_beats = new_length
        self.valid_layouts = beat_frame_layout_options.get(
            self.layout_tab.num_beats, [(1, 1)]
        )
        self.layout_dropdown.clear()
        self.layout_dropdown.addItems(
            [f"{cols} x {rows}" for cols, rows in self.valid_layouts]
        )
        self.current_layout = self.valid_layouts[0]
        self.num_beats_spinbox.setValue(self.layout_tab.num_beats)
        # self.beat_frame.update_preview()
        self.rearrange_beats(self.layout_tab.num_beats)
        self.update_default_layout_label(self.current_layout)

    def _on_layout_selected(self, layout_text: str):
        """Handle updates to the selected layout."""
        if layout_text:
            rows, cols = map(int, layout_text.split(" x "))
            self.current_layout = (rows, cols)
            # self.beat_frame.update_preview()
            self.rearrange_beats(self.layout_tab.num_beats)
            self.layout_settings.set_layout_setting(
                str(self.layout_tab.num_beats), list(self.current_layout)
            )

    def rearrange_beats(self, num_beats):
        """Update the beat frame to match the selected layout."""
        while self.beat_frame.layout.count():
            self.beat_frame.layout.takeAt(0).widget().hide()

        self.beat_frame.layout.addWidget(self.beat_frame.start_pos_view, 0, 0, 1, 1)
        self.beat_frame.start_pos_view.show()

        index = 0
        beats = self.beat_frame.beat_views
        for row in range(self.beat_frame.rows):
            for col in range(1, self.beat_frame.cols + 1):
                if index < num_beats:
                    if index < len(beats):
                        beat_view = beats[index]
                        self.beat_frame.layout.addWidget(beat_view, row, col)
                        beat_view.beat.beat_number_item.update_beat_number(index + 1)
                        beat_view.show()
                    index += 1
                else:
                    if index < len(beats):
                        beats[index].hide()
                        index += 1
        self.beat_frame.adjustSize()
        self.beat_frame.update_preview()

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
            self.update_button,
            self.default_layout_label,
        ]
        for widget in widgets:
            widget.setFont(font)

        spinbox_font = self.num_beats_spinbox.font()
        spinbox_font.setPointSize(font_size)
        self.num_beats_spinbox.setFont(spinbox_font)

    def _on_sequence_length_changed(self, new_length: int):
        self.num_beats = new_length
        self.valid_layouts = beat_frame_layout_options.get(self.num_beats, [(1, 1)])
        self.current_layout = self.layout_settings.get_layout_setting(
            str(self.num_beats)
        )
        self.layout_dropdown.clear()
        self.layout_dropdown.addItems(
            [f"{rows} x {cols}" for rows, cols in self.valid_layouts]
        )
        layout_text = f"{self.current_layout[0]} x {self.current_layout[1]}"
        self.layout_dropdown.setCurrentText(layout_text)

        self.beat_frame.update_preview()
        self.default_layout_label.setText(f"Default: {layout_text}")
