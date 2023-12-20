from typing import Union
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtWidgets import QGraphicsSceneMouseEvent
from objects.arrow.arrow_manipulator import ArrowManipulator
from objects.grid import GridItem
from objects.prop.prop import Prop
from constants.string_constants import (
    END_LOCATION,
    MOTION_TYPE,
    ROTATION_DIRECTION,
    START_LOCATION,
    TURNS,
    COLOR,
    COUNTER_CLOCKWISE,
    CLOCKWISE,
    PRO,
    ANTI,
    STATIC,
    NORTHEAST,
    SOUTHEAST,
    SOUTHWEST,
    NORTHWEST,
    ARROW_ATTRIBUTES,
    ARROW_DIR,
    ARROW_LOCATION,
    LOCATION,
    LAYER,
)
from objects.graphical_object import GraphicalObject
from data.start_end_location_map import get_start_end_locations
from utilities.TypeChecking.TypeChecking import (
    ArrowAttributesDicts,
    MotionTypes,
    Locations,
    RotationDirections,
    Turns,
    RotationAngles,
    TYPE_CHECKING,
    Optional,
    Dict,
)

if TYPE_CHECKING:
    from objects.motion import Motion
    from objects.pictograph.pictograph import Pictograph
    from objects.ghosts.ghost_arrow import GhostArrow
    from objects.prop.prop import Prop
    from widgets.graph_editor_tab.object_panel.arrowbox.arrowbox import ArrowBox


