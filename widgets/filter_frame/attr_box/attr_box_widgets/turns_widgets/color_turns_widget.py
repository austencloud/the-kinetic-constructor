from typing import TYPE_CHECKING
from .base_turns_widget.base_turns_widget import TurnsWidget

if TYPE_CHECKING:
    from ...color_attr_box import ColorAttrBox


class ColorTurnsWidget(TurnsWidget):
    def __init__(self, attr_box: "ColorAttrBox") -> None:
        """Initialize the IGColorTurnsWidget."""
        super().__init__(attr_box)
        self.attr_box = attr_box

        self.color = self.attr_box.color
