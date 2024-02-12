import json
import os
from PyQt6.QtWidgets import QTreeView, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QDir, QModelIndex
from typing import TYPE_CHECKING

from widgets.pictograph.pictograph import Pictograph
from widgets.sequence_widget.beat_frame.start_pos_beat import StartPositionBeat

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
from widgets.sequence_widget.beat_frame.start_pos_beat import StartPositionBeat


class Library(QWidget):
    def __init__(self, main_widget: "MainWidget"):
        super().__init__(main_widget)
        self.main_widget = main_widget
        layout = QVBoxLayout(self)

        # File system model
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.currentPath() + "/library")

        # File tree view
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(QDir.currentPath() + "/library"))
        self.tree_view.doubleClicked.connect(
            self.on_double_clicked
        )  # Connect the doubleClicked signal
        layout.addWidget(self.tree_view)

        # Placeholder for preview area
        self.preview_area = QWidget()
        self.preview_area.setStyleSheet("background-color: gray;")
        layout.addWidget(self.preview_area)

        self.setLayout(layout)

    def on_double_clicked(self, index: QModelIndex):
        file_path = self.model.filePath(index)
        if file_path.endswith(".json"):
            self.load_sequence_from_file(file_path)
        else:
            QMessageBox.information(
                self, "Information", "Selected file is not a JSON sequence file."
            )

    def load_sequence_from_file(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                sequence_data = json.load(file)
                self.populate_sequence(sequence_data)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load sequence: {str(e)}")

    def populate_sequence(self, sequence_data):
        if not sequence_data:
            return  # Handle empty sequence case

        # Clear the existing sequence
        self.main_widget.sequence_widget.button_frame.clear_sequence()

        # Extract the start position key from the first item
        start_pos_key = sequence_data[0]["start_pos"]

        # Retrieve or create the start position pictograph
        start_position_pictograph = self.get_start_position_pictograph(start_pos_key)

        # Set the start position in the beat frame
        if start_position_pictograph:
            self.main_widget.sequence_widget.beat_frame.set_start_position(
                start_position_pictograph
            )

        # Populate the sequence with the remaining pictographs
        for pictograph_dict in sequence_data:
            self.main_widget.sequence_widget.populate_sequence(pictograph_dict)

    def get_start_position_pictograph(self, start_pos_key):
        # Assuming 'letters' is accessible via main_widget and contains start position definitions
        start_position_definitions = self.main_widget.letters.get(start_pos_key)

        if start_position_definitions:
            # Assuming the definitions contain exactly what's needed to create a pictograph
            start_pos_def = start_position_definitions[
                0
            ]  # Assuming only one definition per start_pos_key
            pictograph_factory = self.main_widget.sequence_widget.pictograph_factory
            pictograph_key = pictograph_factory.generate_pictograph_key_from_dict(
                start_pos_def
            )
            return pictograph_factory.get_or_create_pictograph(
                pictograph_key, start_pos_def
            )

        return None
