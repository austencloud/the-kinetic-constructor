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

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class SequenceButtonFrame(QFrame):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.main_widget = sequence_widget.main_widget
        self.indicator_label = sequence_widget.indicator_label
        self.font_size = self.sequence_widget.width() // 45
        self.setup_save_sequence_button()
        self.setup_clear_sequence_button()
        self.setup_layout()
        # self.setStyleSheet("border: 1px solid black;")

    def setup_save_sequence_button(self):
        self.save_sequence_button = QPushButton("Save Sequence")
        self.save_sequence_button.clicked.connect(self.save_sequence)
        self.save_sequence_button.setFixedHeight(40)
        font = self.save_sequence_button.font()
        font.setPointSize(self.font_size)
        self.save_sequence_button.setFont(font)

    def setup_clear_sequence_button(self):
        self.clear_sequence_button = QPushButton("Clear Sequence")
        self.clear_sequence_button.clicked.connect(
            lambda: self.clear_sequence(show_indicator=True)
        )
        self.clear_sequence_button.setFixedHeight(40)
        font = self.clear_sequence_button.font()
        font.setPointSize(self.font_size)
        self.clear_sequence_button.setFont(font)

    def setup_layout(self):
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

    def resize_event(self, event):
        button_width = self.width() // 6
        self.save_sequence_button.setFixedWidth(button_width)
        self.clear_sequence_button.setFixedWidth(button_width)

    def save_sequence(self):
        sequence_data = (
            self.main_widget.json_manager.current_sequence_json_handler.load_sequence()
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
        library_folder = os.path.join(os.getcwd(), "library")
        os.makedirs(library_folder, exist_ok=True)
        filename = os.path.join(library_folder, f"{sequence_name}.json")
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(sequence_data, file, indent=4, ensure_ascii=False)
        self.sequence_widget.indicator_label.show_indicator(
            "Sequence saved as " + sequence_name
        )
        print(f"Sequence saved to {filename}.")

    def clear_sequence(self, show_indicator=True, reset_to_start_pos_picker=True):
        for beat_view in self.sequence_widget.beat_frame.beat_views:
            beat_view.setScene(None)
            beat_view.is_filled = False
        self.sequence_widget.beat_frame.start_pos_view.setScene(None)
        self.sequence_widget.beat_frame.start_pos_view.is_filled = False
        if reset_to_start_pos_picker:
            self.main_widget.main_tab_widget.sequence_builder.reset_to_start_pos_picker()
        self.main_widget.main_tab_widget.sequence_builder.current_pictograph = (
            self.sequence_widget.beat_frame.start_pos
        )
        with open(
            self.main_widget.json_manager.current_sequence_json_handler.current_sequence_json,
            "w",
        ) as file:
            file.write("[]")
        if show_indicator:
            self.sequence_widget.indicator_label.show_indicator("Sequence cleared")
        self.sequence_widget.beat_frame.selection_manager.deselect_beat()
        self.sequence_widget.sequence_modifier.graph_editor.GE_pictograph_view.set_to_blank_grid()
