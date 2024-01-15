from typing import TYPE_CHECKING
from .base_turns_widget.base_turns_widget import BaseTurnsWidget

if TYPE_CHECKING:
    from ...color_attr_box import ColorAttrBox


class ColorTurnsWidget(BaseTurnsWidget):
    def __init__(self, attr_box: "ColorAttrBox") -> None:
        """Initialize the IGColorTurnsWidget."""
        super().__init__(attr_box)
        self.attr_box = attr_box

        self.attr_box.same_button = self.attr_box.vtg_dir_widget.same_button
        self.color = self.attr_box.color
        self.pictographs = self.attr_box.pictographs



