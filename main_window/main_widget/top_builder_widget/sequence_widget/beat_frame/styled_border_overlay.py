from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QPainter, QPen, QColor, QResizeEvent
from PyQt6.QtCore import Qt, QRect
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from base_widgets.base_pictograph.components.pictograph_view import (
        PictographView,
    )
import math


class StyledBorderOverlay(QWidget):
    def __init__(self, view: "PictographView") -> None:
        super().__init__(view)
        self.view = view
        self.is_set = False
        self.primary_color = None
        self.secondary_color = None
        self.saved_primary_color = None
        self.saved_secondary_color = None
        self.setFixedSize(view.size())
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def resize_styled_border_overlay(self) -> None:
        self.setFixedSize(self.view.width(), self.view.height())
        self.update_border_widths()

    def update_border_widths(self) -> None:
        view_width = self.view.size().width()
        self.outer_border_width = max(1, math.ceil(view_width * 0.016))
        self.inner_border_width = max(1, math.ceil(view_width * 0.016))
        self.update()

    def update_border_color_and_width(self, primary_color, secondary_color) -> None:
        self.update_border_widths()
        self.primary_color = primary_color
        self.secondary_color = (
            secondary_color if primary_color != secondary_color else "transparent"
        )
        self.is_set = True
        self.update()

    def paintEvent(self, event) -> None:
        if self.primary_color and self.secondary_color:
            painter = QPainter(self)
            self._draw_borders(painter)

    def _draw_borders(self, painter: QPainter) -> None:
        pen = QPen()
        outer_border = self._draw_outer_border(painter, pen)
        self._draw_inner_border(painter, pen, outer_border)

    def _draw_inner_border(
        self, painter: QPainter, pen: QPen, outer_rect: QRect
    ) -> None:
        pen.setColor(QColor(self.secondary_color))
        pen.setWidth(self.inner_border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)
        inner_offset = self.outer_border_width - (
            self.outer_border_width - self.inner_border_width
        )
        inner_rect = outer_rect.adjusted(
            inner_offset,
            inner_offset,
            -inner_offset,
            -inner_offset,
        )
        painter.drawRect(inner_rect)

    def _draw_outer_border(self, painter: QPainter, pen: QPen) -> QRect:
        pen.setColor(QColor(self.primary_color))
        pen.setWidth(self.outer_border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)
        outer_rect = self.rect().adjusted(
            self.outer_border_width // 2,
            self.outer_border_width // 2,
            -(self.outer_border_width // 2),
            -(self.outer_border_width // 2),
        )
        painter.drawRect(outer_rect)
        return outer_rect

    def set_gold_border(self) -> None:
        # Add a condition to skip setting the gold border when in quiz mode
        if getattr(self.view.pictograph, 'is_quiz_mode', False):
            # If in quiz mode, don't apply the gold border
            return
        self.saved_primary_color = self.primary_color
        self.saved_secondary_color = self.secondary_color
        self.update_border_color_and_width("gold", "gold")

    def reset_border(self) -> None:
        if self.saved_primary_color and self.saved_secondary_color:
            self.update_border_color_and_width(
                self.saved_primary_color, self.saved_secondary_color
            )

    def set_thick_gold_border(self) -> None:
        self.saved_primary_color = self.primary_color
        self.saved_secondary_color = self.secondary_color
        self.update_border_color_and_width("gold", "gold")

