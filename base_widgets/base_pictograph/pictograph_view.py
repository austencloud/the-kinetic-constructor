import math
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsView, QFrame
from PyQt6.QtCore import Qt, QEvent, QRectF
from PyQt6.QtGui import QPainter, QPen, QColor, QCursor, QKeyEvent, QMouseEvent

from Enums.letters import LetterType

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class PictographView(QGraphicsView):
    def __init__(self, pictograph: "BasePictograph") -> None:
        super().__init__(pictograph)
        self.pictograph = pictograph

        # Remove any frames or borders
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setStyleSheet("background: transparent; border: none;")

        # Disable scrollbars and set alignment
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Set contents margins to zero
        self.setContentsMargins(0, 0, 0, 0)
        self.viewport().setContentsMargins(0, 0, 0, 0)
        self.setViewportMargins(0, 0, 0, 0)

        # Initialize border colors
        self.primary_color = None
        self.secondary_color = None
        self.saved_primary_color = None
        self.saved_secondary_color = None
        self.update_borders()

        # Additional initializations if necessary
        self.grabGesture(Qt.GestureType.TapGesture)
        self.grabGesture(Qt.GestureType.TapAndHoldGesture)

    ### BORDER METHODS ###

    def update_borders(self):
        """Initialize or update the border colors based on the pictograph's letter type."""
        letter_type = self.pictograph.letter_type
        border_colors_map = {
            LetterType.Type1: ("#36c3ff", "#6F2DA8"),  # Cyan, Purple
            LetterType.Type2: ("#6F2DA8", "#6F2DA8"),  # Purple, Purple
            LetterType.Type3: ("#26e600", "#6F2DA8"),  # Green, Purple
            LetterType.Type4: ("#26e600", "#26e600"),  # Green, Green
            LetterType.Type5: ("#00b3ff", "#26e600"),  # Cyan, Green
            LetterType.Type6: ("#eb7d00", "#eb7d00"),  # Orange, Orange
        }
        self.primary_color, self.secondary_color = border_colors_map.get(
            letter_type, ("black", "black")
        )
        self.update()  # Trigger repaint

    def set_gold_border(self):
        """Set the border colors to gold, typically on hover."""
        if getattr(self.pictograph, "disable_gold_overlay", False):
            return
        self.saved_primary_color = self.primary_color
        self.saved_secondary_color = self.secondary_color
        self.primary_color = "gold"
        self.secondary_color = "gold"
        self.update()

    def reset_border(self):
        """Reset the border colors to their original values."""
        if self.saved_primary_color and self.saved_secondary_color:
            self.primary_color = self.saved_primary_color
            self.secondary_color = self.saved_secondary_color
            self.update()
        else:
            self.update_borders()

    ### EVENTS ###

    def paintEvent(self, event):
        """Draw the pictograph and borders."""
        super().paintEvent(event)
        painter = QPainter(self.viewport())
        if self.primary_color and self.secondary_color:
            self._draw_borders(painter)

    def _draw_borders(self, painter: QPainter):
        """Draw the outer and inner borders."""
        pen = QPen()
        # Use floating-point calculations
        view_width = self.viewport().size().width()
        outer_border_width = max(1.0, view_width * 0.016)
        inner_border_width = max(1.0, view_width * 0.016)

        # Calculate half pen widths
        half_outer_pen = outer_border_width / 2.0
        half_inner_pen = inner_border_width / 2.0

        # Draw outer border
        pen.setColor(QColor(self.primary_color))
        pen.setWidthF(outer_border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)

        # Convert viewport rect to QRectF
        outer_rect = QRectF(self.viewport().rect())
        outer_rect = outer_rect.adjusted(
            +half_outer_pen,
            +half_outer_pen,
            -half_outer_pen,
            -half_outer_pen,
        )
        painter.drawRect(outer_rect)

        # Draw inner border
        pen.setColor(QColor(self.secondary_color))
        pen.setWidthF(inner_border_width)
        pen.setJoinStyle(Qt.PenJoinStyle.MiterJoin)
        painter.setPen(pen)
        inner_rect = outer_rect.adjusted(
            +half_inner_pen,
            +half_inner_pen,
            -half_inner_pen,
            -half_inner_pen,
        )
        painter.drawRect(inner_rect)



    def enterEvent(self, event: QEvent) -> None:
        """Handle mouse entering the widget area."""
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.set_gold_border()

    def leaveEvent(self, event: QEvent) -> None:
        """Handle mouse leaving the widget area."""
        self.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.reset_border()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        """Handle mouse press events."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Handle left-click events
            pass  # Replace with your event handling code
        super().mousePressEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        """Handle key press events."""
        # Handle key events if necessary
        super().keyPressEvent(event)

    # Additional methods if needed

    def update_border_widths(self) -> None:
        view_width = self.size().width()
        self.outer_border_width = max(1, math.ceil(view_width * 0.016))
        self.inner_border_width = max(1, math.ceil(view_width * 0.016))
        self.update()
