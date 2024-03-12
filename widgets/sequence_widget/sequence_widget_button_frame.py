import json
import os
from PyQt6.QtWidgets import (
    QPushButton,
    QHBoxLayout,
    QFrame,
    QVBoxLayout,
)
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from Enums.letters import Letter
from constants import BLUE, RED

from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class SequenceWidgetButtonFrame(QFrame):
    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.main_widget = sequence_widget.main_widget
        self.json_handler = self.main_widget.json_manager.current_sequence_json_handler
        self.sequence_constructor = self.main_widget.main_tab_widget.sequence_builder
        self.graph_editor = self.sequence_widget.sequence_modifier.graph_editor
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
        sequence_data = (
            self.main_widget.json_manager.current_sequence_json_handler.load_current_sequence_json()
        )
        if not sequence_data:
            self.sequence_widget.indicator_label.show_indicator(
                "You must build a sequence before you can save it."
            )
            return
        sequence_name = "".join(
            [
                pictograph.get("letter", "")
                for pictograph in sequence_data
                if "letter" in pictograph
            ]
        )
        dictionary_folder = os.path.join(os.getcwd(), "dictionary")
        os.makedirs(dictionary_folder, exist_ok=True)
        filename = os.path.join(dictionary_folder, f"{sequence_name}.json")
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(sequence_data, file, indent=4, ensure_ascii=False)
        self.sequence_widget.indicator_label.show_indicator(
            "Sequence saved as " + sequence_name
        )
        print(f"Sequence saved to {filename}.")

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
        # self._reset_start_pos_pictograph_orientations()

    def _reset_start_pos_pictograph_orientations(self) -> None:
        start_pos_letters = [Letter.α, Letter.β, Letter.Γ]
        for letter in start_pos_letters:
            if letter in self.main_widget.all_pictographs:
                for pictograph_key, pictograph in self.main_widget.all_pictographs[
                    letter
                ].items():
                    self._reset_pictograph_prop_orientations(pictograph)

    def _reset_pictograph_prop_orientations(self, pictograph: Pictograph) -> None:
        default_left_orientation = self.orientations[
            self.sequence_constructor.start_pos_picker.default_ori_picker.current_left_orientation_index
        ]
        default_right_orientation = self.orientations[
            self.sequence_constructor.start_pos_picker.default_ori_picker.current_right_orientation_index
        ]
        pictograph.pictograph_dict["red_start_ori"] = default_right_orientation
        pictograph.pictograph_dict["blue_start_ori"] = default_left_orientation
        pictograph.props[RED].updater.update_prop(
            {"start_ori": default_right_orientation}
        )
        pictograph.props[BLUE].updater.update_prop(
            {"start_ori": default_left_orientation}
        )
        pictograph.updater.update_pictograph(pictograph.pictograph_dict)

    def _reset_beat_frame(self) -> None:
        for beat_view in self.beat_frame.beat_views:
            beat_view.setScene(None)
            beat_view.is_filled = False
        self.beat_frame.start_pos_view.setScene(None)
        self.beat_frame.start_pos_view.is_filled = False
        self.beat_frame.selection_manager.deselect_beat()

    def _clear_graph_editor(self) -> None:
        self.graph_editor.GE_pictograph_view.set_to_blank_grid()
        self.graph_editor.adjustment_panel.set_turns(0, 0)
        self.graph_editor.adjustment_panel.update_adjustment_panel()
