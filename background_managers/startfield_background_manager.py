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
