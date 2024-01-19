from typing import TYPE_CHECKING

from constants import CLOCK, COUNTER, IN, OUT


if TYPE_CHECKING:
    from objects.prop.prop import Prop


class PropChecker:
    def __init__(self, prop: "Prop") -> None:
        self.prop = prop

    def is_radial(self) -> bool:
        return self.prop.ori in [IN, OUT]

    def is_antiradial(self) -> bool:
        return self.prop.ori in [CLOCK, COUNTER]
