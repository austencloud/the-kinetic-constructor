from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPainter, QLinearGradient, QColor
import math


class TopLevelBuilderWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.gradient_shift = 0
        self.color_shift = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_background)
        self.timer.start(100)  # Adjust as needed for smoother or faster animation

    def animate_background(self):
        """Update the gradient and color shift for the animation."""
        self.gradient_shift += 0.05  # Adjust for speed of the undulation
        self.color_shift += 1  # Adjust for speed of color change
        if self.color_shift > 360:
            self.color_shift = 0
        self.update()  # Trigger a repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())
        for i in range(10):  # Number of bands in the gradient
            pos = i / 10
            hue = int((self.color_shift + pos * 100) % 360)
            color = QColor.fromHsv(hue, 255, 255, 150)  # Adjust the alpha for intensity
            # Calculate undulation effect and clamp values to the 0-1 range
            adjusted_pos = pos + math.sin(self.gradient_shift + pos * math.pi) * 0.05
            clamped_pos = max(0, min(adjusted_pos, 1))  # Clamp between 0 and 1
            gradient.setColorAt(clamped_pos, color)

        painter.fillRect(self.rect(), gradient)
