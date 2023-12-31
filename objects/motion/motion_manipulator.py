from typing import Dict, List, Literal, Tuple
from PyQt6.QtGui import QTransform
from Enums import (
    Direction,
    GridMode,
    Handpath,
    Location,
    MotionType,
    PropRotationDirection,
)
from constants import *
from data.start_end_loc_map import get_start_end_locs
from utilities.TypeChecking.TypeChecking import TYPE_CHECKING


if TYPE_CHECKING:
    from objects.motion.motion import Motion


class MotionManipulator:
    def __init__(self, motion: "Motion"):
        self.pictograph = motion.scene
        self.motion = motion
        self.arrow = motion.arrow
        self.prop = motion.prop
        self.color = motion.color
        self.other_color = RED if self.color == BLUE else BLUE

    def move_wasd(self, direction: Direction) -> None:
        wasd_location_map = {
            UP: {SOUTHEAST: NORTHEAST, SOUTHWEST: NORTHWEST},
            LEFT: {NORTHEAST: NORTHWEST, SOUTHEAST: SOUTHWEST},
            DOWN: {NORTHEAST: SOUTHEAST, NORTHWEST: SOUTHWEST},
            RIGHT: {NORTHWEST: NORTHEAST, SOUTHWEST: SOUTHEAST},
        }
        current_location = self.arrow.location
        new_location = wasd_location_map.get(direction, {}).get(
            current_location, current_location
        )
        (new_start_loc, new_end_loc) = get_start_end_locs(
            self.arrow.motion_type, self.motion.prop_rot_dir, new_location
        )
        pictograph_dict = {
            f"{self.color}_start_location": new_start_loc,
            f"{self.color}_end_location": new_end_loc,
        }
        self.pictograph.update_pictograph(pictograph_dict)

    ### MIRRORING ###

    def swap_rot_dir(self) -> None:
        if self.arrow.is_svg_mirrored:
            self.arrow.unmirror_svg()
        elif not self.arrow.is_svg_mirrored:
            self.arrow.mirror_svg()

        if self.motion.prop_rot_dir == COUNTER_CLOCKWISE:
            new_rot_dir = CLOCKWISE
        elif self.motion.prop_rot_dir == CLOCKWISE:
            new_rot_dir = COUNTER_CLOCKWISE
        elif self.motion.prop_rot_dir == "no_rotation":
            new_rot_dir = "no_rotation"

        new_start_loc = self.motion.end_loc
        new_end_loc = self.motion.start_loc

        pictograph_dict = {
            f"{self.color}_start_location": new_start_loc,
            f"{self.color}_end_location": new_end_loc,
            f"{self.color}_prop_rot_dir": new_rot_dir,
        }
        self.pictograph.update_pictograph(pictograph_dict)

    ### MOTION TYPE ###

    def swap_motion_type(self) -> None:
        if self.arrow.motion_type == ANTI:
            new_motion_type = PRO
        elif self.arrow.motion_type == PRO:
            new_motion_type = ANTI
        elif self.arrow.motion_type == STATIC:
            new_motion_type = STATIC

        if self.motion.prop_rot_dir == COUNTER_CLOCKWISE:
            new_rot_dir = CLOCKWISE
        elif self.motion.prop_rot_dir == CLOCKWISE:
            new_rot_dir = COUNTER_CLOCKWISE
        elif self.motion.prop_rot_dir == "no_rotation":
            new_rot_dir = "no_rotation"

        self.prop.swap_ori(self.prop.ori)
        pictograph_dict = {
            f"{self.color}_motion_type": new_motion_type,
            f"{self.color}_prop_rot_dir": new_rot_dir,
            f"{self.color}_end_ori": self.prop.ori,
        }
        self.pictograph.update_pictograph(pictograph_dict)

    ### ROTATION ###

    def rotate_motion(self, rotation_direction: Handpath) -> None:
        mode_mappings = self._get_mode_mappings()
        rotate_func, locations = mode_mappings.get(
            (self.motion.motion_type, self.arrow.pictograph.grid.grid_mode),
            (None, None),
        )

        if rotate_func:
            rotate_func(rotation_direction, locations)

    def _get_mode_mappings(self):
        """Returns mappings for different modes and motion types."""
        return {
            (STATIC, DIAMOND): (self._rotate_arrow, [NORTH, EAST, SOUTH, WEST]),
            (PRO, DIAMOND): (
                self._rotate_arrow,
                [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST],
            ),
            (ANTI, DIAMOND): (
                self._rotate_arrow,
                [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST],
            ),
            (FLOAT, DIAMOND): (
                self._rotate_arrow,
                [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST],
            ),
            (DASH, DIAMOND): (self._rotate_arrow, [NORTH, EAST, SOUTH, WEST]),
            (STATIC, BOX): (
                self._rotate_arrow,
                [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST],
            ),
            (PRO, BOX): (self._rotate_arrow, [NORTH, EAST, SOUTH, WEST]),
            (ANTI, BOX): (self._rotate_arrow, [NORTH, EAST, SOUTH, WEST]),
            (FLOAT, BOX): (self._rotate_arrow, [NORTH, EAST, SOUTH, WEST]),
            (DASH, BOX): (
                self._rotate_arrow,
                [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST],
            ),
        }

    def _rotate_arrow(self, handpath, locations: List[Location]) -> None:
        """
        Generic method to rotate arrows based on the handpath and locations.
        """
        current_index = locations.index(self.arrow.location)
        new_index = (
            (current_index + 1) % len(locations)
            if handpath == CW_HANDPATH
            else (current_index - 1) % len(locations)
        )
        new_location = locations[new_index]

        new_start_loc, new_end_loc = get_start_end_locs(
            self.arrow.motion_type, self.motion.prop_rot_dir, new_location
        )

        self._update_motion_attributes(new_location, new_start_loc, new_end_loc)

    def _update_motion_attributes(self, new_location, new_start_loc, new_end_loc):
        """
        Update motion attributes and reflect changes in the pictograph.
        """
        self.arrow.location = new_location
        self.motion.start_loc = new_start_loc
        self.motion.end_loc = new_end_loc
        self.prop.loc = new_end_loc

        self._refresh_pictograph()

    def _refresh_pictograph(self):
        """
        Refresh the arrow and prop, and update the pictograph.
        """
        self.arrow.update_arrow()
        self.prop.update_prop()
        self.arrow.scene.update_pictograph()
