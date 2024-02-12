import json
import os
from PyQt6.QtWidgets import QTreeView, QVBoxLayout, QWidget, QMessageBox
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import QDir, QModelIndex
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


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
        # Assuming self.main_widget points to MainWidget
        # Clear the existing sequence
        self.main_widget.sequence_widget.button_frame.clear_sequence()
        # Populate the sequence
        for pictograph_dict in sequence_data:
            self.main_widget.sequence_widget.populate_sequence(pictograph_dict)
        # Trigger any necessary updates or refreshes here
