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
        # Load the current sequence which already includes the start position
        sequence_data = self.sequence_widget.sequence_validation_engine.load_sequence()

        # Generate a sequence name based on the letters of the sequence, skipping the start position entry
        sequence_name = "".join(
            [
                pictograph.get("letter", "")
                for pictograph in sequence_data
                if "letter" in pictograph
            ]
        )

        # Define the library folder and ensure it exists
        library_folder = os.path.join(os.getcwd(), "library")
        os.makedirs(library_folder, exist_ok=True)

        # Construct the filename using the sequence name
        filename = os.path.join(library_folder, f"{sequence_name}.json")

        # Save the sequence data to the file
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(sequence_data, file, indent=4, ensure_ascii=False)

        print(f"Sequence saved to {filename}.")

    def clear_sequence(self):
        # Logic to clear the current sequence goes here
        for beat_view in self.sequence_widget.beat_frame.beats:
            beat_view.clear()
        # empty the sequence json file too
        with open(
            self.main_widget.json_manager.current_sequence_json_handler.current_sequence_json,
            "w",
        ) as file:
            file.write("[]")
