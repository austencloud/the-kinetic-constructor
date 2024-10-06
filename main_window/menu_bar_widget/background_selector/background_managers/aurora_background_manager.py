from main_window.menu_bar_widget.background_selector.background_managers.background_manager import (
    BackgroundManager,
)
from PyQt6.QtGui import QLinearGradient, QColor, QPainter, QPainterPath
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
import math
import random


class AuroraBackgroundManager(BackgroundManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.gradient_shift = 0
        self.color_shift = 0
        self.darkness_factor = 0.8  # Make the colors slightly darker
        self.sparkles = self.create_sparkles()  # Sparkling stars or particles
        self.wave_phase = 0  # Phase of sine wave for wavy gradient effect

    def animate_background(self):
        self.gradient_shift += 0.01
        self.color_shift += 2
        self.wave_phase += 0.02  # Gradually move the wave phase
        if self.color_shift > 360:
            self.color_shift = 0

        # Animate sparkles
        for sparkle in self.sparkles:
            sparkle["opacity"] += sparkle["pulse_speed"]
            if sparkle["opacity"] > 1.0 or sparkle["opacity"] < 0.5:
                sparkle["pulse_speed"] *= -1  # Reverse the pulse direction

        self.update_required.emit()

    def create_sparkles(self):
        """Creates random sparkles for the background."""
        return [
            {
                "x": random.uniform(0, 1),
                "y": random.uniform(0, 1),
                "size": random.uniform(2, 4),
                "opacity": random.uniform(0.5, 1.0),
                "pulse_speed": random.uniform(0.01, 0.03),
            }
            for _ in range(50)
        ]

    def paint_background(self, widget: QWidget, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw a wavy gradient background
        gradient = QLinearGradient(0, widget.height(), widget.width(), 0)

        # Add a sine wave effect to the gradient position
        colors = [(255, 0, 255, 100), (0, 255, 255, 100), (255, 255, 0, 100)]
        for i, (r, g, b, a) in enumerate(colors):
            hue = int((self.color_shift + i * 120) % 360)
            color = QColor.fromHsv(hue, 255, int(255), a)

            # Apply sine wave to adjust gradient positioning
            wave_shift = 0.1 * math.sin(self.wave_phase + i * 2 * math.pi / len(colors))
            gradient.setColorAt(min(max(i / len(colors) + wave_shift, 0), 1), color)

        painter.fillRect(widget.rect(), gradient)

        # Draw transparent moving blobs (light streaks effect)
        # self.draw_blobs(widget, painter)

        # Draw sparkling particles
        self.draw_sparkles(widget, painter)

    def draw_blobs(self, widget, painter):
        """Draws semi-transparent blobs to create a light streaks effect."""
        for i in range(3):  # Create 3 blobs
            blob_path = QPainterPath()
            blob_x = random.uniform(0.1, 0.9) * widget.width()
            blob_y = random.uniform(0.1, 0.9) * widget.height()
            blob_size = random.uniform(100, 200)
            blob_path.addEllipse(blob_x, blob_y, blob_size, blob_size)

            painter.setBrush(QColor(255, 255, 255, 50))  # Light, transparent blob
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawPath(blob_path)

    def draw_sparkles(self, widget, painter):
        """Draws small glowing particles for a subtle sparkle effect."""
        for sparkle in self.sparkles:
            x = int(sparkle["x"] * widget.width())
            y = int(sparkle["y"] * widget.height())
            size = int(sparkle["size"])
            opacity = int(sparkle["opacity"] * 255)

            painter.setOpacity(sparkle["opacity"])
            painter.setBrush(QColor(255, 255, 255, opacity))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(x, y, size, size)

        painter.setOpacity(1.0)  # Reset opacity
