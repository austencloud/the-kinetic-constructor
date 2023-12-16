from typing import List
from PyQt6.QtGui import QTransform
from constants.string_constants import (
    BOX,
    DASH,
    DIAMOND,
    FLOAT,
    MOTION_TYPE,
    TURNS,
    COLOR,
    COUNTER_CLOCKWISE,
    CLOCKWISE,
    PRO,
    ANTI,
    STATIC,
    ROTATION_DIRECTION,
    NORTHEAST,
    SOUTHEAST,
    SOUTHWEST,
    NORTHWEST,
    START_LOCATION,
    END_LOCATION,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    ARROW_LOCATION,
    RED,
    BLUE,
    NORTH,
    SOUTH,
    WEST,
    EAST,
)
from data.start_end_location_map import get_start_end_locations
from utilities.TypeChecking.TypeChecking import (
    Locations,
    RotationDirections,
    Direction,
    TYPE_CHECKING,
)

if TYPE_CHECKING:
    from objects.arrow.arrow import Arrow


class ArrowManipulator:
    def __init__(self, arrow: "Arrow"):
        self.arrow = arrow

    def move_wasd(self, direction: Direction) -> None:
        wasd_location_map = {
            UP: {SOUTHEAST: NORTHEAST, SOUTHWEST: NORTHWEST},
            LEFT: {NORTHEAST: NORTHWEST, SOUTHEAST: SOUTHWEST},
            DOWN: {NORTHEAST: SOUTHEAST, NORTHWEST: SOUTHWEST},
            RIGHT: {NORTHWEST: NORTHEAST, SOUTHWEST: SOUTHEAST},
        }
        current_location = self.arrow.motion.arrow_location
        new_location = wasd_location_map.get(direction, {}).get(
            current_location, current_location
        )
        self.arrow.motion.arrow_location = new_location
        self.arrow.motion.arrow_location = new_location
        (
            new_start_location,
            new_end_location,
        ) = get_start_end_locations(
            self.arrow.motion_type, self.arrow.motion.rotation_direction, new_location
        )

        updated_arrow_dict = {
            COLOR: self.arrow.color,
            MOTION_TYPE: self.arrow.motion_type,
            ARROW_LOCATION: new_location,
            ROTATION_DIRECTION: self.arrow.motion.rotation_direction,
            START_LOCATION: new_start_location,
            END_LOCATION: new_end_location,
            TURNS: self.arrow.turns,
        }

        self.arrow.motion.start_location = new_start_location
        self.arrow.motion.end_location = new_end_location

        self.arrow.update_attributes(updated_arrow_dict)
        self.arrow.prop.prop_location = new_end_location
        self.arrow.prop.update_appearance()
        self.arrow.motion.update_attr_from_arrow()
        self.arrow.scene.update_pictograph()

    def rotate_arrow(self, rotation_direction: RotationDirections) -> None:
        diamond_mode_static_arrow_locations = [NORTH, EAST, SOUTH, WEST]
        diamond_mode_shift_arrow_locations = [
            NORTHEAST,
            SOUTHEAST,
            SOUTHWEST,
            NORTHWEST,
        ]
        diamond_mode_dash_arrow_locations = [NORTH, EAST, SOUTH, WEST]

        box_mode_static_arrow_locations = [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST]
        box_mode_shift_arrow_locations = [NORTH, EAST, SOUTH, WEST]
        box_mode_dash_arrow_locations = [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST]

        if self.arrow.pictograph.grid.grid_mode == DIAMOND:
            if self.arrow.motion.motion_type == STATIC:
                self.rotate_diamond_mode_static_arrow(
                    rotation_direction, diamond_mode_static_arrow_locations
                )
            elif self.arrow.motion.motion_type in [PRO, ANTI, FLOAT]:
                self.rotate_diamond_mode_shift_arrow(
                    rotation_direction, diamond_mode_shift_arrow_locations
                )
            elif self.arrow.motion.motion_type in [DASH]:
                self.rotate_diamond_mode_dash_arrow(
                    rotation_direction, diamond_mode_dash_arrow_locations
                )
        elif self.arrow.pictograph.grid.grid_mode == BOX:
            if self.arrow.motion.motion_type == STATIC:
                self.rotate_box_mode_static_arrow(
                    rotation_direction, box_mode_static_arrow_locations
                )
            elif self.arrow.motion.motion_type in [PRO, ANTI, FLOAT]:
                self.rotate_box_mode_shift_arrow(
                    rotation_direction, box_mode_shift_arrow_locations
                )
            elif self.arrow.motion.motion_type in [DASH]:
                self.rotate_box_mode_dash_arrow(
                    rotation_direction, box_mode_dash_arrow_locations
                )

    def rotate_diamond_mode_dash_arrow(
        self, rotation_direction, box_mode_arrow_locations: List[Locations]
    ) -> None:
        pass

    def rotate_diamond_mode_dash_arrow(
        self, rotation_direction, diamond_mode_arrow_locations: List[Locations]
    ) -> None:
        pass

    def rotate_box_mode_dash_arrow(
        self, rotation_direction, box_mode_dash_arrow_locations: List[Locations]
    ) -> None:
        pass

    def rotate_box_mode_shift_arrow(
        self, rotation_direction, box_mode_shift_arrow_locations: List[Locations]
    ) -> None:
        current_location_index = box_mode_shift_arrow_locations.index(
            self.arrow.motion.arrow_location
        )
        new_location_index = (
            (current_location_index + 1) % 4
            if rotation_direction == CLOCKWISE
            else (current_location_index - 1) % 4
        )

        new_arrow_location = box_mode_shift_arrow_locations[new_location_index]
        (
            new_start_location,
            new_end_location,
        ) = get_start_end_locations(
            self.arrow.motion_type,
            self.arrow.motion.rotation_direction,
            new_arrow_location,
        )

        self.arrow.motion.arrow_location = new_arrow_location
        self.arrow.motion.start_location = new_start_location
        self.arrow.motion.end_location = new_end_location

        self.arrow.motion.arrow_location = new_arrow_location
        self.arrow.motion.start_location = new_start_location
        self.arrow.motion.end_location = new_end_location
        self.arrow.prop.prop_location = new_end_location

        self.arrow.update_appearance()
        self.arrow.prop.update_appearance()
        self.arrow.scene.update_pictograph()

    def rotate_diamond_mode_shift_arrow(
        self, rotation_direction, diamond_mode_shift_arrow_locations: List[Locations]
    ) -> None:
        current_location_index = diamond_mode_shift_arrow_locations.index(
            self.arrow.motion.arrow_location
        )
        new_location_index = (
            (current_location_index + 1) % 4
            if rotation_direction == CLOCKWISE
            else (current_location_index - 1) % 4
        )

        new_arrow_location = diamond_mode_shift_arrow_locations[new_location_index]
        (
            new_start_location,
            new_end_location,
        ) = get_start_end_locations(
            self.arrow.motion_type,
            self.arrow.motion.rotation_direction,
            new_arrow_location,
        )

        self.arrow.motion.arrow_location = new_arrow_location
        self.arrow.motion.start_location = new_start_location
        self.arrow.motion.end_location = new_end_location

        self.arrow.motion.arrow_location = new_arrow_location
        self.arrow.motion.start_location = new_start_location
        self.arrow.motion.end_location = new_end_location
        self.arrow.prop.prop_location = new_end_location

        self.arrow.update_appearance()
        self.arrow.prop.update_appearance()
        self.arrow.scene.update_pictograph()

    def rotate_box_mode_static_arrow(
        self, rotation_direction, box_mode_static_arrow_locations: List[Locations]
    ) -> None:
        current_location_index = box_mode_static_arrow_locations.index(
            self.arrow.motion.arrow_location
        )
        new_location_index = (
            (current_location_index + 1) % 4
            if rotation_direction == CLOCKWISE
            else (current_location_index - 1) % 4
        )
        new_location = box_mode_static_arrow_locations[new_location_index]
        self.arrow.motion.arrow_location = new_location
        self.arrow.motion.start_location = new_location
        self.arrow.motion.end_location = new_location
        self.arrow.motion.arrow_location = new_location
        self.arrow.motion.start_location = new_location
        self.arrow.motion.end_location = new_location
        self.arrow.prop.prop_location = new_location

        self.arrow.motion.update_attr_from_arrow()
        self.arrow.prop.update_appearance()
        self.arrow.scene.update_pictograph()

    def rotate_diamond_mode_static_arrow(
        self, rotation_direction, diamond_mode_locations: List[Locations]
    ) -> None:
        current_location_index = diamond_mode_locations.index(
            self.arrow.motion.arrow_location
        )
        new_location_index = (
            (current_location_index + 1) % 4
            if rotation_direction == CLOCKWISE
            else (current_location_index - 1) % 4
        )
        new_location = diamond_mode_locations[new_location_index]
        self.arrow.motion.arrow_location = new_location
        self.arrow.motion.start_location = new_location
        self.arrow.motion.end_location = new_location
        self.arrow.motion.arrow_location = new_location
        self.arrow.motion.start_location = new_location
        self.arrow.motion.end_location = new_location
        self.arrow.prop.prop_location = new_location

        self.arrow.motion.update_attr_from_arrow()
        self.arrow.prop.update_appearance()
        self.arrow.scene.update_pictograph()

    def swap_color(self) -> None:
        if self.arrow.color == RED:
            new_color = BLUE
        elif self.arrow.color == BLUE:
            new_color = RED

        self.arrow.color = new_color
        self.arrow.update_appearance()

        self.arrow.prop.color = new_color
        self.arrow.prop.update_appearance()

        self.arrow.scene.update_pictograph()

    def swap_rot_dir(self) -> None:
        pass

        if self.arrow.is_svg_mirrored:
            self.unmirror()
        elif not self.arrow.is_svg_mirrored:
            self.mirror()

        if self.arrow.motion.rotation_direction == COUNTER_CLOCKWISE:
            new_rotation_direction = CLOCKWISE
        elif self.arrow.motion.rotation_direction == CLOCKWISE:
            new_rotation_direction = COUNTER_CLOCKWISE
        elif self.arrow.motion.rotation_direction == "None":
            new_rotation_direction = "None"

        old_start_location = self.arrow.motion.start_location
        old_end_location = self.arrow.motion.end_location
        new_start_location = old_end_location
        new_end_location = old_start_location

        svg_file = self.arrow.get_svg_file(self.arrow.motion_type, self.arrow.turns)
        self.arrow.update_svg(svg_file)

        self.arrow.motion.rotation_direction = new_rotation_direction
        self.arrow.motion.start_location = new_start_location
        self.arrow.motion.end_location = new_end_location

        self.arrow.motion.rotation_direction = new_rotation_direction
        self.arrow.motion.start_location = new_start_location
        self.arrow.motion.end_location = new_end_location

        self.arrow.prop.color = self.arrow.color
        self.arrow.prop.prop_location = new_end_location

        self.arrow.update_appearance()
        self.arrow.prop.update_appearance()
        if hasattr(self, "ghost_arrow"):
            if (
                not isinstance(self, self.arrow.motion.ghost_arrow.__class__)
                and self.arrow.motion.ghost_arrow
            ):
                self.arrow.motion.ghost_arrow.is_svg_mirrored = (
                    self.arrow.is_svg_mirrored
                )
                self.arrow.motion.ghost_arrow.update_attributes(self.arrow.arrow_dict)
        self.arrow.scene.update_pictograph()

    def mirror(self) -> None:
        transform = QTransform()
        transform.translate(self.arrow.center_x, self.arrow.center_y)
        transform.scale(-1, 1)
        transform.translate(-self.arrow.center_x, -self.arrow.center_y)
        self.arrow.setTransform(transform)
        if hasattr(self, "ghost_arrow"):
            self.arrow.motion.ghost_arrow.setTransform(transform)
            self.arrow.motion.ghost_arrow.is_svg_mirrored = True
        self.arrow.is_svg_mirrored = True

    def unmirror(self) -> None:
        transform = QTransform()
        transform.translate(self.arrow.center.x(), self.arrow.center.y())
        transform.scale(1, 1)
        transform.translate(-self.arrow.center.x(), -self.arrow.center.y())
        self.arrow.setTransform(transform)
        if hasattr(self, "ghost_arrow"):
            self.arrow.motion.ghost_arrow.setTransform(transform)
            self.arrow.motion.ghost_arrow.is_svg_mirrored = False
        self.arrow.is_svg_mirrored = False

    def swap_motion_type(self) -> None:
        if self.arrow.motion_type == ANTI:
            new_motion_type = PRO
        elif self.arrow.motion_type == PRO:
            new_motion_type = ANTI
        elif self.arrow.motion_type == STATIC:
            new_motion_type = STATIC

        if self.arrow.motion.rotation_direction == COUNTER_CLOCKWISE:
            new_rotation_direction = CLOCKWISE
        elif self.arrow.motion.rotation_direction == CLOCKWISE:
            new_rotation_direction = COUNTER_CLOCKWISE
        elif self.arrow.motion.rotation_direction == "None":
            new_rotation_direction = "None"

        new_arrow_dict = {
            COLOR: self.arrow.color,
            MOTION_TYPE: new_motion_type,
            ARROW_LOCATION: self.arrow.motion.arrow_location,
            ROTATION_DIRECTION: new_rotation_direction,
            START_LOCATION: self.arrow.motion.start_location,
            END_LOCATION: self.arrow.motion.end_location,
            TURNS: self.arrow.turns,
        }

        self.arrow.motion_type = new_motion_type
        self.arrow.motion.motion_type = new_motion_type
        self.arrow.motion.rotation_direction = new_rotation_direction

        self.arrow.prop.orientation = self.arrow.prop.swap_orientation(
            self.arrow.prop.orientation
        )
        self.arrow.motion.end_orientation = self.arrow.prop.orientation

        svg_file = self.arrow.get_svg_file(self.arrow.motion_type, self.arrow.turns)
        self.arrow.update_svg(svg_file)
        self.arrow.update_attributes(new_arrow_dict)
        if hasattr(self, "ghost_arrow"):
            self.arrow.motion.ghost_arrow.motion_type = new_motion_type
            self.arrow.motion.ghost_arrow.update_svg(svg_file)
            self.arrow.motion.ghost_arrow.update_attributes(new_arrow_dict)

        self.arrow.prop.update_appearance()

        self.arrow.scene.update_pictograph()
