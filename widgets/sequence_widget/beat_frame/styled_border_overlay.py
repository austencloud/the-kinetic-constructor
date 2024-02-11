from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.pictograph.components.pictograph_view import PictographView


class StyledBorderOverlay(QWidget):
    def __init__(self, view: "PictographView"):
        super().__init__(view)
        self.view = view
        self.primary_color = None
        self.secondary_color = None
        self.primary_border_width = 3
        self.secondary_border_width = 2
        self.setFixedSize(view.size())
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def update_border_colors(self, primary_color, secondary_color):
        self.primary_color = primary_color
        self.secondary_color = (
            secondary_color if primary_color != secondary_color else "transparent"
        )
        self.update()  # Call this to trigger a repaint

    def resize_styled_border_overlay(self):
        self.setFixedSize(
            self.view.size().width(),
            self.view.size().height(),
        )

    def paintEvent(self, event):
        if self.primary_color and self.secondary_color:
            painter = QPainter(self)
            pen = QPen()

            # Outer border
            pen.setColor(QColor(self.primary_color))
            pen.setWidth(self.primary_border_width)
            painter.setPen(pen)
            outer_rect = self.rect().adjusted(
                self.primary_border_width // 2,
                self.primary_border_width // 2,
                -(self.primary_border_width // 2),
                -(self.primary_border_width // 2),
            )
            painter.drawRect(outer_rect)

            # Inner border
            pen.setColor(QColor(self.secondary_color))
            pen.setWidth(self.secondary_border_width)
            painter.setPen(pen)
            inner_offset = self.primary_border_width - (
                self.secondary_border_width // 2
            )
            inner_rect = outer_rect.adjusted(
                inner_offset,
                inner_offset,
                -inner_offset,
                -inner_offset,
            )
            painter.drawRect(inner_rect)

    def set_gold_border(self):
        self.saved_primary_color = self.primary_color
        self.saved_secondary_color = self.secondary_color
        self.update_border_colors("gold", "gold")

    def reset_border(self):
        self.update_border_colors(self.saved_primary_color, self.saved_secondary_color)
