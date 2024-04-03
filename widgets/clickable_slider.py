from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QSlider
from PyQt6.QtGui import QMouseEvent


class ClickableSlider(QSlider):
    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            val = (
                self.minimum()
                + ((self.maximum() - self.minimum()) * event.position().x())
                / self.width()
            )
            val = round(val)
            self.setValue(val)
            event.accept()
        super().mousePressEvent(event)