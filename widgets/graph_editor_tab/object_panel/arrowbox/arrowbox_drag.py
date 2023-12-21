from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtCore import Qt
from constants.string_constants import (
    ANTI,
    ARROW,
    BLUE,
    CLOCKWISE,
    COLOR,
    COUNTER_CLOCKWISE,
    IN,
    LAYER,
    NORTHEAST,
    NORTHWEST,
    PRO,
    PROP,
    LOCATION,
    RED,
    SOUTHEAST,
    SOUTHWEST,
    MOTION_TYPE,
    ROTATION_DIRECTION,
    START_LOCATION,
    END_LOCATION,
    TURNS,
    START_ORIENTATION,
    START_LAYER,
)
from objects.arrow.arrow import Arrow
from typing import TYPE_CHECKING, Dict, Tuple
from objects.ghosts.ghost_arrow import GhostArrow

from widgets.graph_editor_tab.object_panel.objectbox_drag import ObjectBoxDrag
from utilities.TypeChecking.TypeChecking import (
    Colors,
    MotionTypes,
    Locations,
    RotationDirections,
    Locations,
    Turns,
    RotationAngles,
)
from data.start_end_location_map import get_start_end_locations

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from objects.pictograph.pictograph import Pictograph
    from widgets.graph_editor_tab.object_panel.arrowbox.arrowbox import ArrowBox


