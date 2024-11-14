from PyQt6.QtWidgets import QFrame, QVBoxLayout
from typing import TYPE_CHECKING

from Enums.Enums import LetterType
from main_window.main_widget.sequence_widget.beat_frame.styled_border_overlay import StyledBorderOverlay



if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class PictographContainer(QFrame):
    def __init__(self, pictograph: "BasePictograph") -> None:
        super().__init__()
        self.pictograph = pictograph
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.view = pictograph.view
        self.layout().addWidget(self.view)
        self.border_colors_map = self._get_border_colors_map()
        self.styled_border_overlay = StyledBorderOverlay(self.view)

    def _get_border_colors_map(self) -> dict[LetterType, tuple[str, str]]:
        border_colors_map = {
            LetterType.Type1: ("#36c3ff", "#6F2DA8"),  # Cyan, Purple
            LetterType.Type2: ("#6F2DA8", "#6F2DA8"),  # Purple, Purple
            LetterType.Type3: ("#26e600", "#6F2DA8"),  # Green, Purple
            LetterType.Type4: ("#26e600", "#26e600"),  # Green, Green
            LetterType.Type5: ("#00b3ff", "#26e600"),  # Cyan, Green
            LetterType.Type6: ("#eb7d00", "#eb7d00"),  # Orange, Orange
        }
        return border_colors_map

    def get_border_colors(self) -> tuple[str, str]:
        letter_type = self.pictograph.letter_type
        return self.border_colors_map.get(letter_type, ("black", "black"))

    def update_borders(self) -> None:
        primary_color, secondary_color = self.get_border_colors()
        self.styled_border_overlay.update_border_color_and_width(
            primary_color, secondary_color
        )
        self.styled_border_overlay.update()
