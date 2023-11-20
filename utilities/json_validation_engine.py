import json
import os
import sys
from typing import List, Dict
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox
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

# Global definitions
NORTH, SOUTH, EAST, WEST, BLUE, RED = "n", "s", "e", "w", "blue", "red"
valid_colors = {RED, BLUE}
valid_motion_types = {"pro", "anti", "dash", "static", "float", "chu"}
valid_quadrants = {"ne", "se", "sw", "nw", None}
valid_rotation_directions = {"cw", "ccw", None}
valid_locations = {"n", "e", "s", "w"}
valid_turns = {0, 0.5, 1, 1.5, 2, 2.5}

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

class JsonValidationEngine(QMainWindow):
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

        self.selectedFilesText = QTextEdit()
        self.selectedFilesText.setReadOnly(True)
        self.selectedFilesText.setPlaceholderText(
            "Selected directories will be displayed here."
        )
        layout.addWidget(self.selectedFilesText)

        self.errorsText = QTextEdit()
        self.errorsText.setReadOnly(True)
        self.errorsText.setPlaceholderText("Validation errors will be displayed here.")
        layout.addWidget(self.errorsText)

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
        default_directory = os.path.join(os.getcwd(), "resources", "json")
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory", default_directory
        )
        if directory:
            self.selectedFiles = self.get_all_json_files(directory)
            self.selectedFilesText.clear()
            self.selectedFilesText.append("Selected Directory: " + directory)
            self.selectedFilesText.append(
                "Files to be validated:\n" + "\n".join(self.selectedFiles)
            )

    def user_wants_corrections(self) -> bool:
        msgBox = QMessageBox()
        msgBox.setWindowTitle("Confirm Corrections")
        msgBox.setText("Errors found in the JSON file. Do you want to apply automatic corrections?")
        msgBox.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        msgBox.setDefaultButton(QMessageBox.StandardButton.Yes)
        response = msgBox.exec()
        return response == QMessageBox.StandardButton.Yes

    def validateFiles(self):
        if not hasattr(self, "selectedFiles"):
            self.errorsText.append("No files selected for validation.")
            return

        self.errorsText.clear()
        total_errors = {}
        for file_path in self.selectedFiles:
            errors = self.validate_and_correct_json_file(file_path)
            if errors:
                for error in errors:
                    attribute = error.split(":")[0].split()[-1]
                    total_errors.setdefault(attribute, []).append(error)
        
        if total_errors:
            self.display_errors_summary(total_errors)
            if self.user_wants_corrections():
                self.apply_corrections_to_all_files()
                self.errorsText.append("All errors have been corrected.")
        else:
            self.errorsText.append("No errors found in selected files.")


    def display_errors_summary(self, total_errors):
        summary = "\nError Summary:\n"
        for attribute, errors in total_errors.items():
            summary += f"{attribute}: {len(errors)} errors found\n"
            for error in errors:
                summary += f"  - {error}\n"
        self.errorsText.append(summary)

    def apply_corrections_to_all_files(self):
        for file_path in self.selectedFiles:
            _, corrections = self.validate_and_correct_json_file(file_path, True)
            if corrections:
                self.errorsText.append(f"Corrections applied to {file_path}:\n")
                for correction in corrections:
                    self.errorsText.append(f"  - {correction}")


    # Helper functions
    def is_none_allowed_for_quadrant(self, motion_type: str) -> bool:
        return motion_type in {"static", "dash"}

    def is_none_allowed_for_rotation_direction(self, motion_type: str, turns: str) -> bool:
        return (motion_type in {"static", "dash"} and turns == 0) or (motion_type in {"pro", "anti"} and turns == "fl")

    def validate_entry_types(self, entry: Dict, letter: str, position: str) -> List[str]:
        errors = []
        # Validate each attribute
        if entry.get("color") not in valid_colors:
            errors.append(f"{letter} {position}: Invalid color '{entry.get('color')}'")
        if entry.get("motion_type") not in valid_motion_types:
            errors.append(f"{letter} {position}: Invalid motion type '{entry.get('motion_type')}'")
        if entry.get("start_location") not in valid_locations:
            errors.append(f"{letter} {position}: Invalid start location '{entry.get('start_location')}'")
        if entry.get("end_location") not in valid_locations:
            errors.append(f"{letter} {position}: Invalid end location '{entry.get('end_location')}'")
        if entry.get("turns") not in valid_turns:
            errors.append(f"{letter} {position}: Invalid turns '{entry.get('turns')}'")

        # Special validation for quadrant and rotation direction
        if not self.is_none_allowed_for_quadrant(entry.get("motion_type")) and entry.get("quadrant") is None:
            errors.append(f"{letter} {position}: Invalid quadrant '{entry.get('quadrant')}'")
        if not self.is_none_allowed_for_rotation_direction(entry.get("motion_type"), str(entry.get("turns"))) and entry.get("rotation_direction") is None:
            errors.append(f"{letter} {position}: Invalid rotation direction '{entry.get('rotation_direction')}'")

        return errors

    # Main validation function
    def validate_and_correct_json_file(self, file_path: str) -> List[str]:
        with open(file_path, "r") as file:
            data = json.load(file)

        key = next(iter(data))
        all_errors = []
        all_corrections = []

        for sequence in data[key]:
            formatted_position = f"{sequence[0]['start_position']}→{sequence[0]['end_position']}".replace("alpha", "α").replace("beta", "β").replace("gamma", "Γ")
            if self.user_wants_corrections():
                for item in sequence[1:]:
                    if "color" in item:
                        corrections = self.apply_corrections(item)
                        all_corrections.extend(corrections)
                        
        # Save data if corrections were made
        if all_corrections:
            with open(file_path, "w") as file:
                json.dump(data, file, indent=4)

        return all_errors, all_corrections
    
    def get_all_json_files(self, directory: str):
        json_files = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(".json"):
                    json_files.append(os.path.join(root, file))
        return json_files


    def apply_corrections(self, entry: Dict) -> List[str]:
        corrections = []
        if entry.get("motion_type") in {"static", "dash"}:
            if entry.get("quadrant") is not None:
                corrections.append("Quadrant set to None for static or dash motion type.")
                entry["quadrant"] = None
        elif "start_location" in entry and "end_location" in entry:
            inferred_quadrant = self.infer_quadrant(entry["start_location"], entry["end_location"])
            if entry.get("quadrant") != inferred_quadrant:
                corrections.append(f"Quadrant corrected to {inferred_quadrant}.")
                entry["quadrant"] = inferred_quadrant
        # Add more correction rules as needed
        return corrections

    def infer_quadrant(self, start: str, end: str) -> str:
        if start == "n":
            return "ne" if end == "e" else "nw"
        elif start == "e":
            return "se" if end == "s" else "ne"
        elif start == "s":
            return "sw" if end == "w" else "se"
        elif start == "w":
            return "nw" if end == "n" else "sw"
        return None
                
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = JsonValidationEngine()
    ex.show()
    sys.exit(app.exec())
