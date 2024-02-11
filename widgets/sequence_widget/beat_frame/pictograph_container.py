from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtCore import QEvent
from PyQt6.QtGui import QPainter, QPen, QColor
from typing import TYPE_CHECKING

from Enums import LetterType
from widgets.pictograph.components.pictograph_view import PictographView
from widgets.sequence_widget.beat_frame.styled_border_overlay import StyledBorderOverlay

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class PictographContainer(QFrame):
    def __init__(self, pictograph: "Pictograph"):
        super().__init__()
        self.pictograph = pictograph
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.view = PictographView(pictograph)
        self.layout().addWidget(self.view)
        self.border_colors_map = self._get_border_colors_map()
        self.styled_border_overlay = StyledBorderOverlay(self.view)

    def _get_border_colors_map(self):
        border_colors_map = {
            LetterType.Type1: ("#6F2DA8", "#00b3ff"),  # Purple, Cyan
            LetterType.Type2: ("#6F2DA8", "#6F2DA8"),  # Purple, Purple
            LetterType.Type3: ("#6F2DA8", "#26e600"),  # Purple, Green
            LetterType.Type4: ("#26e600", "#26e600"),  # Green, Green
            LetterType.Type5: ("#26e600", "#00b3ff"),  # Green, Cyan
            LetterType.Type6: ("#eb7d00", "#eb7d00"),  # Orange, Orange
        }
        return border_colors_map

    def paintEvent(self, event: QEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        primary_color, secondary_color = self.get_border_colors()

        outer_border_rect = self.rect()
        inner_border_rect = outer_border_rect.adjusted(4, 4, -4, -4)

        painter.setPen(QPen(QColor(primary_color), 4))
        painter.drawRect(outer_border_rect)

        painter.setPen(QPen(QColor(secondary_color), 2))
        painter.drawRect(inner_border_rect)

    def get_border_colors(self) -> tuple[str, str]:
        letter_type = self.pictograph.letter_type
        return self.border_colors_map.get(letter_type, ("black", "black"))

    def update_borders(self):
        # Update border colors based on the letter type
        primary_color, secondary_color = self.get_border_colors()
        self.styled_border_overlay.update_border_colors(primary_color, secondary_color)
        self.styled_border_overlay.update()  # Trigger a repaint of the over
