import random
from main_window.menu_bar_widget.background_selector.background_managers.background_manager import (
    BackgroundManager,
)

from PyQt6.QtGui import QColor, QPainter, QLinearGradient, QRadialGradient, QPainterPath
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QPointF


class BubblesBackgroundManager(BackgroundManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Create bubbles floating upward with additional reflection properties
        self.bubbles = [
            {
                "x": random.uniform(0, 1),
                "y": random.uniform(0, 1),
                "size": random.uniform(5, 15),
                "speed": random.uniform(0.0005, 0.002),
                "opacity": random.uniform(0.4, 0.8),
                "highlight_factor": random.uniform(0.7, 1.0),  # Highlight brightness
            }
            for _ in range(100)
        ]

    def animate_background(self):
        # Move the bubbles upwards
        for bubble in self.bubbles:
            bubble["y"] -= bubble["speed"]
            if bubble["y"] < 0:
                bubble["y"] = 1  # Reset bubble position to the bottom
                bubble["x"] = random.uniform(0, 1)
                bubble["size"] = random.uniform(5, 15)
                bubble["highlight_factor"] = random.uniform(0.7, 1.0)  # Reset highlight
        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create an underwater gradient (light blue at top, deep blue at bottom)
        gradient = QLinearGradient(0, 0, 0, widget.height())
        gradient.setColorAt(0, QColor(100, 150, 255))  # Light blue
        gradient.setColorAt(1, QColor(0, 30, 90))  # Deep blue
        painter.fillRect(widget.rect(), gradient)

        # Draw bubbles
        for bubble in self.bubbles:
            x = int(bubble["x"] * widget.width())
            y = int(bubble["y"] * widget.height())
            size = int(bubble["size"])

            # Set bubble opacity and fill
            painter.setOpacity(bubble["opacity"])
            painter.setBrush(QColor(255, 255, 255, int(bubble["opacity"] * 255)))
            painter.setPen(Qt.PenStyle.NoPen)

            # Draw the main bubble
            painter.drawEllipse(x, y, size, size)

            # Add a reflection highlight to the bubble for realism
            self.draw_bubble_reflection(
                painter,
                QPointF(x + size / 4, y + size / 4),
                size,
                bubble["highlight_factor"],
            )

        painter.setOpacity(1.0)  # Reset opacity after drawing

    def draw_bubble_reflection(
        self, painter: QPainter, center: QPointF, size: int, highlight_factor: float
    ):
        """Draws a reflection highlight on the top of the bubble to simulate lighting."""
        # Create a small, soft radial gradient for the highlight (reflection effect)
        highlight_radius = size * 0.4 * highlight_factor
        gradient = QRadialGradient(center, highlight_radius)
        gradient.setColorAt(0, QColor(255, 255, 255, 180))  # Bright reflection
        gradient.setColorAt(1, QColor(255, 255, 255, 0))  # Soft fade out

        painter.setBrush(gradient)
        painter.drawEllipse(center, highlight_radius, highlight_radius)

    def draw_underwater_ripples(self, widget: QWidget, painter: QPainter):
        """Optional: Simulates subtle ripples of light on the underwater background."""
        ripple_color = QColor(255, 255, 255, 30)  # Faint light ripples
        painter.setPen(ripple_color)
        ripple_step = 20
        for y in range(0, widget.height(), ripple_step):
            painter.drawLine(0, y, widget.width(), y)
