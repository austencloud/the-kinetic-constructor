from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import Qt, QPropertyAnimation, QRect, QTimer, pyqtProperty
from PyQt6.QtGui import QPainter, QColor, QPen


class LoadingSpinnerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.angle = 0  # Start angle for the spinner
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_angle)
        self.timer.start(10)  # Adjust for rotation speed

        self.animation = QPropertyAnimation(self, b"angle")
        self.animation.setStartValue(0)
        self.animation.setEndValue(360)
        self.animation.setDuration(2000)  # Duration of one full rotation
        self.animation.setLoopCount(-1)  # Loop indefinitely
        self.animation.start()

    @pyqtProperty(int)
    def angle(self):
        return self._angle

    @angle.setter
    def angle(self, value):
        self._angle = value
        self.update()  # Trigger a repaint

    def update_angle(self):
        self.angle += 2  # Rotate by 2 degrees each time
        if self.angle >= 360:
            self.angle = 0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Determine the size of the spinner
        size = min(self.width(), self.height()) // 2
        spinner_rect = QRect(
            self.width() // 2 - size, self.height() // 2 - size, 2 * size, 2 * size
        )

        # Draw the rotating arc
        pen = QPen(QColor("#3498db"))  # Blue color, adjust as needed
        pen.setWidth(5)  # Width of the spinner arc
        painter.setPen(pen)
        painter.drawArc(
            spinner_rect, self.angle * 16, 120 * 16
        )  # 120 degrees of the arc
