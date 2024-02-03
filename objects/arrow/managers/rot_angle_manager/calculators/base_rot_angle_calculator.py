from typing import TYPE_CHECKING, Optional

from constants import *

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class BaseRotAngleCalculator:
    def __init__(self, arrow: "Arrow"):
        self.arrow = arrow

    def apply_rotation(self) -> None:
        angle = self.calculate_angle()
        self.arrow.setTransformOriginPoint(self.arrow.boundingRect().center())
        self.arrow.setRotation(angle)

    def calculate_angle(self) -> int:
        rot_angle_override_bool = self.get_rot_angle_override_bool()
        if rot_angle_override_bool:
            return self._get_rot_angle_override_according_to_loc(
                rot_angle_override_bool
            )
        return self._calculate_angle_impl()

    def get_rot_angle_override_bool(self) -> bool:
        if not self.arrow.motion.motion_type in [DASH, STATIC]:
            return False
        special_placements = (
            self.arrow.pictograph.main_widget.special_placement_loader.special_placements
        )
        ori_key = self.arrow.pictograph.arrow_placement_manager.special_positioner.data_updater.get_ori_key(
            self.arrow.motion
        )
        letter = self.arrow.pictograph.letter
        letter_data = special_placements.get(ori_key, {}).get(letter, {})
        turns_tuple = self.arrow.pictograph.main_widget.turns_tuple_generator.generate_turns_tuple(
            self.arrow.pictograph
        )
        rot_angle_override_key = self.arrow.pictograph.wasd_manager.rotation_angle_override_manager.key_generator.generate_rotation_angle_override_key(
            self.arrow
        )
        if not letter_data.get(turns_tuple):
            return False
        if not letter_data.get(turns_tuple).get(rot_angle_override_key):
            return False
        return letter_data.get(turns_tuple).get(rot_angle_override_key)

    def _calculate_angle_impl(self) -> int:
        raise NotImplementedError("Subclasses must implement this method")

    def _get_final_rot_angle_override(self) -> Optional[int]:
        special_manager = (
            self.arrow.pictograph.arrow_placement_manager.special_positioner
        )
        if special_manager:
            rotation_override = self.arrow.pictograph.wasd_manager.rotation_angle_override_manager.get_rot_angle_override_from_placements_dict(
                self.arrow
            )
            if rotation_override is not None:
                return self._get_rot_angle_override_according_to_loc(rotation_override)
        return None

    def _get_rot_angle_override_according_to_loc(self, rotation_override: int) -> int:
        if self.arrow.motion.start_ori in [IN, OUT]:
            static_angle_override_map = {
                NORTH: 180,
                EAST: {CLOCKWISE: 270, COUNTER_CLOCKWISE: 90},
                SOUTH: 0,
                WEST: {CLOCKWISE: 90, COUNTER_CLOCKWISE: 270},
            }
            dash_angle_override_map = {
                NORTH: 90,
                EAST: {CLOCKWISE: 180, COUNTER_CLOCKWISE: 0},
                SOUTH: 270,
                WEST: {CLOCKWISE: 0, COUNTER_CLOCKWISE: 180},
            }
        elif self.arrow.motion.start_ori in [CLOCK, COUNTER]:
            static_angle_override_map = {
                NORTH: 0,
                EAST: {CLOCKWISE: 90, COUNTER_CLOCKWISE: 270},
                SOUTH: 180,
                WEST: {CLOCKWISE: 270, COUNTER_CLOCKWISE: 90},
            }
            dash_angle_override_map = {
                NORTH: 270,
                EAST: {CLOCKWISE: 0, COUNTER_CLOCKWISE: 180},
                SOUTH: 90,
                WEST: {CLOCKWISE: 180, COUNTER_CLOCKWISE: 0},
            }
        if self.arrow.motion.motion_type == DASH:
            if rotation_override:
                loc_angle = dash_angle_override_map.get(self.arrow.loc)
                if isinstance(loc_angle, dict):
                    return loc_angle.get(self.arrow.motion.prop_rot_dir, 0)
                return loc_angle
        elif self.arrow.motion.motion_type == STATIC:
            if rotation_override:
                loc_angle = static_angle_override_map.get(self.arrow.loc)
                if isinstance(loc_angle, dict):
                    return loc_angle.get(self.arrow.motion.prop_rot_dir, 0)
                return loc_angle
        return None

    def _apply_rotation(self, angle: int) -> None:
        self.arrow.setTransformOriginPoint(self.arrow.boundingRect().center())
        self.arrow.setRotation(angle)
        if self.arrow.ghost:
            self.arrow.ghost.setRotation(angle)