class Arrow(GraphicalObject):
    def __init__(self, scene, arrow_dict, motion) -> None:
        super().__init__(scene)
        self.svg_file = self.get_svg_file(arrow_dict[MOTION_TYPE], arrow_dict[TURNS])
        self.motion: Motion = motion
        self.setup_svg_renderer(self.svg_file)
        self.setAcceptHoverEvents(True)
        self._setup_attributes(scene, arrow_dict)

    ### SETUP ###

    def _setup_attributes(self, scene, arrow_dict: "ArrowAttributesDicts") -> None:
        self.scene: Pictograph | ArrowBox = scene
        self.manipulator = ArrowManipulator(self)
        self.drag_offset = QPointF(0, 0)
        self.is_svg_mirrored: bool = False
        self.is_dragging: bool = False
        self.ghost: GhostArrow = None
        self.location: Locations = None
        self.turns: Turns = arrow_dict[TURNS]
        self.center_x = self.boundingRect().width() / 2
        self.center_y = self.boundingRect().height() / 2

        if arrow_dict:
            self.update_attributes(arrow_dict)
            self.arrow_dict = arrow_dict
        if self.motion:
            self.set_is_svg_mirrored_from_attributes()
            self.update_mirror()
            self.center = self.boundingRect().center()

    def set_is_svg_mirrored_from_attributes(self) -> None:
        if self.motion_type == PRO:
            rotation_direction = self.motion.rotation_direction
            if rotation_direction == CLOCKWISE:
                self.is_svg_mirrored = False
            elif rotation_direction == COUNTER_CLOCKWISE:
                self.is_svg_mirrored = True
        elif self.motion_type == ANTI:
            rotation_direction = self.motion.rotation_direction
            if rotation_direction == CLOCKWISE:
                self.is_svg_mirrored = True
            elif rotation_direction == COUNTER_CLOCKWISE:
                self.is_svg_mirrored = False

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        self.setSelected(True)
        self.ghost.update_appearance()
        self.ghost.show()
        if hasattr(self.motion, "ghost_arrow"):
            if self.ghost:
                self._update_ghost_on_click()
                self.ghost.setTransform(self.transform())
                print("Transformation attributes:")
                print("Translation:", self.transform().dx(), self.transform().dy())

        if hasattr(self.motion, "prop"):
            if self.motion.prop:
                self._update_prop_on_click()

        self.scene.update_pictograph()

        for item in self.scene.items():
            if item != self and not isinstance(item, GridItem):
                item.setSelected(False)
        if self.scene:
            self.scene.update_attr_panel()

    def mouseMoveEvent(
        self: Union["Prop", "Arrow"], event: "QGraphicsSceneMouseEvent"
    ) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_location = self.scene.get_closest_layer2_point(event.scenePos())[0]
            new_pos = event.scenePos() - self.get_object_center()
            self.set_drag_pos(new_pos)
            if new_location != self.location:
                self.update_ghost_arrow_location(event.scenePos())

    def mouseReleaseEvent(self, event) -> None:
        self.is_dragging = False
        self.scene.arrows[self.color] = self
        self.scene.update_pictograph()
        self.ghost.hide()

    ### UPDATERS ###

    def _update_prop_on_click(self) -> None:
        self.motion.prop.color = self.color
        self.motion.prop.location = self.motion.end_location
        self.motion.prop.axis = self.motion.prop.update_axis_from_layer(
            self.motion.end_location
        )

    def _update_ghost_on_click(self) -> None:
        from objects.pictograph.pictograph import Pictograph

        if isinstance(self.scene, Pictograph):
            self.ghost: "GhostArrow" = self.scene.ghost_arrows[self.color]
            self.ghost.update_attributes(self.arrow_dict)
            self.ghost.set_arrow_attrs_from_arrow(self)
            self.ghost.set_is_svg_mirrored_from_attributes()
            self.ghost.update_appearance()
            self.ghost.transform = self.transform
            self.scene.addItem(self.ghost)
            self.scene.ghost_arrows[self.ghost.color] = self.ghost

    def update_ghost_arrow_location(self, new_pos: QPointF) -> None:
        new_location = self.scene.get_closest_layer2_point(new_pos)[0]
        self.motion.arrow.location = new_location
        self.set_start_end_locations()
        if hasattr(self, "ghost_arrow"):
            self.ghost.set_arrow_attrs_from_arrow(self)
            self.ghost.update_appearance()

        self.motion.prop.set_prop_attrs_from_arrow(self)
        self.motion.prop.update_appearance()
        self.motion.arrow.location = new_location
        self.ghost.location = new_location
        self.update_appearance()
        self.ghost.update_appearance()
        self.scene.ghost_arrows[self.color] = self.ghost
        self.scene.props[self.color] = self.motion.prop
        self.is_dragging = True
        self.scene.update_pictograph()

    def set_drag_pos(self, new_pos: QPointF) -> None:
        self.setPos(new_pos)

    def update_mirror(self) -> None:
        if self.is_svg_mirrored:
            self.manipulator.mirror()
        else:
            self.manipulator.unmirror()

    def update_rotation(self) -> None:
        angle = self.get_arrow_rotation_angle()
        self.setRotation(angle)

    def set_start_end_locations(self) -> None:
        (
            self.motion.start_location,
            self.motion.end_location,
        ) = get_start_end_locations(
            self.motion_type, self.motion.rotation_direction, self.motion.arrow.location
        )
        self.motion.start_location = self.motion.start_location
        self.motion.end_location = self.motion.end_location

    def set_arrow_attrs_from_arrow(self, target_arrow: "Arrow") -> None:
        self.color = target_arrow.color
        self.motion.color = target_arrow.color
        self.motion_type: MotionTypes = target_arrow.motion_type
        self.motion.arrow.location = target_arrow.location
        self.motion.rotation_direction: RotationDirections = (
            target_arrow.motion.rotation_direction
        )
        self.motion.start_location: Locations = target_arrow.motion.start_location
        self.motion.end_location: Locations = target_arrow.motion.end_location
        self.motion.turns: Turns = target_arrow.motion.turns

    def update_prop_during_drag(self) -> None:
        for prop in self.scene.props.values():
            if prop.color == self.color:
                if prop not in self.scene.props:
                    self.scene.props[prop.color] = prop

                prop.update_attributes(
                    {
                        COLOR: self.color,
                        LOCATION: self.motion.end_location,
                        LAYER: 1,
                    }
                )

                if prop not in self.scene.items():
                    self.scene.addItem(prop)
                prop.show()
                prop.update_appearance()
                self.scene.update_pictograph()

    def set_arrow_transform_origin_to_center(self) -> None:
        self.center = self.boundingRect().center()
        self.setTransformOriginPoint(self.center)

    def clear_attributes(self) -> None:
        self.motion_type = None
        self.location = None
        self.turns = None
        self.motion = None

    ### GETTERS ###

    def get_svg_data(self, svg_file: str) -> bytes:
        with open(svg_file, "r") as f:
            svg_data = f.read()
        return svg_data.encode("utf-8")

    def get_arrow_rotation_angle(
        self, arrow: Optional["Arrow"] = None
    ) -> RotationAngles:
        arrow = arrow or self
        location_to_angle = self.get_location_to_angle_map(
            arrow.motion.motion_type, arrow.motion.rotation_direction
        )
        return location_to_angle.get(self.location, 0)

    def get_location_to_angle_map(
        self, motion_type: str, rotation_direction: str
    ) -> Dict[str, Dict[str, int]]:
        if motion_type == PRO:
            return {
                CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 90,
                    SOUTHWEST: 180,
                    NORTHWEST: 270,
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 270,
                    SOUTHEAST: 180,
                    SOUTHWEST: 90,
                    NORTHWEST: 0,
                },
            }.get(rotation_direction, {})
        elif motion_type == ANTI:
            return {
                CLOCKWISE: {
                    NORTHEAST: 270,
                    SOUTHEAST: 180,
                    SOUTHWEST: 90,
                    NORTHWEST: 0,
                },
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 90,
                    SOUTHWEST: 180,
                    NORTHWEST: 270,
                },
            }.get(rotation_direction, {})
        elif motion_type == STATIC:
            return {
                CLOCKWISE: {NORTHEAST: 0, SOUTHEAST: 0, SOUTHWEST: 0, NORTHWEST: 0},
                COUNTER_CLOCKWISE: {
                    NORTHEAST: 0,
                    SOUTHEAST: 0,
                    SOUTHWEST: 0,
                    NORTHWEST: 0,
                },
            }.get(rotation_direction, {})

    def get_attributes(self) -> ArrowAttributesDicts:
        return {attr: getattr(self, attr) for attr in ARROW_ATTRIBUTES}

    def get_svg_file(self, motion_type: MotionTypes, turns: Turns) -> str:
        svg_file = f"{ARROW_DIR}{self.pictograph.grid.grid_mode}/{motion_type}/{motion_type}_{float(turns)}.svg"
        return svg_file

    def _change_arrow_to_static(self) -> None:
        static_arrow_dict = {
            COLOR: self.color,
            MOTION_TYPE: STATIC,
            TURNS: 0,
        }

        self.update_attributes(static_arrow_dict)
        self.motion[COLOR] = self.color
        self.motion[MOTION_TYPE] = STATIC
        self.motion[TURNS] = 0
        self.motion[ROTATION_DIRECTION] = None
        self.motion[START_LOCATION] = self.motion.prop.location
        self.motion[END_LOCATION] = self.motion.prop.location
        self.motion[ARROW_LOCATION] = self.motion.prop.location
