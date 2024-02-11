from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from PyQt6.QtGui import QColor
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph


class PictographFrameStyler:
    def __init__(self, pictograph: "Pictograph"):
        self.pictograph = pictograph
        self.border_colors = {
            "Type1": ("#6F2DA8", "#00b3ff"),  # Purple, Cyan
            "Type2": ("#6F2DA8", "#6F2DA8"),  # Purple, Purple
            "Type3": ("#6F2DA8", "#26e600"),  # Purple, Green
            "Type4": ("#26e600", "#26e600"),  # Green, Green
            "Type5": ("#26e600", "#00b3ff"),  # Green, Cyan
            "Type6": ("#eb7d00", "#eb7d00"),  # Orange, Orange
        }

    def update_view_border(self):

        primary_color, secondary_color = self.border_colors.get(
            self.pictograph.letter_type.name, ("transparent", "transparent")
        )

        stylesheet = f"border: 2px solid {primary_color};"
        self.pictograph.view.original_style = f"border: 2px solid {primary_color};"
        self.pictograph.view.setStyleSheet(stylesheet)

        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(secondary_color))
        shadow.setBlurRadius(0)  # Adjust the blur radius as needed
        shadow.setOffset(4, 4)  # Simulate the border width and direction
        self.pictograph.view.setGraphicsEffect(shadow)

    # Inside the PictographFrameStyler class

    def save_original_style(self):

        primary_color, secondary_color = self.border_colors.get(
            self.pictograph.letter_type.name, ("transparent", "transparent")
        )

        self.pictograph.view.original_style = f"border: 2px solid {primary_color};"
        self.pictograph.view.setStyleSheet(self.pictograph.view.original_style)

        shadow = QGraphicsDropShadowEffect()
        shadow.setColor(QColor(secondary_color))
        shadow.setBlurRadius(0)
        shadow.setOffset(4, 4)
        self.pictograph.view.setGraphicsEffect(shadow)
