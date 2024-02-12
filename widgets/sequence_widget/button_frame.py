import json
import codecs
import os
from PyQt6.QtWidgets import QPushButton, QHBoxLayout, QFrame
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFileDialog

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class SequenceButtonFrame(QFrame):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.main_widget = sequence_widget.main_widget
        self.layout = QHBoxLayout()

        # Save Sequence Button
        self.save_sequence_button = QPushButton("Save Sequence")
        self.save_sequence_button.clicked.connect(self.save_sequence)
        self.layout.addWidget(self.save_sequence_button)

        # Clear Sequence Button
        self.clear_sequence_button = QPushButton("Clear Sequence")
        self.clear_sequence_button.clicked.connect(self.clear_sequence)
        self.layout.addWidget(self.clear_sequence_button)

        self.setLayout(self.layout)

    def save_sequence(self):
        sequence_data = [
            beat_view.beat.get.pictograph_dict()
            for beat_view in self.sequence_widget.beat_frame.beats
            if hasattr(beat_view.beat, "pictograph_dict")
        ]
        sequence_name = "".join([pictograph["letter"] for pictograph in sequence_data])
        library_folder = os.path.join(os.getcwd(), "library")
        os.makedirs(library_folder, exist_ok=True)
        filename = os.path.join(library_folder, f"{sequence_name}.json")
        with codecs.open(filename, "w", encoding="utf-8") as file:
            json.dump(sequence_data, file, indent=4, ensure_ascii=False)
        print(f"Sequence saved to {filename}.")

    def clear_sequence(self):
        # Logic to clear the current sequence goes here
        for beat_view in self.sequence_widget.beat_frame.beats:
            beat_view.clear()
        # empty the sequence json file too
        with open(
            self.sequence_widget.sequence_validation_engine.sequence_file, "w"
        ) as file:
            file.write("[]")
