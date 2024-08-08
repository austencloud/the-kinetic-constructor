from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPainter, QPen, QFont
from PyQt6.QtCore import Qt, QRectF

class DifficultyLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.difficulty_level = 1
        self.setFixedSize(60, 60)  # Adjust the size to ensure the circle is fully visible
        self.setToolTip("Difficulty Level")  # Add tooltip here

    def set_difficulty_level(self, level: int):
        self.difficulty_level = level
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Inset the circle drawing to ensure it is not cut off
        inset = 5
        rect = self.rect().adjusted(inset, inset, -inset, -inset)

        # Draw the circle
        pen = QPen(Qt.GlobalColor.black, 2)
        painter.setPen(pen)
        painter.setBrush(Qt.GlobalColor.white)
        painter.drawEllipse(rect)

        # Draw the difficulty level number
        font = QFont("Arial", 16, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, str(self.difficulty_level))

        painter.end()
