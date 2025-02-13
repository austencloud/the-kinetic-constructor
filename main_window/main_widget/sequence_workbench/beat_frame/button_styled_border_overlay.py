from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QColor
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.generate_tab.freeform.letter_type_picker_widget.letter_type_widget import (
        LetterTypeButton,
    )


class StyledBorderOverlayForButton(QWidget):
    """
    Draws two concentric circles (outer + inner border) over the parent button.
    """

    def __init__(self, parent: "LetterTypeButton"):
        super().__init__(parent)
        self.parent_button = parent
        self.is_set = False
        self.primary_color = None
        self.secondary_color = None

        # Let clicks pass through this overlay
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.outer_border_width = 5
        self.inner_border_width = 5

    def update_border_colors(self, primary_color: str, secondary_color: str):
        self.primary_color = primary_color
        self.secondary_color = (
            secondary_color if primary_color != secondary_color else "transparent"
        )
        self.is_set = True
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.is_set or not self.primary_color or not self.secondary_color:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Outer border ellipse
        outer_rect = self.rect().adjusted(
            self.outer_border_width // 2,
            self.outer_border_width // 2,
            -self.outer_border_width // 2,
            -self.outer_border_width // 2,
        )
        pen = painter.pen()
        pen.setColor(QColor(self.primary_color))
        pen.setWidth(self.outer_border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawEllipse(outer_rect)

        # Inner border ellipse
        inner_rect = outer_rect.adjusted(
            self.inner_border_width,
            self.inner_border_width,
            -self.inner_border_width,
            -self.inner_border_width,
        )
        pen.setColor(QColor(self.secondary_color))
        pen.setWidth(self.inner_border_width)
        painter.setPen(pen)
        painter.drawEllipse(inner_rect)
