import random

from background_managers.background_manager import BackgroundManager
from PyQt6.QtGui import QColor, QPainter

from PyQt6.QtWidgets import QWidget


class ParticleBackgroundManager(BackgroundManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.particles = [
            {
                "x": random.random(),
                "y": random.random(),
                "dx": random.random() - 0.5,
                "dy": random.random() - 0.5,
            }
            for _ in range(80)
        ]

    def animate_background(self):
        # Update particle positions
        for p in self.particles:
            p["x"] += p["dx"] * 0.01
            p["y"] += p["dy"] * 0.01
            # Boundary reflection
            if p["x"] < 0 or p["x"] > 1:
                p["dx"] *= -1
            if p["y"] < 0 or p["y"] > 1:
                p["dy"] *= -1
        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(widget.rect(), QColor(20, 20, 20))  # Dark background
        for p in self.particles:
            particle_color = QColor(180, 180, 255, 150)
            painter.setBrush(particle_color)
            x = int(p["x"] * widget.width())
            y = int(p["y"] * widget.height())
            painter.drawEllipse(x, y, 10, 10)


