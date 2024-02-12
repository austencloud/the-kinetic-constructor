from typing import TYPE_CHECKING, Optional
from abc import ABC, abstractmethod

from constants import *

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class BaseRotAngleCalculator(ABC):
    def __init__(self, arrow: "Arrow"):
        self.arrow = arrow
        self.rot_angle_key_generator = (
            self.arrow.pictograph.wasd_manager.rotation_angle_override_manager.key_generator
        )
        self.data_updater = (
            self.arrow.pictograph.arrow_placement_manager.special_positioner.data_updater
        )

    def apply_rotation(self) -> None:
        angle = self.calculate_angle()
        self.arrow.setTransformOriginPoint(self.arrow.boundingRect().center())
        self.arrow.setRotation(angle)

    @abstractmethod
    def calculate_angle(self) -> int:
        pass

    def has_rotation_angle_override(self) -> bool:
        if self.arrow.motion.motion_type not in [DASH, STATIC]:
            return False

        special_placements = (
            self.arrow.pictograph.main_widget.special_placement_loader.special_placements
        )
        ori_key = self.data_updater.get_ori_key(self.arrow.motion)
        letter = self.arrow.pictograph.letter

        letter_data = special_placements.get(ori_key, {}).get(letter, {})
        
        rot_angle_override_key = (
            self.rot_angle_key_generator.generate_rotation_angle_override_key(
                self.arrow
            )
        )

        return bool(letter_data.get(self.arrow.pictograph.turns_tuple, {}).get(rot_angle_override_key))

    def _apply_rotation(self, angle: int) -> None:
        self.arrow.setTransformOriginPoint(self.arrow.boundingRect().center())
        self.arrow.setRotation(angle)
        if self.arrow.ghost:
            self.arrow.ghost.setRotation(angle)
