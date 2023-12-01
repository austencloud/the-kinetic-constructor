from PyQt6.QtWidgets import QPushButton, QWidget
from PyQt6.QtCore import (
    QPropertyAnimation,
    QEasingCurve,
    pyqtProperty,
    Qt,
    QRectF,
    QPoint,
)
from PyQt6.QtGui import QColor, QPainter, QBrush, QPen, QPalette, QPainterPath
from PyQt6.QtGui import QMouseEvent



class AnimatedButton(QPushButton):
    def __init__(self, widget: QWidget):
        super().__init__(widget)
        self._color = self.palette().color(QPalette.ColorRole.Button)
        self.widget = widget
        self.color_animation = QPropertyAnimation(self, b"animatedColor")
        self.button_size = self.widget.width() * 0.2
        self.border_radius = self.button_size / 2
        self.setStyleSheet(self.get_button_style())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Convert QRect to QRectF for addEllipse
        clipping_rect = self.rect().adjusted(1, 1, -1, -1)
        clipping_rectF = QRectF(clipping_rect)

        # Create an elliptical path for clipping
        path = QPainterPath()
        path.addEllipse(clipping_rectF)

        # Set the path as the clipping path
        painter.setClipPath(path)

        # Draw the circle
        painter.setBrush(QBrush(self._color))
        pen = QPen(Qt.GlobalColor.black, 1)
        painter.setPen(pen)
        painter.drawPath(path)

        super().paintEvent(event)
        
    @pyqtProperty(QColor)
    def animatedColor(self):
        return self._color

    @animatedColor.setter
    def animatedColor(self, color):
        self._color = color
        self.update()

    def enterEvent(self, event):
        self.startColorAnimation(QColor(200, 200, 200))  # Lighter color on hover
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.startColorAnimation(
            self.palette().color(QPalette.ColorRole.Button)
        )  # Original color on leave
        super().leaveEvent(event)

    def startColorAnimation(self, new_color):
        self.color_animation.stop()
        self.color_animation.setDuration(300)
        self.color_animation.setStartValue(self._color)
        self.color_animation.setEndValue(new_color)
        self.color_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.color_animation.start()

    def get_button_style(self):
        return (
            f"QPushButton {{"
            f"   border-radius: {self.border_radius}px;"
            f"   border: none;"
            f"   min-width: {self.button_size}px;"
            f"   min-height: {self.button_size}px;"
            f"}}"
            f"QPushButton:pressed {{"
            f"   background-color: rgba(204, 228, 247, 255);"
            f"}}"
        )

    def mousePressEvent(self, event: QMouseEvent):
        if self.isPointInCircle(event.pos()):
            super().mousePressEvent(event)
        else:
            event.ignore()

    def isPointInCircle(self, point: QPoint):
        center = QPoint(int(self.width() / 2), int(self.height() / 2))
        radius = min(self.width(), self.height()) / 2
        return (point - center).manhattanLength() < radius
