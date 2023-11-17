import json
import os
import sys
from typing import List

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

# Print the current working directory
print("Current working directory:", os.getcwd())

BLUE = "blue"
RED = "red"
NORTH = "n"
SOUTH = "s"
EAST = "e"
WEST = "w"

positions_map = {
    (NORTH, RED, SOUTH, BLUE): "alpha1",
    (EAST, RED, WEST, BLUE): "alpha2",
    (SOUTH, RED, NORTH, BLUE): "alpha3",
    (WEST, RED, EAST, BLUE): "alpha4",
    (NORTH, RED, NORTH, BLUE): "beta1",
    (EAST, RED, EAST, BLUE): "beta2",
    (SOUTH, RED, SOUTH, BLUE): "beta3",
    (WEST, RED, WEST, BLUE): "beta4",
    (NORTH, RED, WEST, BLUE): "gamma1",
    (EAST, RED, NORTH, BLUE): "gamma2",
    (SOUTH, RED, EAST, BLUE): "gamma3",
    (WEST, RED, SOUTH, BLUE): "gamma4",
    (NORTH, RED, EAST, BLUE): "gamma5",
    (EAST, RED, SOUTH, BLUE): "gamma6",
    (SOUTH, RED, WEST, BLUE): "gamma7",
    (WEST, RED, NORTH, BLUE): "gamma8",
}


def validate_and_correct_json_file(file_path) -> List[str]:
    with open(file_path, "r") as file:
        data = json.load(file)

    key = next(iter(data))
    errors = []
    corrected = False

    for sequence in data[key]:
        # Filter out items that don't have the 'color' key
        items_with_color = [item for item in sequence[1:] if "color" in item]
        
        color_start = {item["color"]: item["start_location"] for item in items_with_color}
        color_end = {item["color"]: item["end_location"] for item in items_with_color}

        start_key = (color_start.get(RED, ""), RED, color_start.get(BLUE, ""), BLUE)
        end_key = (color_end.get(RED, ""), RED, color_end.get(BLUE, ""), BLUE)

        correct_start = positions_map.get(start_key)
        correct_end = positions_map.get(end_key)

        if sequence[0]["start_position"] != correct_start:
            errors.append(f"Correcting start position in {file_path}: {sequence[0]['start_position']} to {correct_start}")
            sequence[0]["start_position"] = correct_start
            corrected = True

        if sequence[0]["end_position"] != correct_end:
            errors.append(f"Correcting end position in {file_path}: {sequence[0]['end_position']} to {correct_end}")
            sequence[0]["end_position"] = correct_end
            corrected = True

    if corrected:
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    return errors

# Function to recursively gather all JSON files from a directory
def get_all_json_files(directory):
    json_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                json_files.append(os.path.join(root, file))
    return json_files


class FileValidator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("JSON File Validator")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.label = QLabel("Select JSON files to validate")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)

        self.textEdit = QTextEdit()
        self.textEdit.setReadOnly(True)
        layout.addWidget(self.textEdit)

        self.btnSelect = QPushButton("Select Files", self)
        self.btnSelect.clicked.connect(self.openFileDialog)
        layout.addWidget(self.btnSelect)

        self.btnValidate = QPushButton("Validate Files", self)
        self.btnValidate.clicked.connect(self.validateFiles)
        layout.addWidget(self.btnValidate)

        centralWidget = QWidget()
        centralWidget.setLayout(layout)
        self.setCentralWidget(centralWidget)

    def openFileDialog(self):
        # Set the default directory to "resources/json"
        default_directory = os.path.join(os.getcwd(), "resources", "json")

        # Select a directory instead of individual files
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory", default_directory
        )

        if directory:
            self.selectedFiles = get_all_json_files(directory)
            self.textEdit.append("Selected Directory: " + directory)
            self.textEdit.append("Files to be validated:\n" + "\n".join(self.selectedFiles))

    def validateFiles(self):
        if not hasattr(self, "selectedFiles"):
            self.textEdit.append("No files selected for validation.")
            return

        for file_path in self.selectedFiles:
            errors = validate_and_correct_json_file(file_path)
            if errors:
                for error in errors:
                    self.textEdit.append(error)
            else:
                self.textEdit.append(f"No errors found in {file_path}.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = FileValidator()
    ex.show()
    sys.exit(app.exec())
