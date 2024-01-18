from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import Qt

from constants import IN

from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING, Dict, Tuple
from objects.arrow.ghost_arrow import GhostArrow

from utilities.TypeChecking.TypeChecking import (
    Colors,
    Locations,
    Locations,
    MotionTypes,
    PropRotDirs,
    Turns,
    RotationAngles,
)
from data.start_end_loc_map import get_start_end_locs
from constants import *
from widgets.graph_editor_tab.graph_editor_object_panel.base_objectbox.base_objectbox_drag import (
    BaseObjectBoxDrag,
)

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget
    from objects.pictograph.pictograph import Pictograph
    from widgets.graph_editor_tab.graph_editor_object_panel.arrowbox.arrowbox import (
        ArrowBox,
    )


class ArrowBoxDrag(BaseObjectBoxDrag):
    def __init__(
        self, main_widget: "MainWidget", pictograph: "Pictograph", arrowbox: "ArrowBox"
    ) -> None:
        super().__init__(main_widget, pictograph, arrowbox)
        self.arrowbox = arrowbox
        self.BaseObjectBox = arrowbox
        self.ghost: GhostArrow = None
        self.start_ori = IN
        self.setup_dependencies(main_widget, pictograph, arrowbox)

    def match_target_arrow(self, target_arrow: "Arrow") -> None:
        self.target_arrow = target_arrow
        self.rot_dir = target_arrow.motion.prop_rot_dir
        self.motion_type = target_arrow.motion_type
        self.color = target_arrow.color
        self.arrow_location = target_arrow.loc
        self.turns = target_arrow.turns
        self.target_arrow_rotation_angle = self._get_arrow_drag_rotation_angle(
            self.target_arrow
        )
        self.is_svg_mirrored = target_arrow.is_svg_mirrored
        super().match_target_object(target_arrow, self.target_arrow_rotation_angle)
        self.set_attributes(target_arrow)
        self.apply_transformations_to_preview()

    def set_attributes(self, target_arrow: "Arrow") -> None:
        self.previous_drag_location = None
        self.color: Colors = target_arrow.color
        self.motion_type: MotionTypes = target_arrow.motion_type
        self.arrow_location: Locations = target_arrow.loc
        self.rot_dir: PropRotDirs = target_arrow.motion.prop_rot_dir

        self.turns: Turns = target_arrow.turns

        self.ghost = self.pictograph.ghost_arrows[self.color]
        self.ghost.target_arrow = target_arrow

    def place_arrow_on_pictograph(self) -> None:
        arrow = self.pictograph.arrows[self.color]
        arrow.update_arrow(self.ghost.get_attributes())
        motion_dict = {
            COLOR: self.color,
            ARROW: arrow,
            PROP: arrow.motion.prop,
            MOTION_TYPE: self.motion_type,
            PROP_ROT_DIR: self.rot_dir,
            TURNS: self.turns,
            START_ORI: self.start_ori,
            START_LOC: self.start_loc,
            END_LOC: self.end_loc,
        }

        self.pictograph.motions[self.color].update_attributes(motion_dict)
        self.pictograph.arrows[self.color] = arrow
        self.pictograph.ghost_arrows[self.color] = self.ghost
        arrow.ghost = self.ghost
        arrow.set_arrow_transform_origin_to_center()
        self.pictograph.clearSelection()
        self.pictograph.arrows[self.color] = arrow
        self.pictograph.arrows[self.color].motion = self.pictograph.motions[self.color]
        arrow.update_arrow()
        arrow.show()
        arrow.setSelected(True)
        self.pictograph.state_updater.update_pictograph()

    ### UPDATERS ###

    def _update_arrow_preview_for_new_location(self, new_location: Locations) -> None:
        self.arrow_location = new_location
        (
            self.start_loc,
            self.end_loc,
        ) = get_start_end_locs(self.motion_type, self.rot_dir, self.arrow_location)

        self.update_drag_pixmap_rotation()
        self._update_ghost_arrow_for_new_location(new_location)
        self.update_prop_during_drag()

        motion_dict = {
            COLOR: self.color,
            ARROW: self,
            PROP: self.ghost.motion.prop,
            MOTION_TYPE: self.motion_type,
            PROP_ROT_DIR: self.rot_dir,
            TURNS: self.turns,
            START_ORI: self.start_ori,
            START_LOC: self.start_loc,
            END_LOC: self.end_loc,
        }
        arrow_dict = {
            COLOR: self.color,
            MOTION_TYPE: self.motion_type,
            LOC: self.pictograph.arrows[
                self.color
            ].arrow_location_manager.get_arrow_location(
                self.start_loc, self.end_loc, self.motion_type
            ),
            TURNS: self.turns,
        }
        self.pictograph.arrows[self.color].update_arrow(arrow_dict)
        self.pictograph.motions[self.color].update_attributes(motion_dict)
        self.pictograph.motions[self.color].arrow = self.pictograph.arrows[self.color]
        self.ghost = self.pictograph.ghost_arrows[self.color]
        self.ghost.loc = new_location
        self.ghost.show()
        self.ghost.update_arrow()

    def _update_ghost_arrow_for_new_location(self, new_location) -> None:
        self.ghost.color = self.color
        self.ghost.motion = self.motion

        self.ghost.motion.arrow.loc = new_location
        self.ghost.motion_type = self.motion_type
        self.ghost.motion.prop_rot_dir = self.rot_dir

        self.ghost.turns = self.turns
        self.ghost.is_svg_mirrored = self.is_svg_mirrored

        if self.is_svg_mirrored:
            mirrored_ghost_transform = (
                QTransform()
                .translate(self.ghost.boundingRect().width(), 0)
                .scale(-1, 1)
            )
            self.ghost.setTransform(mirrored_ghost_transform)

        if self.ghost not in self.pictograph.arrows:
            self.pictograph.ghost_arrows[self.ghost.color] = self.ghost
        if self.ghost not in self.pictograph.items():
            self.pictograph.addItem(self.ghost)
            self.ghost.show()

    ### EVENT HANDLERS ###

    def handle_mouse_move(self, event_pos: QPoint) -> None:
        if self.preview:
            self.move_to_cursor(event_pos)
            if self.is_over_pictograph(event_pos):
                if not self.has_entered_pictograph_once:
                    self.remove_same_color_objects()
                    self.has_entered_pictograph_once = True
                    self.pictograph.motions[self.color].arrow = self

                pos_in_main_window = self.arrowbox.view.mapToGlobal(event_pos)
                view_pos_in_pictograph = self.pictograph.view.mapFromGlobal(
                    pos_in_main_window
                )
                scene_pos = self.pictograph.view.mapToScene(view_pos_in_pictograph)
                new_location = self.pictograph.get_closest_layer2_point(scene_pos)[0]

                if self.previous_drag_location != new_location:
                    self.motion = self.pictograph.motions[self.color]
                    self.pictograph.arrows[self.color].motion = self.motion
                    self.pictograph.arrows[self.color].loc = new_location
                    motion_dict = {
                        COLOR: self.color,
                        ARROW: self.pictograph.arrows[self.color],
                        PROP: self.ghost.motion.prop,
                        MOTION_TYPE: self.motion_type,
                        PROP_ROT_DIR: self.rot_dir,
                        TURNS: self.turns,
                        START_ORI: self.start_ori,
                        START_LOC: self.start_loc,
                        END_LOC: self.end_loc,
                    }

                    self.pictograph.motions[self.color].update_motion(motion_dict)
                    self._update_arrow_preview_for_new_location(new_location)
                    self.previous_drag_location = new_location

    def handle_mouse_release(self) -> None:
        if self.has_entered_pictograph_once:
            self.place_arrow_on_pictograph()
        self.arrowbox.drag = None
        self.deleteLater()
        self.pictograph.state_updater.update_pictograph()
        self.reset_drag_state()

    ### FLAGS ###

    def is_over_pictograph(self, event_pos: QPoint) -> bool:
        pos_in_main_window = self.arrowbox.view.mapToGlobal(event_pos)
        local_pos_in_pictograph = self.pictograph.view.mapFromGlobal(pos_in_main_window)
        return self.pictograph.view.rect().contains(local_pos_in_pictograph)

    ### UPDATERS ###

    def update_prop_during_drag(self) -> None:
        for prop in self.pictograph.props.values():
            if prop.color == self.color:
                if prop not in self.pictograph.props:
                    self.pictograph.props[prop.color] = prop

                prop_dict = {
                    COLOR: self.color,
                    LOC: self.end_loc,
                }

                self.ghost.motion.prop = prop
                self.prop = prop
                prop.motion = self.motion

                if prop not in self.pictograph.items():
                    self.pictograph.addItem(prop)
                prop.update_prop(prop_dict)
                prop.update_prop()

    def apply_transformations_to_preview(self) -> None:
        self.update_mirror()
        self.update_drag_pixmap_rotation()

    def update_mirror(self) -> None:
        if self.is_svg_mirrored:
            transform = QTransform().scale(-1, 1)
            mirrored_pixmap = self.preview.pixmap().transformed(
                transform, Qt.TransformationMode.SmoothTransformation
            )
            self.preview.setPixmap(mirrored_pixmap)
            self.is_svg_mirrored = True

    def update_drag_pixmap_rotation(self) -> None:
        renderer = QSvgRenderer(self.target_arrow.svg_file)
        scaled_size = renderer.defaultSize()
        pixmap = QPixmap(scaled_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        with painter as painter:
            renderer.render(painter)

        angle = self._get_arrow_drag_rotation_angle(self)

        unrotate_transform = QTransform().rotate(-self.target_arrow_rotation_angle)
        unrotated_pixmap = self.preview.pixmap().transformed(unrotate_transform)

        rotate_transform = QTransform().rotate(angle)
        rotated_pixmap = unrotated_pixmap.transformed(rotate_transform)

        self.target_arrow_rotation_angle = angle
        self.preview.setPixmap(rotated_pixmap)

        (
            self.start_loc,
            self.end_loc,
        ) = get_start_end_locs(
            self.motion_type,
            self.rot_dir,
            self.arrow_location,
        )

    def _get_arrow_drag_rotation_angle(
        self, arrow: Arrow | BaseObjectBoxDrag
    ) -> RotationAngles:
        """
        Calculate the rotation angle for the given arrow based on its motion type, rotation direction, color, and location.
        Takes either the target arrow when setting the pixmap, or the drag widget itself when updating rotation.

        Parameters:
        arrow (Arrow): The arrow object for which to calculate the rotation angle.

        Returns:
        RotationAngles: The calculated rotation angle for the arrow.
        """
        motion_type, rot_dir, color, location = (
            arrow.motion_type,
            self.rot_dir,
            arrow.color,
            self.arrow_location,
        )

        rotation_angle_map: Dict[
            Tuple[MotionTypes, Colors],
            Dict[PropRotDirs, Dict[Locations, RotationAngles]],
        ] = {
            (PRO, RED): {
                CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 90,
                    SOUTHWEST: 180,
                    NORTHWEST: 270,
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 90,
                    SOUTHEAST: 180,
                    SOUTHWEST: 270,
                    NORTHWEST: 0,
                },
            },
            (PRO, BLUE): {
                CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 90,
                    SOUTHWEST: 180,
                    NORTHWEST: 270,
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 90,
                    SOUTHEAST: 180,
                    SOUTHWEST: 270,
                    NORTHWEST: 0,
                },
            },
            (ANTI, RED): {
                CLOCKWISE: {
                    NORTHEAST: 90,
                    SOUTHEAST: 180,
                    SOUTHWEST: 270,
                    NORTHWEST: 0,
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 90,
                    SOUTHWEST: 180,
                    NORTHWEST: 270,
                },
            },
            (ANTI, BLUE): {
                CLOCKWISE: {
                    NORTHEAST: 90,
                    SOUTHEAST: 180,
                    SOUTHWEST: 270,
                    NORTHWEST: 0,
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 90,
                    SOUTHWEST: 180,
                    NORTHWEST: 270,
                },
            },
        }

        direction_map: Dict[
            PropRotDirs, Dict[Locations, RotationAngles]
        ] = rotation_angle_map.get((motion_type, color), {})
        location_map: Dict[Locations, RotationAngles] = direction_map.get(rot_dir, {})
        rotation_angle: RotationAngles = location_map.get(location, 0)

        return rotation_angle
