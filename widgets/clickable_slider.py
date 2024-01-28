from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QSlider
from PyQt6.QtGui import QMouseEvent


class ClickableSlider(QSlider):
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            # Calculate the value based on the mouse position
            val = (
                self.minimum()
                + ((self.maximum() - self.minimum()) * event.position().x())
                / self.width()
            )
            val = round(val)  # Round to the nearest integer
            self.setValue(val)
            event.accept()
        super().mousePressEvent(event)  # Call the parent method to handle dragging