# prop_mouse_event_manager.py
from data.start_end_loc_map import get_start_end_locs

from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent
from typing import TYPE_CHECKING, Dict, Tuple

from constants import *
from utilities.TypeChecking.MotionAttributes import Locations, MotionTypes, PropRotDirs

if TYPE_CHECKING:
    from objects.prop.prop import Prop


class PropMouseEventHandler:
    def __init__(self, prop: "Prop") -> None:
        self.p = prop

    def handle_mouse_press(self) -> None:
        self.p.setSelected(True)
        if isinstance(self.p.scene, self.p.scene.__class__):
            if not self.p.ghost:
                self.p.ghost = self.p.scene.ghost_props[self.p.color]
            self.p.ghost.color = self.p.color
            self.p.ghost.loc = self.p.loc
            self.p.ghost.ori = self.p.ori
            self.p.ghost.updater.update_prop()
            self.p.ghost.show()
            self.p.scene.props[self.p.ghost.color] = self.p.ghost
            self.p.scene.props[self.p.color] = self.p.ghost
            self.p.scene.state_updater.update_pictograph()
            self.p.scene.props[self.p.color] = self.p
            for item in self.p.scene.items():
                if item != self.p:
                    item.setSelected(False)
            self.p.previous_location = self.p.loc

    def handle_mouse_move(self, event: QGraphicsSceneMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = event.scenePos() - self.p.get_center()
            self.set_drag_pos(new_pos)
            self.update_ghost_prop_location_during_drag(event.scenePos())
            self.update_arrow_location_during_prop_drag(self.p.loc)

    def handle_mouse_release(self, event: QGraphicsSceneMouseEvent) -> None:
        if isinstance(self.p.scene, self.p.scene.__class__):
            self.p.ghost.hide()
            self.p.scene.state_updater.update_pictograph()
            self.finalize_prop_drop(event)

    def update_ghost_prop_location_during_drag(self, new_pos: QPointF) -> None:
        new_location = self.p.pictograph.grid.get_closest_hand_point(new_pos)[0][0]

        if new_location != self.p.previous_location:
            self.p.loc = new_location

            if self.p.motion.motion_type == STATIC:
                self.p.motion.arrow.loc = new_location
                self.p.motion.start_loc = new_location
                self.p.motion.end_loc = new_location

            self.p.axis = self.p.attr_manager.get_axis_from_ori()
            self.p.updater.update_prop()
            self.update_arrow_location_during_prop_drag(new_location)

            self.p.ghost.color = self.p.color
            self.p.ghost.loc = self.p.loc
            self.p.ghost.updater.update_prop()
            self.p.scene.props[self.p.ghost.color] = self.p.ghost
            self.p.scene.state_updater.update_pictograph()
            self.p.scene.props[self.p.color] = self.p
            new_pos = new_pos - self.p.get_center()
            self.set_drag_pos(new_pos)
            self.p.previous_location = new_location

    def update_arrow_location_during_prop_drag(
        self, new_arrow_location: Locations
    ) -> None:
        if self.p.motion.motion_type in [PRO, ANTI]:
            shift_location_map: Dict[
                Tuple(Locations, PropRotDirs, MotionTypes),
                Dict[Locations, Locations],
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
                self.p.pictograph.state_updater.update_pictograph()

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
        self.p.scene.state_updater.update_pictograph()

    def set_drag_pos(self, new_pos: QPointF) -> None:
        object_length = self.p.boundingRect().width()
        object_width = self.p.boundingRect().height()

        offset = self.p.offest_calculator.get_offset(object_length, object_width)

        self.p.setPos(new_pos + offset)
