import os
import subprocess
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QLineEdit,
    QFileDialog,
    QMessageBox,
    QLabel,
)
from PyQt6.QtCore import Qt


class MovToMp4Converter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("MOV to MP4 Converter")
        self.setGeometry(300, 300, 500, 200)

        # Main layout
        layout = QVBoxLayout()

        # Input file selection
        self.input_label = QLabel("Select .mov file:")
        self.input_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.input_label)

        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Path to the .mov file")
        layout.addWidget(self.input_field)

        self.input_button = QPushButton("Browse")
        self.input_button.clicked.connect(self.select_input_file)
        layout.addWidget(self.input_button)

        # Output file selection
        self.output_label = QLabel("Save as .mp4 file:")
        self.output_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.output_label)

        self.output_field = QLineEdit()
        self.output_field.setPlaceholderText("Path to save the .mp4 file")
        layout.addWidget(self.output_field)

        self.output_button = QPushButton("Browse")
        self.output_button.clicked.connect(self.select_output_file)
        layout.addWidget(self.output_button)

        # Convert button
        self.convert_button = QPushButton("Convert")
        self.convert_button.clicked.connect(self.convert_mov_to_mp4)
        layout.addWidget(self.convert_button)

        # Central widget setup
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def select_input_file(self):
        """Open file dialog to select a .mov file."""
        input_file, _ = QFileDialog.getOpenFileName(
            self, "Select a .mov file", "", "MOV Files (*.mov)"
        )
        if input_file:
            self.input_field.setText(input_file)

    def select_output_file(self):
        """Open file dialog to save the .mp4 file."""
        output_file, _ = QFileDialog.getSaveFileName(
            self, "Save as", "", "MP4 Files (*.mp4)"
        )
        if output_file:
            self.output_field.setText(output_file)

    def convert_mov_to_mp4(self):
        """Convert the selected .mov file to .mp4."""
        input_file = self.input_field.text()
        output_file = self.output_field.text()

        if not input_file or not output_file:
            QMessageBox.critical(
                self, "Error", "Please select both input and output files."
            )
            return

        if not os.path.exists(input_file):
            QMessageBox.critical(
                self, "Error", f"Input file does not exist: {input_file}"
            )
            return

        try:
            # Build and execute the ffmpeg command
            command = [
                "ffmpeg",
                "-i",
                input_file,  # Input file
                "-c:v",
                "libx264",  # Video codec
                "-preset",
                "medium",  # Compression speed/quality
                "-crf",
                "23",  # Quality level
                "-c:a",
                "aac",  # Audio codec
                "-b:a",
                "192k",  # Audio bitrate
                "-movflags",
                "+faststart",  # Optimize for streaming
                output_file,  # Output file
            ]
            subprocess.run(command, check=True)
            QMessageBox.information(
                self, "Success", f"Conversion completed: {output_file}"
            )
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Error during conversion: {e}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Unexpected error: {e}")


# Run the application
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MovToMp4Converter()
    window.show()
    sys.exit(app.exec())
