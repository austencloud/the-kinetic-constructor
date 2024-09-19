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


