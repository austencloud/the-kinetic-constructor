from constants import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class BaseRotAngleCalculator:
    def __init__(self, arrow: "Arrow"):
        self.arrow = arrow

    def calculate_angle(self):
        raise NotImplementedError("Must be implemented by subclasses.")

    def apply_rotation(self, angle):
        self.arrow.setTransformOriginPoint(self.arrow.boundingRect().center())
        self.arrow.setRotation(angle)
        if hasattr(self.arrow, "ghost") and self.arrow.ghost:
            self.arrow.ghost.setRotation(angle)

