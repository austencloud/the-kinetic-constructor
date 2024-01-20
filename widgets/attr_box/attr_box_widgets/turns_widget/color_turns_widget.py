from typing import TYPE_CHECKING

from .base_turns_widget.base_turns_widget import TurnsWidget

if TYPE_CHECKING:
    from widgets.attr_box.attr_box import AttrBox

class ColorTurnsWidget(TurnsWidget):
    def __init__(self, attr_box: "AttrBox") -> None:
        """Initialize the IGColorTurnsWidget."""
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.color = self.attr_box.color