class ArrowBoxDrag(ObjectBoxDrag):
    def __init__(
        self, main_widget: "MainWidget", pictograph: "Pictograph", arrowbox: "ArrowBox"
    ) -> None:
        super().__init__(main_widget, pictograph, arrowbox)
        self.arrowbox = arrowbox
        self.objectbox = arrowbox
        self.ghost: GhostArrow = None
        self.start_orientation = IN
        self.setup_dependencies(main_widget, pictograph, arrowbox)

    def match_target_arrow(self, target_arrow: "Arrow") -> None:
        self.target_arrow = target_arrow
        self.rotation_direction = target_arrow.motion.rotation_direction
        self.motion_type = target_arrow.motion_type
        self.color = target_arrow.color
        self.arrow_location = target_arrow.location
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
        self.arrow_location: Locations = target_arrow.location
        self.rotation_direction: RotationDirections = (
            target_arrow.motion.rotation_direction
        )

        self.turns: Turns = target_arrow.turns

        self.ghost = self.pictograph.ghost_arrows[self.color]
        self.ghost.target_arrow = target_arrow

    def place_arrow_on_pictograph(self) -> None:
        self.placed_arrow = Arrow(
            self.pictograph,
            self.ghost.get_attributes(),
            self.pictograph.motions[self.color],
        )
        self.placed_arrow.motion.prop = self.pictograph.props[self.color]

        motion_dict = {
            COLOR: self.color,
            ARROW: self.placed_arrow,
            PROP: self.placed_arrow.motion.prop,
            MOTION_TYPE: self.motion_type,
            ROTATION_DIRECTION: self.rotation_direction,
            TURNS: self.turns,
            START_ORIENTATION: self.start_orientation,
            START_LAYER: 1,
            START_LOCATION: self.start_location,
            END_LOCATION: self.end_location,
        }

        self.pictograph.motions[self.color].setup_attributes(motion_dict)
        self.pictograph.arrows[self.color] = self.placed_arrow
        self.pictograph.ghost_arrows[self.color] = self.ghost

        self.placed_arrow.ghost = self.ghost

        self.placed_arrow.set_arrow_transform_origin_to_center()
        self.pictograph.addItem(self.placed_arrow)
        self.pictograph.clearSelection()
        self.pictograph.arrows[self.color] = self.placed_arrow
        self.pictograph.arrows[self.color].motion = self.pictograph.motions[self.color]
        self.placed_arrow.update_appearance()
        self.placed_arrow.show()
        self.placed_arrow.setSelected(True)

    ### UPDATERS ###

    def _update_arrow_preview_for_new_location(self, new_location: Locations) -> None:
        self.arrow_location = new_location
        (
            self.start_location,
            self.end_location,
        ) = get_start_end_locations(
            self.motion_type, self.rotation_direction, self.arrow_location
        )

        self.update_rotation()
        self._update_ghost_arrow_for_new_location(new_location)
        self.update_prop_during_drag()

        motion_dict = {
            COLOR: self.color,
            ARROW: self,
            PROP: self.ghost.motion.prop,
            MOTION_TYPE: self.motion_type,
            ROTATION_DIRECTION: self.rotation_direction,
            TURNS: self.turns,
            START_LOCATION: self.start_location,
            END_LOCATION: self.end_location,
            START_ORIENTATION: self.start_orientation,
            START_LAYER: 1,
        }

        self.pictograph.motions[self.color].setup_attributes(motion_dict)
        self.pictograph.motions[self.color].arrow = self.pictograph.arrows[self.color]
        self.finalize_ghost_arrow_for_new_location(new_location)
        self.pictograph.update_pictograph()

    def finalize_ghost_arrow_for_new_location(self, new_location):
        self.ghost = self.pictograph.ghost_arrows[self.color]
        self.ghost.location = new_location
        self.ghost.set_arrow_transform_origin_to_center()
        self.ghost.show()
        self.ghost.update_color()
        self.ghost.update_appearance()

    def _update_ghost_arrow_for_new_location(self, new_location) -> None:
        self.ghost.color = self.color
        self.ghost.motion = self.motion

        self.ghost.motion.arrow.location = new_location
        self.ghost.motion_type = self.motion_type
        self.ghost.motion.rotation_direction = self.rotation_direction

        self.ghost.turns = self.turns
        self.ghost.is_svg_mirrored = self.is_svg_mirrored

        ghost_svg = self.ghost.get_svg_file(self.motion_type, self.turns)

        self.ghost.update_mirror()
        self.ghost.update_svg(ghost_svg)
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
                    self.pictograph.arrows[self.color].location = new_location
                    self.pictograph.arrows[
                        self.color
                    ].set_is_svg_mirrored_from_attributes()
                    self._update_arrow_preview_for_new_location(new_location)
                    self.previous_drag_location = new_location

    def handle_mouse_release(self) -> None:
        if self.has_entered_pictograph_once:
            self.place_arrow_on_pictograph()
        self.arrowbox.drag = None
        self.deleteLater()
        self.pictograph.update_pictograph()
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
                    LOCATION: self.end_location,
                    LAYER: 1,
                }
                prop.update_attributes(prop_dict)
                prop.ghost = self.pictograph.ghost_props[self.color]
                prop.ghost.update_attributes(prop_dict)

                self.ghost.motion.prop = prop
                self.motion.prop = prop
                prop.motion = self.motion

                if prop not in self.pictograph.items():
                    self.pictograph.addItem(prop)
                prop.update_appearance()
                self.pictograph.update_props()

    def apply_transformations_to_preview(self) -> None:
        self.update_mirror()
        self.update_rotation()

    def update_mirror(self) -> None:
        if self.is_svg_mirrored:
            transform = QTransform().scale(-1, 1)
            mirrored_pixmap = self.preview.pixmap().transformed(
                transform, Qt.TransformationMode.SmoothTransformation
            )
            self.preview.setPixmap(mirrored_pixmap)
            self.is_svg_mirrored = True

    def update_rotation(self) -> None:
        renderer = QSvgRenderer(self.target_arrow.svg_file)
        scaled_size = (
            renderer.defaultSize()
            * self.main_widget.graph_editor_tab.graph_editor.main_pictograph.view_scale
        )
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
            self.start_location,
            self.end_location,
        ) = get_start_end_locations(
            self.motion_type,
            self.rotation_direction,
            self.arrow_location,
        )

    def _get_arrow_drag_rotation_angle(
        self, arrow: Arrow | ObjectBoxDrag
    ) -> RotationAngles:
        """
        Calculate the rotation angle for the given arrow based on its motion type, rotation direction, color, and location.
        Takes either the target arrow when setting the pixmap, or the drag widget itself when updating rotation.

        Parameters:
        arrow (Arrow): The arrow object for which to calculate the rotation angle.

        Returns:
        RotationAngles: The calculated rotation angle for the arrow.
        """
        motion_type, rotation_direction, color, location = (
            arrow.motion_type,
            self.rotation_direction,
            arrow.color,
            self.arrow_location,
        )

        rotation_angle_map: Dict[
            Tuple[MotionTypes, Colors],
            Dict[RotationDirections, Dict[Locations, RotationAngles]],
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
            RotationDirections, Dict[Locations, RotationAngles]
        ] = rotation_angle_map.get((motion_type, color), {})
        location_map: Dict[Locations, RotationAngles] = direction_map.get(
            rotation_direction, {}
        )
        rotation_angle: RotationAngles = location_map.get(location, 0)

        return rotation_angle
