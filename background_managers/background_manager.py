from PyQt6.QtCore import QObject, QTimer, pyqtSignal
from PyQt6.QtGui import QLinearGradient, QColor, QPainter
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from PyQt6.QtWidgets import QWidget


class BackgroundManager(QObject):
    update_required = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.gradient_shift = 0
        self.color_shift = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate_background)
        self.timer.start(50)

    def animate_background(self):
        # implement in subclass
        pass


import random
from background_managers.background_manager import BackgroundManager
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QWidget


class StarfieldBackgroundManager(BackgroundManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stars = [
            (random.random(), random.random(), random.random() * 2 + 1)
            for _ in range(100)
        ]

    def animate_background(self):
        self.stars = [(x, y, z - 0.02) for x, y, z in self.stars if z > 0.1]
        if len(self.stars) < 100:
            self.stars.append((random.random(), random.random(), 2))
        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(widget.rect(), QColor(0, 0, 0))
        for x, y, z in self.stars:
            star_color = QColor(255, 255, 255)
            star_size = int((1 - z) * 5)
            xpos = int(x * widget.width())
            ypos = int(y * widget.height())
            painter.setBrush(star_color)
            painter.drawEllipse(xpos, ypos, star_size, star_size)


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


from background_managers.background_manager import BackgroundManager
from PyQt6.QtGui import QLinearGradient, QColor, QPainter

from PyQt6.QtWidgets import QWidget


class AuroraBackgroundManager(BackgroundManager):
    def animate_background(self):
        self.gradient_shift += 0.01
        self.color_shift += 2
        if self.color_shift > 360:
            self.color_shift = 0
        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        gradient = QLinearGradient(0, widget.height(), widget.width(), 0)
        colors = [(255, 0, 255, 100), (0, 255, 255, 100), (255, 255, 0, 100)]
        for i, (r, g, b, a) in enumerate(colors):
            hue = int((self.color_shift + i * 120) % 360)
            color = QColor.fromHsv(hue, 255, 255, a)
            gradient.setColorAt(i / len(colors), color)
        painter.fillRect(widget.rect(), gradient)


import math
import random
from background_managers.background_manager import BackgroundManager
from PyQt6.QtGui import QLinearGradient, QColor, QPainter

from PyQt6.QtWidgets import QWidget


class AuroraBorealisBackgroundManager(BackgroundManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.light_waves = [random.random() * 2 * math.pi for _ in range(10)]

    def animate_background(self):
        # Update light waves positions
        self.light_waves = [x + 0.01 for x in self.light_waves]
        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        gradient = QLinearGradient(0, 0, widget.width(), widget.height())
        colors = [(0, 25, 50, 100), (0, 50, 100, 50), (0, 100, 150, 25)]
        for i, wave in enumerate(self.light_waves):
            pos = (math.sin(wave) + 1) / 2
            color = QColor(*colors[i % len(colors)])
            gradient.setColorAt(pos, color)
        painter.fillRect(widget.rect(), gradient)


import math
import random
from background_managers.background_manager import BackgroundManager
from PyQt6.QtGui import QLinearGradient, QColor, QPainter

from PyQt6.QtWidgets import QWidget


# Example using PyQt and a particle system with attraction points
class AttractionParticlesBackgroundManager(BackgroundManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.particles = [
            {"x": random.random(), "y": random.random(), "dx": 0, "dy": 0}
            for _ in range(100)
        ]
        self.attraction_points = [{"x": 0.5, "y": 0.5}]  # Center point attraction

    def animate_background(self):
        for p in self.particles:
            for a in self.attraction_points:
                distance_x = a["x"] - p["x"]
                distance_y = a["y"] - p["y"]
                distance = math.sqrt(distance_x**2 + distance_y**2)
                force_direction_x = distance_x / distance
                force_direction_y = distance_y / distance
                # Update particle velocity based on the attraction point
                p["dx"] += force_direction_x * 0.05
                p["dy"] += force_direction_y * 0.05
            # Update particle position
            p["x"] += p["dx"]
            p["y"] += p["dy"]
            # Implement damping to slow down particles
            p["dx"] *= 0.95
            p["dy"] *= 0.95
        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(widget.rect(), QColor(0, 0, 20))  # Dark blue background
        for p in self.particles:
            painter.setBrush(QColor(255, 255, 255))
            painter.drawEllipse(
                int(p["x"] * widget.width()), int(p["y"] * widget.height()), 5, 5
            )


# This would require integrating a water ripple simulation algorithm
import math
import random
from background_managers.background_manager import BackgroundManager
from PyQt6.QtGui import QLinearGradient, QColor, QPainter

from PyQt6.QtWidgets import QWidget


class WaterRipplesBackgroundManager(BackgroundManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.water_height = [
            [0 for _ in range(100)] for _ in range(100)
        ]  # Simplified grid-based approach

    def animate_background(self):
        # Implement water ripple physics here
        new_height = [[0 for _ in range(100)] for _ in range(100)]
        for y in range(1, 99):
            for x in range(1, 99):
                new_height[y][x] = (
                    (
                        self.water_height[y - 1][x]
                        + self.water_height[y + 1][x]
                        + self.water_height[y][x - 1]
                        + self.water_height[y][x + 1]
                    )
                    / 2
                ) - new_height[y][x]
                new_height[y][x] *= 0.99  # Damping
        self.water_height = new_height
        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        color = QColor(0, 75, 150, 100)  # Light blue with some transparency
        for y in range(100):
            for x in range(100):
                intensity = int(self.water_height[y][x] * 255)
                painter.setBrush(QColor(0, 75 + intensity, 150 + intensity))
                painter.drawRect(
                    x * widget.width() // 100,
                    y * widget.height() // 100,
                    widget.width() // 100,
                    widget.height() // 100,
                )
