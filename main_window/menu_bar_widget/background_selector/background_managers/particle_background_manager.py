import random
import math

from main_window.menu_bar_widget.background_selector.background_managers.background_manager import (
    BackgroundManager,
)
from PyQt6.QtGui import QColor, QPainter, QPen
from PyQt6.QtCore import QPointF
from PyQt6.QtWidgets import QWidget


class ParticleBackgroundManager(BackgroundManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.particles = [
            {
                "x": random.random(),
                "y": random.random(),
                "dx": (random.random() - 0.5) * 2,  # Faster movement
                "dy": (random.random() - 0.5) * 2,
                "size": random.randint(5, 12),  # Random particle size (larger range)
                "color": QColor(
                    random.randint(100, 255),  # More vivid colors
                    random.randint(100, 255),
                    random.randint(150, 255),
                    random.randint(150, 230),  # Reduced transparency (150-230 range)
                ),
            }
            for _ in range(80)  # Slightly fewer particles for better performance
        ]
        self.mouse_pos = QPointF(0.5, 0.5)  # Default mouse position at center

    def animate_background(self):
        # Update particle positions
        for p in self.particles:
            p["x"] += p["dx"] * 0.01
            p["y"] += p["dy"] * 0.01

            # Gravity towards the center (or mouse position)
            attraction_strength = 0.0005
            direction_to_center = QPointF(
                self.mouse_pos.x() - p["x"], self.mouse_pos.y() - p["y"]
            )
            distance = math.sqrt(
                direction_to_center.x() ** 2 + direction_to_center.y() ** 2
            )
            if distance > 0.05:  # Only attract when far enough
                p["dx"] += direction_to_center.x() * attraction_strength
                p["dy"] += direction_to_center.y() * attraction_strength

            # Boundary reflection
            if p["x"] < 0 or p["x"] > 1:
                p["dx"] *= -1
            if p["y"] < 0 or p["y"] > 1:
                p["dy"] *= -1

        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(
            widget.rect(), QColor(10, 10, 30)
        )  # Dark background with bluish hue

        # Draw particles
        for p in self.particles:
            particle_color = p["color"]
            painter.setBrush(particle_color)
            x = int(p["x"] * widget.width())
            y = int(p["y"] * widget.height())
            size = p["size"]
            painter.drawEllipse(x, y, size, size)

        # Draw trails with a gradient effect
        for p in self.particles:
            trail_color = QColor(
                p["color"].red(), p["color"].green(), p["color"].blue(), 80
            )
            pen = QPen(trail_color)  # Slightly transparent trail color
            pen.setWidth(2)
            painter.setPen(pen)
            trail_length = 20  # Longer trails
            painter.drawLine(
                x, y, x - int(p["dx"] * trail_length), y - int(p["dy"] * trail_length)
            )

    def set_mouse_position(self, pos: QPointF):
        """Set the mouse position for interaction effects."""
        self.mouse_pos = QPointF(pos.x(), pos.y())
