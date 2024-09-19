from PyQt6.QtWidgets import QCheckBox, QApplication
from PyQt6.QtCore import QPropertyAnimation, QRect, Qt, pyqtProperty, QEasingCurve
from PyQt6.QtGui import QColor, QPainter


class PyToggle(QCheckBox):
    def __init__(
        self,
        width=60,
        bg_color="#00BCff",  # Set the background color to be consistent
        circle_color="#DDD",
        animation_curve=QEasingCurve.Type.OutBounce,
    ):
        super().__init__()
        self.setFixedSize(width, 28)
        self.setCursor(Qt.CursorShape.PointingHandCursor)

        # Colors
        self._bg_color = QColor(bg_color)
        self._circle_color = QColor(circle_color)

        # Animation properties
        self._circle_position = 3  # Initial circle position
        self.animation = QPropertyAnimation(self, b"circle_position", self)
        self.animation.setEasingCurve(animation_curve)
        self.animation.setDuration(300)

        # Connect to state change
        self.stateChanged.connect(self.start_transition)

    def start_transition(self, state):
        """Start the animation when toggle is clicked."""
        self.animation.stop()  # Stop any ongoing animation
        if state:
            self.animation.setEndValue(self.width() - 26)
        else:
            self.animation.setEndValue(3)
        self.animation.start()

    @pyqtProperty(float)
    def circle_position(self):
        return self._circle_position

    # SET A NEW HIT AREA
    def hitButton(self, pos):
        return self.contentsRect().contains(pos)

    @circle_position.setter
    def circle_position(self, pos):
        self._circle_position = pos
        self.update()

    def paintEvent(self, e):
        """Custom paint for drawing the toggle switch."""
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw the background (always the same color)
        rect = QRect(0, 0, self.width(), self.height())
        p.setBrush(self._bg_color)

        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(rect, self.height() / 2, self.height() / 2)

        # Draw the circle using the animated position
        p.setBrush(self._circle_color)
        p.drawEllipse(int(self._circle_position), 3, 22, 22)
        p.end()
