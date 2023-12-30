from typing import List
from PyQt6.QtGui import QTransform
from Enums import (
    Direction,
    Location,
    PropRotationDirection,
)
from constants import *
from data.start_end_loc_map import get_start_end_locs
from objects.motion.motion import Motion
from utilities.TypeChecking.TypeChecking import TYPE_CHECKING


if TYPE_CHECKING:
    from objects.arrow import Arrow


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
            self.unmirror_svg()
        elif not self.arrow.is_svg_mirrored:
            self.mirror_svg()

        if self.motion.prop_rot_dir == COUNTER_CLOCKWISE:
            new_rot_dir = CLOCKWISE
        elif self.motion.prop_rot_dir == CLOCKWISE:
            new_rot_dir = COUNTER_CLOCKWISE
        elif self.motion.prop_rot_dir == "NoRotation":
            new_rot_dir = "NoRotation"

        new_start_loc = self.motion.end_loc
        new_end_loc = self.motion.start_loc

        pictograph_dict = {
            f"{self.color}_start_location": new_start_loc,
            f"{self.color}_end_location": new_end_loc,
            f"{self.color}_prop_rot_dir": new_rot_dir,
        }
        self.pictograph.update_pictograph(pictograph_dict)

    def mirror_svg(self) -> None:
        self.arrow.set_arrow_transform_origin_to_center()
        transform = QTransform()
        transform.translate(self.arrow.center_x, self.arrow.center_y)
        transform.scale(-1, 1)
        transform.translate(-self.arrow.center_x, -self.arrow.center_y)
        self.arrow.setTransform(transform)
        if hasattr(self.arrow, GHOST) and self.arrow.ghost:
            self.arrow.ghost.setTransform(transform)
            self.arrow.ghost.is_svg_mirrored = True
        self.arrow.is_svg_mirrored = True

    def unmirror_svg(self) -> None:
        transform = QTransform()
        transform.translate(self.arrow.center.x(), self.arrow.center.y())
        transform.scale(1, 1)
        transform.translate(-self.arrow.center.x(), -self.arrow.center.y())
        self.arrow.setTransform(transform)
        if hasattr(self.arrow, GHOST) and self.arrow.ghost:
            self.arrow.ghost.setTransform(transform)
            self.arrow.ghost.is_svg_mirrored = False
        self.arrow.is_svg_mirrored = False

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
        elif self.motion.prop_rot_dir == "NoRotation":
            new_rot_dir = "NoRotation"

        self.prop.ori = self.prop.swap_ori(self.prop.ori)
        self.motion.end_ori = self.prop.ori
        self.prop.update_prop()
        pictograph_dict = {
            f"{self.color}_motion_type": new_motion_type,
            f"{self.color}_prop_rot_dir": new_rot_dir,
        }

        self.pictograph.update_pictograph(pictograph_dict)

    ### ROTATION ###

    def rotate_arrow(self, rot_dir: PropRotationDirection) -> None:
        diamond_mode_static_arrow_locations = [
            NORTH,
            EAST,
            SOUTH,
            WEST,
        ]
        diamond_mode_shift_arrow_locations = [
            NORTHEAST,
            SOUTHEAST,
            SOUTHWEST,
            NORTHWEST,
        ]
        diamond_mode_dash_arrow_locations = [
            NORTH,
            EAST,
            SOUTH,
            WEST,
        ]

        box_mode_static_arrow_locations = [
            NORTHEAST,
            SOUTHEAST,
            SOUTHWEST,
            NORTHWEST,
        ]
        box_mode_shift_arrow_locations = [
            NORTH,
            EAST,
            SOUTH,
            WEST,
        ]
        box_mode_dash_arrow_locations = [
            NORTHEAST,
            SOUTHEAST,
            SOUTHWEST,
            NORTHWEST,
        ]

        if self.arrow.pictograph.grid.grid_mode == DIAMOND:
            if self.motion.motion_type == STATIC:
                self.rotate_diamond_mode_static_arrow(
                    rot_dir, diamond_mode_static_arrow_locations
                )
            elif self.motion.motion_type in [
                PRO,
                ANTI,
                FLOAT,
            ]:
                self.rotate_diamond_mode_shift_arrow(
                    rot_dir, diamond_mode_shift_arrow_locations
                )
            elif self.motion.motion_type in [DASH]:
                self.rotate_diamond_mode_dash_arrow(
                    rot_dir, diamond_mode_dash_arrow_locations
                )
        elif self.arrow.pictograph.grid.grid_mode == BOX:
            if self.motion.motion_type == STATIC:
                self.rotate_box_mode_static_arrow(
                    rot_dir, box_mode_static_arrow_locations
                )
            elif self.motion.motion_type in [
                PRO,
                ANTI,
                FLOAT,
            ]:
                self.rotate_box_mode_shift_arrow(
                    rot_dir, box_mode_shift_arrow_locations
                )
            elif self.motion.motion_type in [DASH]:
                self.rotate_box_mode_dash_arrow(rot_dir, box_mode_dash_arrow_locations)

    def rotate_diamond_mode_dash_arrow(
        self, rot_dir, box_mode_arrow_locations: List[Location]
    ) -> None:
        pass

    def rotate_diamond_mode_dash_arrow(
        self, rot_dir, diamond_mode_arrow_locations: List[Location]
    ) -> None:
        pass

    def rotate_box_mode_dash_arrow(
        self, rot_dir, box_mode_dash_arrow_locations: List[Location]
    ) -> None:
        pass

    def rotate_box_mode_shift_arrow(
        self, rot_dir, box_mode_shift_arrow_locations: List[Location]
    ) -> None:
        current_location_index = box_mode_shift_arrow_locations.index(
            self.arrow.location
        )
        new_location_index = (
            (current_location_index + 1) % 4
            if rot_dir == CLOCKWISE
            else (current_location_index - 1) % 4
        )

        new_arrow_location = box_mode_shift_arrow_locations[new_location_index]
        (
            new_start_loc,
            new_end_loc,
        ) = get_start_end_locs(
            self.arrow.motion_type,
            self.motion.prop_rot_dir,
            new_arrow_location,
        )

        self.arrow.location = new_arrow_location
        self.motion.start_loc = new_start_loc
        self.motion.end_loc = new_end_loc

        self.arrow.location = new_arrow_location
        self.motion.start_loc = new_start_loc
        self.motion.end_loc = new_end_loc
        self.prop.loc = new_end_loc

        self.arrow.update_arrow()
        self.prop.update_prop()
        self.arrow.scene.update_pictograph()

    def rotate_diamond_mode_shift_arrow(
        self, rot_dir, diamond_mode_shift_arrow_locations: List[Location]
    ) -> None:
        current_location_index = diamond_mode_shift_arrow_locations.index(
            self.arrow.location
        )
        new_location_index = (
            (current_location_index + 1) % 4
            if rot_dir == CLOCKWISE
            else (current_location_index - 1) % 4
        )

        new_arrow_location = diamond_mode_shift_arrow_locations[new_location_index]
        (
            new_start_loc,
            new_end_loc,
        ) = get_start_end_locs(
            self.arrow.motion_type,
            self.motion.prop_rot_dir,
            new_arrow_location,
        )

        self.arrow.location = new_arrow_location
        self.arrow.ghost.location = new_arrow_location
        self.motion.start_loc = new_start_loc
        self.motion.end_loc = new_end_loc
        self.prop.loc = new_end_loc

        self.arrow.update_arrow()
        self.arrow.ghost.update_arrow()
        self.prop.update_prop()
        self.arrow.scene.update_pictograph()

    def rotate_box_mode_static_arrow(
        self, rot_dir, box_mode_static_arrow_locations: List[Location]
    ) -> None:
        current_location_index = box_mode_static_arrow_locations.index(
            self.arrow.location
        )
        new_location_index = (
            (current_location_index + 1) % 4
            if rot_dir == CLOCKWISE
            else (current_location_index - 1) % 4
        )
        new_location = box_mode_static_arrow_locations[new_location_index]
        self.arrow.location = new_location
        self.motion.start_loc = new_location
        self.motion.end_loc = new_location
        self.arrow.location = new_location
        self.motion.start_loc = new_location
        self.motion.end_loc = new_location
        self.prop.loc = new_location

        self.motion.update_attr_from_arrow()
        self.prop.update_prop()
        self.arrow.scene.update_pictograph()

    def rotate_diamond_mode_static_arrow(
        self, rot_dir, diamond_mode_locations: List[Location]
    ) -> None:
        current_location_index = diamond_mode_locations.index(self.arrow.location)
        new_location_index = (
            (current_location_index + 1) % 4
            if rot_dir == CLOCKWISE
            else (current_location_index - 1) % 4
        )
        new_location = diamond_mode_locations[new_location_index]
        self.arrow.location = new_location
        self.motion.start_loc = new_location
        self.motion.end_loc = new_location
        self.arrow.location = new_location
        self.motion.start_loc = new_location
        self.motion.end_loc = new_location
        self.prop.loc = new_location

        self.motion.update_attr_from_arrow()
        self.prop.update_prop()
        self.arrow.scene.update_pictograph()

    ### DELETION ###

    def delete(self, keep_prop: bool = False) -> None:
        if self.arrow in self.arrow.scene.arrows.values():
            self.arrow.scene.removeItem(self.arrow)
            self.arrow.scene.removeItem(self.arrow.ghost)
            self.motion.clear_attributes()
            self.prop.clear_attributes()
            self.arrow.ghost.clear_attributes()
            self.prop.clear_attributes()
        if keep_prop:
            self.arrow._change_arrow_to_static()
        else:
            self.arrow.scene.removeItem(self.prop)

        self.arrow.scene.update_pictograph()
