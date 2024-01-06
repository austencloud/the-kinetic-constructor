from typing import TYPE_CHECKING
from objects.pictograph.position_engines.arrow_positioners.arrow_positioner import (
    ArrowPositioner,
)
from constants import (
    RED,
    BLUE,
    PRO,
    ANTI,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    NORTHEAST,
    SOUTHEAST,
    SOUTHWEST,
    NORTHWEST,
)
from objects.arrow import Arrow
from PyQt6.QtCore import QPointF
from objects.pictograph.position_engines.arrow_positioners.by_letter.G_positioner import (
    G_Positioner,
)

from objects.pictograph.position_engines.arrow_positioners.by_letter.I_positioner import (
    I_Positioner,
)

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph


class Type1ArrowPositioner(ArrowPositioner):
    def __init__(self, pictograph: "Pictograph") -> None:
        super().__init__(pictograph)

    def _reposition_arrows(self) -> None:
        if self.letter_type == "Type1":
            self.reposition_for_letter(self.letter)
