from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer
from objects.prop.prop import Prop
from utilities.TypeChecking.TypeChecking import *
from typing import TYPE_CHECKING
from constants.string_constants import (
    ARROW,
    IN,
    OUT,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    NORTH,
    PROP,
    SOUTH,
    START_LAYER,
    START_ORIENTATION,
    WEST,
    EAST,
    COLOR,
    MOTION_TYPE,
    STATIC,
    ROTATION_DIRECTION,
    START_LOCATION,
    END_LOCATION,
    TURNS,
)
from widgets.graph_editor.object_panel.objectbox_drag import ObjectBoxDrag


if TYPE_CHECKING:
    from main import MainWindow
    from objects.pictograph.pictograph import Pictograph
    from widgets.graph_editor.object_panel.propbox.propbox import PropBox


class PropBoxDrag(ObjectBoxDrag):
    def __init__(
        self, main_window: "MainWindow", pictograph: "Pictograph", propbox: "PropBox"
    ) -> None:
        super().__init__(main_window, pictograph, propbox)
        self.attributes: PropAttributesDicts = {}
        self.propbox = propbox
        self.objectbox = propbox
        self.arrow = None

    def match_target_prop(self, target_prop: "Prop") -> None:
        self.target_prop = target_prop
        self.arrow = target_prop.motion.arrow
        drag_angle = self._get_prop_drag_rotation_angle(target_prop)
        super().match_target_object(target_prop, drag_angle)
        self.set_attributes(target_prop)
        self.move_to_cursor(self.propbox.view.mapFromGlobal(self.pos()))

    def set_attributes(self, target_prop: "Prop") -> None:
        self.color: Colors = target_prop.color
        self.prop_type: PropTypes = target_prop.prop_type
        self.location: Locations = target_prop.location
        self.layer: Layers = target_prop.layer
        self.orientation: Orientations = target_prop.orientation

        self.ghost = self.pictograph.ghost_props[self.color]
        self.ghost.target_prop = target_prop

    def place_prop_on_pictograph(self) -> None:
        self.placed_prop = Prop(
            self.pictograph,
            self.ghost.get_attributes(),
            self.pictograph.motions[self.color],
        )

        self.placed_prop.motion.arrow.location = self.location
        self.placed_prop.motion.start_location = self.location
        self.placed_prop.motion.end_location = self.location

        motion_dict = {
            COLOR: self.color,
            ARROW: self.placed_prop.motion.arrow,
            PROP: self.placed_prop,
            MOTION_TYPE: STATIC,
            ROTATION_DIRECTION: None,
            TURNS: 0,
            START_LOCATION: self.location,
            END_LOCATION: self.location,
            START_ORIENTATION: self.orientation,
            START_LAYER: self.layer,
        }

        self.pictograph.motions[self.color].setup_attributes(motion_dict)
        self.placed_prop.motion.arrow.location = self.location
        self.placed_prop.motion.start_location = self.location
        self.placed_prop.motion.end_location = self.location

        self.pictograph.addItem(self.placed_prop)
        self.pictograph.props[self.color] = self.placed_prop

        self.pictograph.update_pictograph()
        self.pictograph.clearSelection()

        self.placed_prop.update_appearance()
        self.placed_prop.show()
        self.placed_prop.setSelected(True)

    ### UPDATERS ###

    def _update_prop_preview_for_new_location(self, new_location: Locations) -> None:
        self.location = new_location

        self._update_ghost_prop_for_new_location(new_location)
        self._update_static_arrow()

        self.current_rotation_angle = self._get_prop_drag_rotation_angle(self)
        rotated_pixmap = self.create_pixmap_with_rotation(self.current_rotation_angle)

        if self.current_rotation_angle in [90, 270]:
            new_size = QSize(rotated_pixmap.width(), rotated_pixmap.height())
        else:
            new_size = rotated_pixmap.size()

        self.setMinimumSize(new_size)
        self.preview.setMinimumSize(new_size)
        self.preview.setPixmap(rotated_pixmap)
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if self.ghost not in self.pictograph.props:
            self.pictograph.props[self.ghost.color] = self.ghost
        if self.ghost not in self.pictograph.items():
            self.pictograph.addItem(self.ghost)

        motion_dict = {
            COLOR: self.color,
            ARROW: self.arrow,
            PROP: self.ghost,
            MOTION_TYPE: STATIC,
            ROTATION_DIRECTION: None,
            TURNS: 0,
            START_LOCATION: self.location,
            END_LOCATION: self.location,
            START_ORIENTATION: self.orientation,
            START_LAYER: self.layer,
        }

        self.pictograph.motions[self.color].setup_attributes(motion_dict)

        self.pictograph.update_pictograph()
        self.move_to_cursor(self.propbox.view.mapFromGlobal(self.pos()))

    def _update_ghost_prop_for_new_location(self, new_location) -> None:
        self.ghost.prop_type = self.prop_type
        self.ghost.color = self.color
        self.ghost.location = new_location
        self.ghost.orientation = self.orientation
        self.ghost.layer = self.layer
        self.ghost.motion.prop = self.ghost
        self.ghost.motion.arrow.location = self.location
        self.ghost.motion.start_location = self.location

        ghost_svg = self.ghost.get_svg_file(self.prop_type)
        self.ghost.update_svg(ghost_svg)
        self.ghost.update_color()

        self.ghost.motion.update_prop_orientation_and_layer()
        self.ghost.update_rotation()

    ### EVENT HANDLERS ###

    def handle_mouse_move(self, event_pos: QPoint) -> None:
        if self.preview:
            self.move_to_cursor(event_pos)
            if self.is_over_pictograph(event_pos):
                if not self.has_entered_pictograph_once:
                    self.has_entered_pictograph_once = True
                    self.remove_same_color_objects()
                    static_arrow_dict = {
                        COLOR: self.color,
                        MOTION_TYPE: STATIC,
                        TURNS: 0,
                    }
                    self.arrow = self.pictograph.arrows[self.color]
                    self.arrow.update_attributes(static_arrow_dict)
                    motion_dict = {
                        COLOR: self.color,
                        ARROW: self.arrow,
                        PROP: self.ghost,
                        MOTION_TYPE: STATIC,
                        ROTATION_DIRECTION: "None",
                        TURNS: 0,
                        START_LOCATION: self.location,
                        END_LOCATION: self.location,
                        START_ORIENTATION: self.orientation,
                        START_LAYER: self.layer,
                    }
                    self.pictograph.motions[self.color].setup_attributes(motion_dict)
                    self.arrow.motion = self.pictograph.motions[self.color]
                    self.pictograph.motions[self.color].arrow = self.arrow
                pos_in_main_window = self.propbox.view.mapToGlobal(event_pos)
                view_pos_in_pictograph = self.pictograph.view.mapFromGlobal(
                    pos_in_main_window
                )
                scene_pos = self.pictograph.view.mapToScene(view_pos_in_pictograph)
                new_location = self.pictograph.get_closest_hand_point(scene_pos)[0]

                if self.previous_drag_location != new_location and new_location:
                    self.previous_drag_location = new_location
                    self.ghost.motion.arrow.location = new_location
                    self.ghost.motion.start_location = new_location
                    self.ghost.motion.end_location = new_location
                    self._update_prop_preview_for_new_location(new_location)
                    self.ghost.update_attributes(self.attributes)
                    self.pictograph.update_pictograph()

    def handle_mouse_release(self) -> None:
        if self.has_entered_pictograph_once:
            self.place_prop_on_pictograph()
        self.deleteLater()
        self.pictograph.update_pictograph()
        self.propbox.drag = None
        self.reset_drag_state()
        self.previous_drag_location = None

    ### HELPERS ###

    def is_over_pictograph(self, event_pos: QPoint) -> bool:
        pos_in_main_window = self.propbox.view.mapToGlobal(event_pos)
        local_pos_in_pictograph = self.pictograph.view.mapFromGlobal(pos_in_main_window)
        return self.pictograph.view.rect().contains(local_pos_in_pictograph)

    def create_pixmap_with_rotation(self, angle: RotationAngles) -> QPixmap:
        # Generate a new pixmap based on target prop and apply the rotation
        new_svg_data = self.target_prop.set_svg_color(self.color)
        renderer = QSvgRenderer()
        renderer.load(new_svg_data)

        scaled_size = (
            renderer.defaultSize()
            * self.pictograph.graph_editor.pictograph_widget.view_scale
        )
        pixmap = QPixmap(scaled_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)

        renderer.render(painter)
        painter.end()
        rotate_transform = QTransform().rotate(angle)
        rotated_pixmap = pixmap.transformed(rotate_transform)

        return rotated_pixmap

    def _get_prop_drag_rotation_angle(
        self, prop: Prop | ObjectBoxDrag
    ) -> RotationAngles:
        """
        Get the rotation angle for the given prop specifically for use with the PropBoxDrag.

        Args:
            prop (Union[Prop, ObjectBoxDrag]): The prop for which to retrieve the rotation angle.

        Returns:
            RotationAngles: The rotation angle for the prop.

        """
        angle_map: Dict[
            Tuple[Layers, Orientations], Dict[Locations, RotationAngles]
        ] = {
            (1, IN): {NORTH: 90, SOUTH: 270, WEST: 0, EAST: 180},
            (1, OUT): {NORTH: 270, SOUTH: 90, WEST: 180, EAST: 0},
            (2, CLOCKWISE): {NORTH: 0, SOUTH: 180, WEST: 270, EAST: 90},
            (2, COUNTER_CLOCKWISE): {NORTH: 180, SOUTH: 0, WEST: 90, EAST: 270},
        }
        key = (prop.layer, prop.orientation)
        return angle_map.get(key, {}).get(prop.location, 0)

    def _update_static_arrow(self) -> None:
        self.arrow.color = self.color
        self.arrow.location = self.location
        self.arrow.motion.start_location = self.location
        self.arrow.motion.end_location = self.location
        self.arrow.ghost = self.pictograph.ghost_arrows[self.color]
        self.arrow.ghost.motion = self.pictograph.motions[self.color]
        self.arrow.update_appearance()
        self.arrow.ghost.update_attributes(self.arrow.get_attributes())
        self.arrow.ghost.update_svg(
            self.arrow.get_svg_file(
                self.arrow.motion.motion_type, self.arrow.motion.turns
            )
        )
        self.arrow.ghost.update_appearance()
        self.pictograph.arrows[self.color] = self.arrow
        self.pictograph.update_pictograph()
