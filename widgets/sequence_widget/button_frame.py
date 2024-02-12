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
        # Logic to save the current sequence goes here
        pass

    def clear_sequence(self):
        # Logic to clear the current sequence goes here
        for beat_view in self.sequence_widget.beat_frame.beats:
            beat_view.clear()
        # Additional cleanup as necessary
