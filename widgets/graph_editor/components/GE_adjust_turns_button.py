from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtWidgets import QAbstractButton


class GE_AdjustTurnsButton(QAbstractButton):
    def __init__(self, icon_path, disabled_icon_path, parent=None):
        super().__init__(parent)
        self.icon_pixmap = QPixmap(icon_path)
        self.disabled_icon_pixmap = QPixmap(disabled_icon_path)
        self.hovered = False
        self.enabled = True

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        current_pixmap = self.icon_pixmap if self.enabled else self.disabled_icon_pixmap

        button_color = (
            Qt.GlobalColor.gray
            if not self.enabled
            else (Qt.GlobalColor.lightGray if self.hovered else Qt.GlobalColor.white)
        )
        painter.setBrush(button_color)

        rect = QRect(0, 0, self.width(), self.height())
        painter.fillRect(rect, painter.brush())

        icon_size = int(min(self.width(), self.height()) * 0.6)
        x = int((self.width() - icon_size) / 2)
        y = int((self.height() - icon_size) / 2)
        icon_rect = QRect(x, y, icon_size, icon_size)

        painter.drawPixmap(icon_rect, current_pixmap)

    def enterEvent(self, event):
        if self.enabled:
            self.hovered = True
            self.update()

    def leaveEvent(self, event):
        self.hovered = False
        self.update()

    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        self.enabled = enabled
        self.update()
