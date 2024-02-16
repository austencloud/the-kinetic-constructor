import json
import os
from PyQt6.QtWidgets import (
    QPushButton,
    QSizePolicy,
    QHBoxLayout,
    QFrame,
    QLabel,
    QApplication,
    QVBoxLayout,
)
from PyQt6.QtCore import QTimer, Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class SequenceButtonFrame(QFrame):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.main_widget = sequence_widget.main_widget

        # Use QVBoxLayout to stack buttons vertically and include the indicator at the top
        self.layout: QVBoxLayout = QVBoxLayout(self)

        # Indicator label setup
        self.indicator_label = QLabel("Status: Ready")  # Initial placeholder text
        self.indicator_label.setStyleSheet("font-size: 16px; color: green;")
        self.layout.addWidget(self.indicator_label)  # Add the label to the layout

        # Save sequence button setup
        self.save_sequence_button = QPushButton("Save Sequence")
        self.save_sequence_button.clicked.connect(self.save_sequence)
        self.save_sequence_button.setStyleSheet("font-size: 16px;")
        self.layout.addWidget(self.save_sequence_button)

        # Clear sequence button setup
        self.clear_sequence_button = QPushButton("Clear Sequence")
        self.clear_sequence_button.clicked.connect(self.clear_sequence)
        self.clear_sequence_button.setStyleSheet("font-size: 16px;")
        self.layout.addWidget(self.clear_sequence_button)

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    def resizeEvent(self, event):
        # Set button width relative to parent's width for responsive design
        button_width = self.width() // 3
        self.save_sequence_button.setFixedWidth(button_width)
        self.clear_sequence_button.setFixedWidth(button_width)
        super().resizeEvent(event)

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
        self.show_indicator("Sequence saved")
        print(f"Sequence saved to {filename}.")

    def clear_sequence(self):
        for beat_view in self.sequence_widget.beat_frame.beats:
            beat_view.setScene(None)
            beat_view.is_filled = False
        self.sequence_widget.beat_frame.start_pos_view.setScene(None)
        self.sequence_widget.beat_frame.start_pos_view.is_filled = False
        self.main_widget.main_tab_widget.sequence_builder.reset_to_start_pos_picker()
        self.main_widget.main_tab_widget.sequence_builder.current_pictograph = (
            self.sequence_widget.beat_frame.start_pos
        )
        with open(
            self.main_widget.json_manager.current_sequence_json_handler.current_sequence_json,
            "w",
        ) as file:
            file.write("[]")
        self.show_indicator("Sequence cleared")

    def show_indicator(self, text):
        self.indicator_label.setText(text)
        self.indicator_label.show()

        # Hide the indicator after 5 seconds
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.timeout.connect(self.hide_indicator)
        timer.start(5000)  # 5000 milliseconds = 5 seconds

    def hide_indicator(self):
        self.indicator_label.hide()
        # Optionally adjust layout or perform other actions when hiding the label
