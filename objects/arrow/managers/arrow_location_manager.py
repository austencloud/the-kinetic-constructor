from typing import TYPE_CHECKING
from .base_location_calculator import BaseLocationCalculator
from .dash_location_calculator import DashLocationCalculator
from .shift_location_calculator import ShiftLocationCalculator
from .static_location_calculator import StaticLocationCalculator
from constants import *

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowLocationManager:
    def __init__(self, arrow: "Arrow"):
        self.arrow = arrow
        self.calculator = self._select_calculator()

    def _select_calculator(self) -> "BaseLocationCalculator":
        calculator_map = {
            PRO: ShiftLocationCalculator,
            ANTI: ShiftLocationCalculator,
            FLOAT: ShiftLocationCalculator,
            DASH: DashLocationCalculator,
            STATIC: StaticLocationCalculator,
        }
        calculator_class = calculator_map.get(
            self.arrow.motion.motion_type, BaseLocationCalculator
        )
        return calculator_class(self.arrow)

    def update_location(self, new_location: str = None) -> None:
        if new_location:
            self.arrow.loc = new_location
        else:
            calculated_location = self.calculator.calculate_location()
            self.arrow.loc = calculated_location
