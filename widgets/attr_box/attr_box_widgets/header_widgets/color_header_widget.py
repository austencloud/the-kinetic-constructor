
from typing import TYPE_CHECKING
from utilities.TypeChecking.TypeChecking import Colors

from .base_header_widget import HeaderWidget

if TYPE_CHECKING:
    from widgets.attr_box.color_attr_box import ColorAttrBox
from constants import (
    BLUE,
)


class ColorHeaderWidget(HeaderWidget):
    def __init__(self, attr_box: "ColorAttrBox", color: Colors) -> None:
        super().__init__(attr_box)
        self.color = color
        self.header_label = self._setup_header_label(
            "Left" if self.color == BLUE else "Right"
        )
        self._setup_layout()

