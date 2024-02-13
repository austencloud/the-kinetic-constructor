import json
import os
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QFrame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class SequenceButtonFrame(QFrame):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.main_widget = sequence_widget.main_widget
        self.layout = QHBoxLayout()

        self.save_sequence_button = QPushButton("Save Sequence")
        self.save_sequence_button.clicked.connect(self.save_sequence)
        self.layout.addWidget(self.save_sequence_button)

        self.clear_sequence_button = QPushButton("Clear Sequence")
        self.clear_sequence_button.clicked.connect(self.clear_sequence)
        self.layout.addWidget(self.clear_sequence_button)

        self.setLayout(self.layout)

    def save_sequence(self):
        sequence_data = (
            self.main_widget.json_manager.current_sequence_json_handler.load_sequence()
        )

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

        print(f"Sequence saved to {filename}.")

    def clear_sequence(self):
        for beat_view in self.sequence_widget.beat_frame.beats:
            beat_view.clear()

        with open(
            self.main_widget.json_manager.current_sequence_json_handler.current_sequence_json,
            "w",
        ) as file:
            file.write("[]")
