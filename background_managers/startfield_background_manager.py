import random
from background_managers.background_manager import BackgroundManager
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QWidget


class StarfieldBackgroundManager(BackgroundManager):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.stars = [
            (
                random.random(),
                random.random(),
                random.random() * 2 + 1,
                random.choice([QColor(255, 255, 255), QColor(255, 255, 0)]),
            )
            for _ in range(100)
        ]
        self.twinkle_state = [random.random() for _ in range(100)]

    def animate_background(self):
        self.stars = [
            (x, y, z - 0.02, color) for x, y, z, color in self.stars if z > 0.1
        ]
        if len(self.stars) < 100:
            self.stars.append(
                (
                    random.random(),
                    random.random(),
                    2,
                    random.choice([QColor(255, 255, 255), QColor(255, 255, 0)]),
                )
            )
        self.twinkle_state = [random.random() for _ in range(len(self.stars))]
        self.update_required.emit()

    def paint_background(self, widget: QWidget, painter: QPainter):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(widget.rect(), QColor(0, 0, 0))
        for i, (x, y, z, color) in enumerate(self.stars):
            star_size = int((1 - z) * 5)
            xpos = int(x * widget.width())
            ypos = int(y * widget.height())
            painter.setBrush(color)
            if self.twinkle_state[i] > 0.9:  # Increase twinkle effect
                star_size += 1
            painter.drawEllipse(xpos, ypos, star_size, star_size)
