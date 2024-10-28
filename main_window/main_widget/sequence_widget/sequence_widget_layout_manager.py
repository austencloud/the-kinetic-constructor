from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QSizePolicy

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class SequenceWidgetLayoutManager:
    def __init__(self, sequence_widget: "SequenceWidget"):
        self.sequence_widget = sequence_widget

    def resize_sequence_widget(self) -> None:
        self.sequence_widget.current_word_label.resize_current_word_label()
        self.sequence_widget.button_panel.resize_button_frame()
        self.sequence_widget.beat_frame.resize_beat_frame()
        self.sequence_widget.graph_editor.resize_graph_editor()

    def setup_layout(self):
        self.setup_beat_frame_layout()
        self.setup_indicator_label_layout()
        layout: QVBoxLayout = QVBoxLayout(self.sequence_widget)

        current_word_layout = QVBoxLayout()
        current_word_layout.addWidget(self.sequence_widget.current_word_label)
        current_word_layout.addWidget(self.sequence_widget.difficulty_label)

        layout.addLayout(current_word_layout, 1)
        layout.addLayout(self.sequence_widget.beat_frame_layout, 12)
        layout.addWidget(self.sequence_widget.indicator_label, 1)
        layout.addWidget(
            self.sequence_widget.graph_editor.toggle_tab,
            alignment=Qt.AlignmentFlag.AlignBottom,
        )
        layout.addWidget(self.sequence_widget.graph_editor, 5)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.sequence_widget.graph_editor.update_graph_editor_visibility()
        self.sequence_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.sequence_widget.scroll_area.setWidget(self.sequence_widget.beat_frame)

        self.sequence_widget.setLayout(layout)

    def setup_beat_frame_layout(self):
        self.sequence_widget.beat_frame_layout = QHBoxLayout()
        self.sequence_widget.beat_frame_layout.addWidget(
            self.sequence_widget.scroll_area, 10
        )
        self.sequence_widget.beat_frame_layout.addWidget(
            self.sequence_widget.button_panel, 1
        )
        self.sequence_widget.beat_frame_layout.setContentsMargins(0, 0, 0, 0)
        self.sequence_widget.beat_frame_layout.setSpacing(0)

    def setup_indicator_label_layout(self):
        self.sequence_widget.indicator_label_layout = QHBoxLayout()
        self.sequence_widget.indicator_label_layout.addStretch(1)
        self.sequence_widget.indicator_label_layout.addWidget(
            self.sequence_widget.indicator_label
        )
        self.sequence_widget.indicator_label_layout.addStretch(1)

    def apply_layout_options(self, cols, rows, num_beats):
        self.sequence_widget.beat_frame.layout_manager.rearrange_beats(
            num_beats, cols, rows
        )
        self.sequence_widget.current_word_label.update_current_word_label_from_beats()
