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
        self.font_size = self.sequence_widget.width() // 45
        self.setup_save_sequence_button()
        self.setup_clear_sequence_button()
        self.setup_indicator_label()
        self.setup_layout()
        # Initialize the timer
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide_indicator)
    def setup_save_sequence_button(self):
        self.save_sequence_button = QPushButton("Save Sequence")
        self.save_sequence_button.clicked.connect(self.save_sequence)
        self.save_sequence_button.setFixedHeight(40)
        font = self.save_sequence_button.font()
        font.setPointSize(self.font_size)
        self.save_sequence_button.setFont(font)

    def setup_clear_sequence_button(self):
        self.clear_sequence_button = QPushButton("Clear Sequence")
        self.clear_sequence_button.clicked.connect(self.clear_sequence)
        self.clear_sequence_button.setFixedHeight(40)
        font = self.clear_sequence_button.font()
        font.setPointSize(self.font_size)
        self.clear_sequence_button.setFont(font)

    def setup_indicator_label(self):
        self.indicator_label = QLabel("")
        self.indicator_label.setStyleSheet("font-size: 16px; color: green;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def setup_layout(self):
        # Create a QHBoxLayout for the buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.save_sequence_button)
        buttons_layout.addWidget(self.clear_sequence_button)
        buttons_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align buttons to the center

        # Create a QHBoxLayout for the indicator label
        label_layout = QHBoxLayout()
        label_layout.addWidget(self.indicator_label)
        label_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Align label to the center

        # Create a QVBoxLayout as the master layout
        master_layout = QVBoxLayout(self)
        master_layout.addLayout(buttons_layout)
        master_layout.addLayout(label_layout)
        master_layout.setAlignment(Qt.AlignmentFlag.AlignTop)  # Align master layout to the top
        self.setLayout(master_layout)  # Set the master layout to the frame

    def resize_event(self, event):
        button_width = self.width() // 6
        self.save_sequence_button.setFixedWidth(button_width)
        self.clear_sequence_button.setFixedWidth(button_width)
        super().resize_event(event)


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
        # Check if the timer is running and restart it
        if self.timer.isActive():
            self.timer.stop()  # Stop the running timer
        self.timer.start(5000)  # Restart the timer for 5 seconds

    def hide_indicator(self):
        self.indicator_label.clear() 