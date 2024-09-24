# prop_mouse_event_manager.py
from data.start_end_loc_map import get_start_end_locs

from PyQt6.QtWidgets import QGraphicsSceneMouseEvent
from typing import TYPE_CHECKING

from data.constants import *
from Enums.MotionAttributes import Location, MotionType, PropRotDir

if TYPE_CHECKING:
    from objects.prop.prop import Prop


class PropMouseEventHandler:
    def __init__(self, prop: "Prop") -> None:
        self.p = prop





    def update_arrow_location_during_prop_drag(
        self, new_arrow_location: Location
    ) -> None:
        if self.p.motion.motion_type in [PRO, ANTI]:
            shift_location_map: dict[
                tuple[Location, PropRotDir, MotionType],
                dict[Location, Location],
            ] = {
                ### ISO ###
                (NORTHEAST, CLOCKWISE, PRO): {
                    NORTH: NORTHWEST,
                    SOUTH: SOUTHEAST,
                },
                (NORTHWEST, CLOCKWISE, PRO): {
                    EAST: NORTHEAST,
                    WEST: SOUTHWEST,
                },
                (SOUTHWEST, CLOCKWISE, PRO): {
                    NORTH: NORTHWEST,
                    SOUTH: SOUTHEAST,
                },
                (SOUTHEAST, CLOCKWISE, PRO): {
                    WEST: SOUTHWEST,
                    EAST: NORTHEAST,
                },
                (
                    NORTHEAST,
                    COUNTER_CLOCKWISE,
                    PRO,
                ): {
                    WEST: NORTHWEST,
                    EAST: SOUTHEAST,
                },
                (
                    NORTHWEST,
                    COUNTER_CLOCKWISE,
                    PRO,
                ): {
                    SOUTH: SOUTHWEST,
                    NORTH: NORTHEAST,
                },
                (
                    SOUTHWEST,
                    COUNTER_CLOCKWISE,
                    PRO,
                ): {
                    EAST: SOUTHEAST,
                    WEST: NORTHWEST,
                },
                (
                    SOUTHEAST,
                    COUNTER_CLOCKWISE,
                    PRO,
                ): {
                    NORTH: NORTHEAST,
                    SOUTH: SOUTHWEST,
                },
                ### ANTI ###
                (NORTHEAST, CLOCKWISE, ANTI): {
                    EAST: SOUTHEAST,
                    WEST: NORTHWEST,
                },
                (NORTHWEST, CLOCKWISE, ANTI): {
                    NORTH: NORTHEAST,
                    SOUTH: SOUTHWEST,
                },
                (SOUTHWEST, CLOCKWISE, ANTI): {
                    EAST: SOUTHEAST,
                    WEST: NORTHWEST,
                },
                (SOUTHEAST, CLOCKWISE, ANTI): {
                    NORTH: NORTHEAST,
                    SOUTH: SOUTHWEST,
                },
                (
                    NORTHEAST,
                    COUNTER_CLOCKWISE,
                    ANTI,
                ): {
                    NORTH: NORTHWEST,
                    SOUTH: SOUTHEAST,
                },
                (
                    NORTHWEST,
                    COUNTER_CLOCKWISE,
                    ANTI,
                ): {
                    WEST: SOUTHWEST,
                    EAST: NORTHEAST,
                },
                (
                    SOUTHWEST,
                    COUNTER_CLOCKWISE,
                    ANTI,
                ): {
                    SOUTH: SOUTHEAST,
                    NORTH: NORTHWEST,
                },
                (
                    SOUTHEAST,
                    COUNTER_CLOCKWISE,
                    ANTI,
                ): {
                    EAST: NORTHEAST,
                    WEST: SOUTHWEST,
                },
            }

            current_arrow_location = self.p.motion.arrow.loc
            rot_dir = self.p.motion.prop_rot_dir
            motion_type = self.p.motion.motion_type
            new_arrow_location = shift_location_map.get(
                (current_arrow_location, rot_dir, motion_type), {}
            ).get(new_arrow_location)

            if new_arrow_location:
                start_loc, end_loc = get_start_end_locs(
                    motion_type, rot_dir, new_arrow_location
                )

                self.p.motion.arrow.loc = new_arrow_location
                self.p.motion.arrow.ghost.loc = new_arrow_location
                self.p.motion.start_loc = start_loc
                self.p.motion.end_loc = end_loc
                self.p.pictograph.updater.update_pictograph()

        elif self.p.motion.motion_type == STATIC:
            self.p.motion.arrow.loc = new_arrow_location
            self.p.motion.start_loc = new_arrow_location
            self.p.motion.end_loc = new_arrow_location
            self.p.motion.arrow.updater.update_arrow()

    def finalize_prop_drop(self, event: "QGraphicsSceneMouseEvent") -> None:
        (
            closest_hand_point,
            closest_hand_point_coord,
        ) = self.p.pictograph.grid.get_closest_hand_point(event.scenePos())

        self.loc = closest_hand_point
        self.axis = self.p.attr_manager.get_axis_from_ori()
        self.p.updater.update_prop()
        self.p.setPos(closest_hand_point_coord)

        if self.p.motion.arrow:
            self.p.motion.arrow.updater.update_arrow()
        self.p.previous_location = closest_hand_point
        self.p.scene.updater.update_pictograph()

