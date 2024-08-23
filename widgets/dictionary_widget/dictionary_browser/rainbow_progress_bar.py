from PyQt6.QtWidgets import QProgressBar, QVBoxLayout, QLabel, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor

class RainbowProgressBar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setTextVisible(False)  # Hide the text on the bar itself

        # Create the label for percentage text
        self.percentage_label = QLabel("0%", self)
        self.percentage_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.percentage_label.setStyleSheet("font-size: 14px; color: #000000;")

        # Layout to position the progress bar and percentage label
        layout = QVBoxLayout(self)
        layout.addWidget(self.percentage_label)
        # add a spacer
        layout.addStretch(1)
        layout.addWidget(self.progress_bar)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        self.setLayout(layout)

        # Set the rainbow gradient style
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #4CAF50;
                border-radius: 5px;
                background-color: #E0E0E0;
            }
            QProgressBar::chunk {
                border-radius: 5px;
                background: qlineargradient(
                    spread:pad, 
                    x1:0, y1:0, x2:1, y2:0, 
                    stop:0 red, 
                    stop:0.16 orange, 
                    stop:0.33 yellow, 
                    stop:0.49 green, 
                    stop:0.66 blue, 
                    stop:0.82 indigo, 
                    stop:1 violet
                );
            }
        """)

    def setValue(self, value):
        """ Update the progress bar value and the percentage label """
        self.progress_bar.setValue(value)
        self.percentage_label.setText(f"{value}%")

