from PyQt6.QtWidgets import (
    QPushButton,
    QHBoxLayout,
    QFrame,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class SequenceWidgetButtonFrame(QFrame):
    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.main_widget = sequence_widget.main_widget
        self.json_handler = self.main_widget.json_manager.current_sequence_json_handler
        self.sequence_constructor = (
            self.main_widget.main_builder_widget.sequence_builder
        )
        self.graph_editor = self.sequence_widget.sequence_modifier.graph_editor
        self.variation_manager = (
            self.main_widget.main_builder_widget.dictionary.variation_manager
        )
        self.beat_frame = self.sequence_widget.beat_frame
        self.indicator_label = sequence_widget.indicator_label
        self.orientations = ["in", "counter", "out", "clock"]

        self.font_size = self.sequence_widget.width() // 45
        self.setup_save_sequence_button()
        self.setup_clear_sequence_button()
        self.setup_layout()

    def setup_save_sequence_button(self) -> None:
        self.save_sequence_button = QPushButton("Save Sequence")
        self.save_sequence_button.clicked.connect(self.save_sequence)
        self.save_sequence_button.setFixedHeight(40)
        font = self.save_sequence_button.font()
        font.setPointSize(self.font_size)
        self.save_sequence_button.setFont(font)

    def setup_clear_sequence_button(self) -> None:
        self.clear_sequence_button = QPushButton("Clear Sequence")
        self.clear_sequence_button.clicked.connect(
            lambda: self.clear_sequence(show_indicator=True)
        )
        self.clear_sequence_button.setFixedHeight(40)
        font = self.clear_sequence_button.font()
        font.setPointSize(self.font_size)
        self.clear_sequence_button.setFont(font)

    def setup_save_turn_pattern_button(self) -> None:
        self.save_turn_pattern_button = QPushButton("Save Current Turn Pattern")
        turn_pattern_widget = self.sequence_widget.sequence_modifier.turn_pattern_widget
        self.save_turn_pattern_button.clicked.connect(
            turn_pattern_widget.save_turn_pattern
        )
        self.save_turn_pattern_button.setFixedHeight(40)
        font = self.save_turn_pattern_button.font()
        font.setPointSize(self.font_size)
        self.save_turn_pattern_button.setFont(font)

    def setup_layout(self) -> None:
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.save_sequence_button)
        buttons_layout.addWidget(self.clear_sequence_button)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        label_layout = QHBoxLayout()
        label_layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop
        )

        master_layout = QVBoxLayout(self)
        master_layout.addLayout(buttons_layout)
        master_layout.addLayout(label_layout)
        master_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.setLayout(master_layout)

    def resize_event(self, event) -> None:
        button_width = self.width() // 6
        self.save_sequence_button.setFixedWidth(button_width)
        self.clear_sequence_button.setFixedWidth(button_width)

    def save_sequence(self) -> None:
        self.sequence = self.json_handler.load_current_sequence_json()
        if not self.sequence:
            self.sequence_widget.indicator_label.show_indicator(
                "You must build a sequence before you can save it."
            )
            return

        base_pattern = "".join(
            pictograph.get("letter", "")
            for pictograph in self.sequence
            if "letter" in pictograph
        )
        self.variation_manager.save_structural_variation(self.sequence, base_pattern)
        self.indicator_label.show_indicator(
            f"Structural variation saved for {base_pattern}"
        )

        self.main_widget.main_builder_widget.dictionary.reload_dictionary_tab()

    def clear_sequence(
        self, show_indicator=True, should_reset_to_start_pos_picker=True
    ) -> None:
        self._reset_beat_frame()
        if should_reset_to_start_pos_picker:
            self.sequence_constructor.reset_to_start_pos_picker()
        self.sequence_constructor.current_pictograph = self.beat_frame.start_pos
        self.json_handler.clear_current_sequence_file()
        if show_indicator:
            self.sequence_widget.indicator_label.show_indicator("Sequence cleared")
        self._clear_graph_editor()

    def _reset_beat_frame(self) -> None:
        for beat_view in self.beat_frame.beat_views:
            beat_view.setScene(None)
            beat_view.is_filled = False
        self.beat_frame.start_pos_view.setScene(None)
        self.beat_frame.start_pos_view.is_filled = False
        self.beat_frame.selection_manager.deselect_beat()

    def _clear_graph_editor(self) -> None:
        self.graph_editor.GE_pictograph_view.set_to_blank_grid()
        self.graph_editor.adjustment_panel.update_turns_displays(0, 0)
        self.graph_editor.adjustment_panel.update_adjustment_panel()
