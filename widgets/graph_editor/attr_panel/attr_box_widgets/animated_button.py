from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
from PyQt6.QtWidgets import QPushButton, QWidget

class AnimatedButton(QPushButton):
    def __init__(self, widget: QWidget):
        super().__init__(widget)
        self.widget = widget
        self.color_animation = QPropertyAnimation(self, b"backgroundColor")
        self.original_color = self.palette().color(QPalette.ColorRole.Button)
        self.setStyleSheet(self.get_button_style())
        
    def enterEvent(self, event):
        self.animateColor(QColor(200, 200, 200))  # Lighter color on hover
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.animateColor(self.original_color)  # Original color on leave
        super().leaveEvent(event)

    def animateColor(self, new_color):
        self.color_animation.stop()
        self.color_animation.setDuration(300)
        self.color_animation.setStartValue(self.palette().color(QPalette.ColorRole.Button))
        self.color_animation.setEndValue(new_color)
        self.color_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.color_animation.start()

    def get_button_style(self) -> str:
        button_size = self.widget.width() / 6
        border_radius = button_size / 2
        return (
            f"QPushButton {{" 
            f"   border-radius: {border_radius}px;"
            f"   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            f"   stop:0 rgba(255, 255, 255, 255), stop:1 rgba(200, 200, 200, 255));"
            f"   border: 1px solid black;"
            f"   min-width: {button_size}px;"
            f"   min-height: {button_size}px;"
            f"}}"
            f"QPushButton:pressed {{" 
            f"   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            f"   stop:0 rgba(204, 228, 247, 255), stop:1 rgba(164, 209, 247, 255));"
            f"}}"
            f"QPushButton:hover:!pressed {{" 
            f"   border: 1px solid #1c1c1c;"
            f"   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            f"   stop:0 rgba(255, 255, 255, 255), stop:1 rgba(230, 230, 230, 255));"
            f"}}"
        )
