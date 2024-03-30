from PyQt6.QtWidgets import QTabBar, QTabWidget
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt


class CustomTabBar(QTabBar):
    def enterEvent(self, event):
        # Change the cursor shape to pointing hand cursor when hovering over the tab
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        super().enterEvent(event)

    def leaveEvent(self, event):
        # Change the cursor shape back to the default arrow cursor when not hovering over the tab
        self.unsetCursor()  # This resets to the default cursor
        super().leaveEvent(event)
