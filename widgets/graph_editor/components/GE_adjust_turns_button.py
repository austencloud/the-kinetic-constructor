from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QRect, QRectF
from PyQt6.QtGui import QPainter
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QAbstractButton

if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_turns_widget import GE_TurnsWidget


class GE_AdjustTurnsButton(QAbstractButton):
    def __init__(self, svg_path, turns_widget: "GE_TurnsWidget"):
        super().__init__(turns_widget)
        self.svg_renderer = QSvgRenderer(svg_path)
        self.hovered = False

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        current_renderer = (
            self.svg_renderer if self.isEnabled() else self.disabled_svg_renderer
        )

        button_color = (
            Qt.GlobalColor.gray
            if not self.isEnabled()
            else (Qt.GlobalColor.lightGray if self.hovered else Qt.GlobalColor.white)
        )
        painter.setBrush(button_color)

        rect = QRect(0, 0, self.width(), self.height())
        painter.fillRect(rect, painter.brush())

        icon_size = int(min(self.width(), self.height()) * 0.8)
        x = int((self.width() - icon_size) / 2)
        y = int((self.height() - icon_size) / 2)
        icon_rect = QRectF(x, y, icon_size, icon_size)

        current_renderer.render(painter, icon_rect)

    def enterEvent(self, event):
        self.hovered = True
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.hovered = False
        self.update()
        super().leaveEvent(event)
