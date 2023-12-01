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
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box_widgets.start_end_widget import (
        StartEndWidget,
    )
    from widgets.graph_editor.attr_panel.attr_box_widgets.turns_widget import (
        TurnsWidget,
    )
    from widgets.graph_editor.attr_panel.attr_box_widgets.motion_types_widget import (
        MotionTypesWidget,
    )


class CustomButton(QPushButton):
    def __init__(
        self, widget: Union["StartEndWidget", "TurnsWidget", "MotionTypesWidget"]
    ):
        super().__init__(widget)
        self._color = self.palette().color(QPalette.ColorRole.Button)
        self.widget = widget
        self.color_animation = QPropertyAnimation(self, b"animatedColor")
        self.button_size = int(self.widget.attr_box.attr_box_width * 0.2 * 0.8)
        self.border_radius = self.button_size / 2
        self.setStyleSheet(self.get_button_style())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Define the circular shape
        clipping_rectF = QRectF(self.rect().adjusted(1, 1, -1, -1))
        painter.setBrush(QBrush(self._color))
        pen = QPen(Qt.GlobalColor.black, 1)
        painter.setPen(pen)
        painter.drawEllipse(clipping_rectF)

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
        self.color_animation.setDuration(1000)  # Set the duration to 1000 milliseconds (1 second)
        self.color_animation.setStartValue(self._color)
        self.color_animation.setEndValue(new_color)
        self.color_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.color_animation.start()

    def get_button_style(self):
        return (
            f"QPushButton {{"
            f"   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(200, 200, 200, 255));"
            f"   border-radius: {self.border_radius}px;"
            f"   border: 1px solid black;"
            f"   min-width: {self.button_size}px;"
            f"   min-height: {self.button_size}px;"  # Adjust height to match width for a circle
            f"   max-width: {self.button_size}px;"
            f"   max-height: {self.button_size}px;"
            f"}}"
            f"QPushButton:hover {{"
            f"   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(230, 230, 230, 255), stop:1 rgba(200, 200, 200, 255));"
            f"}}"
            f"QPushButton:pressed {{"
            f"   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(204, 228, 247, 255), stop:1 rgba(164, 209, 247, 255));"
            f"}}"
        )

    def isPointInCircle(self, point: QPoint):
        center = QPoint(int(self.width() / 2), int(self.height() / 2))
        radius = min(self.width(), self.height()) / 2
        return (point - center).manhattanLength() < radius
