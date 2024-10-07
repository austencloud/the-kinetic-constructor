import random
import math
from main_window.menu_bar_widget.background_selector.background_managers.background_manager import (
    BackgroundManager,
)
from PyQt6.QtGui import QColor, QPainter, QLinearGradient, QPainterPath
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
                * (2 if random.random() < 0.2 else 1),  # More frequent special flakes
                "sway": random.uniform(-0.001, 0.001),
                "opacity": random.uniform(0.6, 1.0),
                "twinkle_factor": random.uniform(0.98, 1.02),
                "is_special": random.random()
                < 0.7,  # Increased chance for special flakes
                "snowflake_type": random.choice(
                    [1, 2, 3]
                ),  # Different snowflake shapes
            }
            for _ in range(200)
        ]
        self.wind = 0.0002
        self.wind_direction_change = 0.00001

    def animate_background(self):
        for flake in self.snowflakes:
            flake["y"] += flake["speed"]
            flake["x"] += flake["sway"] + self.wind

            # Add twinkle effect
            flake["opacity"] *= flake["twinkle_factor"]
            if flake["opacity"] > 1.0:
                flake["opacity"] = 1.0
            if flake["opacity"] < 0.6:
                flake["opacity"] = 0.6

            # Reset snowflake
            if flake["y"] > 1:
                flake["y"] = 0
                flake["x"] = random.uniform(0, 1)
                flake["speed"] = random.uniform(0.001, 0.005)
                flake["size"] = random.uniform(2, 5) * (
                    2 if random.random() < 0.2 else 1
                )
                flake["sway"] = random.uniform(-0.001, 0.001)
                flake["opacity"] = random.uniform(0.6, 1.0)
                flake["is_special"] = random.random() < 0.5
                flake["snowflake_type"] = random.choice(
                    [1, 2, 3]
                )  # Random snowflake shape

            # Wrap around horizontally
            if flake["x"] < 0:
                flake["x"] += 1
            elif flake["x"] > 1:
                flake["x"] -= 1

        self.wind += random.uniform(
            -self.wind_direction_change, self.wind_direction_change
        )
        self.wind = max(min(self.wind, 0.002), -0.002)

        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Gradient sky background
        gradient = QLinearGradient(0, 0, 0, widget.height())
        gradient.setColorAt(0, QColor(100, 150, 200))
        gradient.setColorAt(1, QColor(30, 30, 60))
        painter.fillRect(widget.rect(), gradient)

        # Draw snowflakes
        for flake in self.snowflakes:
            x = int(flake["x"] * widget.width())
            y = int(flake["y"] * widget.height())
            size = int(flake["size"])

            painter.setOpacity(flake["opacity"])
            painter.setBrush(QColor(255, 255, 255, int(flake["opacity"] * 255)))
            painter.setPen(Qt.PenStyle.NoPen)

            if flake["is_special"]:
                # Draw a special snowflake shape based on type
                if flake["snowflake_type"] == 1:
                    self.draw_star_snowflake(painter, x, y, size)
                elif flake["snowflake_type"] == 2:
                    self.draw_spiky_snowflake(painter, x, y, size)
                elif flake["snowflake_type"] == 3:
                    self.draw_spiky_snowflake_variant(painter, x, y, size)
            else:
                painter.drawEllipse(x, y, size, size)

        painter.setOpacity(1.0)

    def draw_star_snowflake(self, painter, x, y, size):
        """Draw a star-like snowflake for special snowflakes."""
        path = QPainterPath()
        radius = size / 2
        angle_step = math.pi / 3  # 60 degrees for 6 points

        # Create a star shape with lines radiating from the center
        for i in range(6):
            angle = i * angle_step
            x1 = x + radius * math.cos(angle)
            y1 = y + radius * math.sin(angle)
            path.moveTo(x, y)  # Start from the center
            path.lineTo(x1, y1)

        painter.setPen(QColor(255, 255, 255))  # Draw the star shape with a solid line
        painter.drawPath(path)

    def draw_spiky_snowflake(self, painter, x, y, size):
        """Draw a spiky snowflake with additional detail."""
        path = QPainterPath()
        radius = size / 2
        small_radius = radius * 0.6  # Smaller spikes between the larger ones
        angle_step = math.pi / 6  # 30 degrees for detailed spikes

        # Create a spiky snowflake with alternating long and short arms
        for i in range(12):
            angle = i * angle_step
            r = radius if i % 2 == 0 else small_radius
            x1 = x + r * math.cos(angle)
            y1 = y + r * math.sin(angle)
            if i == 0:
                path.moveTo(x1, y1)
            else:
                path.lineTo(x1, y1)
        path.closeSubpath()  # Complete the spiky snowflake

        painter.setPen(
            QColor(255, 255, 255)
        )  # Draw the spiky snowflake with a solid line
        painter.drawPath(path)

    def draw_spiky_snowflake_variant(self, painter, x, y, size):
        """Draw a variant spiky snowflake with a different number of spikes."""
        path = QPainterPath()
        num_points = random.randint(5, 8)  # Random number of spikes (5 to 8)
        radius = size / 2
        small_radius = radius * 0.6  # Smaller spikes between the larger ones
        angle_step = (
            2 * math.pi / (num_points * 2)
        )  # Adjust angle step based on number of points

        # Create a variant spiky snowflake with alternating long and short arms
        for i in range(num_points * 2):
            angle = i * angle_step
            r = radius if i % 2 == 0 else small_radius
            x1 = x + r * math.cos(angle)
            y1 = y + r * math.sin(angle)
            if i == 0:
                path.moveTo(x1, y1)
            else:
                path.lineTo(x1, y1)
        path.closeSubpath()  # Complete the spiky snowflake

        painter.setPen(QColor(255, 255, 255))  # Draw the variant spiky snowflake
        painter.drawPath(path)
