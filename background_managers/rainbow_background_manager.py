import random

from background_managers.background_manager import BackgroundManager
from PyQt6.QtGui import QLinearGradient, QColor, QPainter
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QWidget


class RainbowBackgroundManager(BackgroundManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stars = [
            (random.random(), random.random(), random.random() * 2 + 1)
            for _ in range(100)
        ]

    def animate_background(self):
        """Update the gradient and color shift for the animation."""
        self.gradient_shift += 0.05  # Adjust for speed of the undulation
        self.color_shift += 1  # Adjust for speed of color change
        if self.color_shift > 360:
            self.color_shift = 0
        self.update_required.emit()

    def paint_background(self, widget: "QWidget", painter: "QPainter"):
        """Paint the animated background gradient on a widget."""
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        gradient = QLinearGradient(0, 0, 0, widget.height())
        for i in range(10):  # Number of bands in the gradient
            pos = i / 10
            hue = int((self.color_shift + pos * 100) % 360)
            color = QColor.fromHsv(hue, 255, 255, 150)  # Adjust the alpha for intensity
            adjusted_pos = pos + math.sin(self.gradient_shift + pos * math.pi) * 0.05
            clamped_pos = max(0, min(adjusted_pos, 1))  # Clamp between 0 and 1
            gradient.setColorAt(clamped_pos, color)
        painter.fillRect(widget.rect(), gradient)


