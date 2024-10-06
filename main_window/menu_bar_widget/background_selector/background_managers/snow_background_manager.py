import random
from main_window.menu_bar_widget.background_selector.background_managers.background_manager import (
    BackgroundManager,
)
from PyQt6.QtGui import QColor, QPainter, QLinearGradient
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt


class SnowBackgroundManager(BackgroundManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.snowflakes = [
            {
                "x": random.uniform(0, 1),
                "y": random.uniform(0, 1),
                "speed": random.uniform(0.001, 0.005),
                "size": random.uniform(2, 5)
                * (2 if random.random() < 0.02 else 1),  # Occasionally large
                "sway": random.uniform(-0.001, 0.001),
                "opacity": random.uniform(0.6, 1.0),  # Add a flickering effect range
                "twinkle_factor": random.uniform(0.98, 1.02),  # For more subtle twinkle
            }
            for _ in range(200)
        ]
        self.wind = 0.0002  # Gentle wind factor
        self.wind_direction_change = 0.00001  # How quickly wind direction changes

    def animate_background(self):
        for flake in self.snowflakes:
            flake["y"] += flake["speed"]
            flake["x"] += flake["sway"] + self.wind  # Apply gentle wind

            # Add slight twinkle effect to opacity
            flake["opacity"] *= flake["twinkle_factor"]
            if flake["opacity"] > 1.0:
                flake["opacity"] = 1.0
            if flake["opacity"] < 0.6:
                flake["opacity"] = 0.6

            # Reset snowflake if it goes beyond the bottom
            if flake["y"] > 1:
                flake["y"] = 0
                flake["x"] = random.uniform(0, 1)
                flake["speed"] = random.uniform(0.001, 0.005)
                flake["size"] = random.uniform(2, 5) * (
                    2 if random.random() < 0.02 else 1
                )
                flake["sway"] = random.uniform(-0.001, 0.001)
                flake["opacity"] = random.uniform(0.6, 1.0)

            # Wrap around horizontally
            if flake["x"] < 0:
                flake["x"] += 1
            elif flake["x"] > 1:
                flake["x"] -= 1

        # Slowly change wind direction over time
        self.wind += random.uniform(
            -self.wind_direction_change, self.wind_direction_change
        )
        self.wind = max(
            min(self.wind, 0.002), -0.002
        )  # Limit wind strength to a small range

        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw a gradient winter sky (soft blue to dark blue)
        gradient = QLinearGradient(0, 0, 0, widget.height())
        gradient.setColorAt(0, QColor(100, 150, 200))  # Light blue at the top
        gradient.setColorAt(1, QColor(30, 30, 60))  # Dark blue at the bottom
        painter.fillRect(widget.rect(), gradient)

        # Set color and draw snowflakes
        for flake in self.snowflakes:
            x = int(flake["x"] * widget.width())
            y = int(flake["y"] * widget.height())
            size = int(flake["size"])

            painter.setOpacity(flake["opacity"])  # Apply opacity for twinkle effect
            painter.setBrush(QColor(255, 255, 255, int(flake["opacity"] * 255)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(x, y, size, size)

        painter.setOpacity(1.0)  # Reset opacity
