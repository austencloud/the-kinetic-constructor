from typing import TYPE_CHECKING
from PyQt6.QtGui import QPainter, QPen, QFont, QImage
from PyQt6.QtCore import QRect, Qt
if TYPE_CHECKING:
    from widgets.sequence_widget.SW_beat_frame.image_creator import ImageCreator


class DifficultyLevelDrawer:
    def __init__(self, image_creator: "ImageCreator"):
        self.image_creator = image_creator

    def draw_difficulty_level(self, image: QImage, difficulty_level: int) -> None:
        """Draw the difficulty level on the top left corner of the image."""
        painter = QPainter(image)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Define the size and position for the difficulty level circle
        circle_size = 50
        inset = 10
        rect = QRect(inset, inset, circle_size, circle_size)

        # Draw the circle
        pen = QPen(Qt.GlobalColor.black, 2)
        painter.setPen(pen)
        painter.setBrush(Qt.GlobalColor.white)
        painter.drawEllipse(rect)

        # Draw the difficulty level number
        font = QFont("Arial", 16, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(difficulty_level))

        painter.end()
