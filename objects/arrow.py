from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QTransform, QCursor
from settings.string_constants import (
    MOTION_TYPE,
    TURNS,
    COLOR,
    COUNTER_CLOCKWISE,
    CLOCKWISE,
    PRO,
    ANTI,
    STATIC,
    ROTATION_DIRECTION,
    QUADRANT,
    NORTHEAST,
    SOUTHEAST,
    SOUTHWEST,
    NORTHWEST,
    START_LOCATION,
    END_LOCATION,
    ARROW_ATTRIBUTES,
    ARROW_DIR,
    UP,
    DOWN,
    LEFT,
    RIGHT,
    LOCATION,
    LAYER,
    RED,
    BLUE,
)
from data.start_end_location_mapping import start_end_location_mapping
from objects.graphical_object import GraphicalObject
from objects.staff import Staff

from utilities.TypeChecking.TypeChecking import (
    ArrowAttributesDicts,
    MotionType,
    Color,
    Quadrant,
    RotationDirection,
    Location,
    Turns,
    Direction,
    StartEndLocationTuple,
    RotationAngle,
    TYPE_CHECKING,
    Optional,
    Dict,
)

if TYPE_CHECKING:
    from widgets.graph_editor.graphboard.graphboard import GraphBoard
    from objects.ghosts.ghost_arrow import GhostArrow


class Arrow(GraphicalObject):
    def __init__(
        self, graphboard: "GraphBoard", attributes: "ArrowAttributesDicts"
    ) -> None:
        svg_file = self.get_svg_file(attributes[MOTION_TYPE], attributes[TURNS])
        super().__init__(svg_file, graphboard)
        self.setAcceptHoverEvents(True)
        self._setup_attributes(graphboard, attributes)

    ### SETUP ###

    def _setup_attributes(
        self, graphboard: "GraphBoard", attributes: ArrowAttributesDicts
    ) -> None:
        self.graphboard = graphboard

        self.drag_offset = QPointF(0, 0)
        self.staff: Staff = None

        self.is_mirrored: bool = False

        self.color: Color = None
        self.motion_type: MotionType = None
        self.rotation_direction: RotationDirection = None
        self.quadrant: Quadrant = None
        self.start_location: Location = None
        self.end_location: Location = None
        self.turns: Turns = None

        self.center_x = self.boundingRect().width() / 2
        self.center_y = self.boundingRect().height() / 2

        if attributes:
            self.set_attributes_from_dict(attributes)
            self.update_appearance()
            self.attributes = attributes
            
        self.set_is_mirrored_from_attributes()
        self.update_mirror()
        self.center = self.boundingRect().center()

    def set_is_mirrored_from_attributes(self) -> None:
        if self.motion_type == PRO:
            rotation_direction = self.rotation_direction
            if rotation_direction == CLOCKWISE:
                self.is_mirrored = False
            elif rotation_direction == COUNTER_CLOCKWISE:
                self.is_mirrored = True
        elif self.motion_type == ANTI:
            rotation_direction = self.rotation_direction
            if rotation_direction == CLOCKWISE:
                self.is_mirrored = True
            elif rotation_direction == COUNTER_CLOCKWISE:
                self.is_mirrored = False

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event) -> None:
        self.setSelected(True)
        
        self.update_ghost_on_click()
        self.update_staff_on_click()
        
        self.graphboard.arrows.remove(self)
        self.graphboard.update()
        self.graphboard.arrows.append(self)
        
        for item in self.graphboard.items():
            if item != self:
                item.setSelected(False)

    def update_staff_on_click(self) -> None:
        self.staff.color = self.color
        self.staff.location = self.end_location
        self.staff.axis = self.staff.get_axis(self.end_location)
        self.staff.update_appearance()

    def update_ghost_on_click(self) -> None:
        self.ghost_arrow: "GhostArrow" = self.graphboard.ghost_arrows[self.color]
        self.ghost_arrow.staff = self.staff
        self.ghost_arrow.set_attributes_from_dict(self.attributes)
        if self.ghost_arrow.is_mirrored != self.is_mirrored:
            self.ghost_arrow.swap_rot_dir()
        if self.ghost_arrow.motion_type != self.motion_type:
            self.ghost_arrow.swap_motion_type()
        self.ghost_arrow.set_arrow_attrs_from_arrow(self)
        self.ghost_arrow.update_appearance()
        self.ghost_arrow.transform = self.transform
        self.graphboard.addItem(self.ghost_arrow)
        self.ghost_arrow.staff = self.staff
        self.graphboard.arrows.append(self.ghost_arrow)

    def mouseMoveEvent(self, event) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton:
            new_pos = event.scenePos() - self.center
            self.setPos(new_pos)

            scene_pos = new_pos + self.center
            new_quadrant = self.graphboard.get_quadrant(scene_pos.x(), scene_pos.y())

            if self.quadrant != new_quadrant:
                if new_quadrant:
                    self.update_for_new_quadrant(new_quadrant)

    def mouseReleaseEvent(self, event) -> None:
        self.graphboard.removeItem(self.ghost_arrow)
        self.graphboard.arrows.remove(self.ghost_arrow)
        self.ghost_arrow.staff = None
        self.graphboard.update()

    ### UPDATERS ###

    def update_mirror(self) -> None:
        if self.is_mirrored:
            self.mirror()
        else:
            self.unmirror()
        
    def update_rotation(self) -> None:
        angle = self.get_rotation_angle()
        self.setRotation(angle)

    def update_for_new_quadrant(self, new_quadrant: Quadrant) -> None:
        self.quadrant = new_quadrant

        self.set_start_end_locations()

        self.ghost_arrow.set_arrow_attrs_from_arrow(self)
        self.ghost_arrow.update_appearance()
        
        self.staff.set_staff_attrs_from_arrow(self)
        self.staff.update_appearance()
        
        self.update_appearance()

        self.graphboard.arrows.remove(self)
        for staff in self.graphboard.staffs:
            if staff.color == self.color:
                staff.arrow = self
                self.staff = staff
        self.graphboard.update()
        self.graphboard.arrows.append(self)

    def set_start_end_locations(self) -> None:
        self.start_location, self.end_location = self.get_start_end_locations(
            self.motion_type, self.rotation_direction, self.quadrant
        )

    def set_arrow_attrs_from_arrow(self, target_arrow: "Arrow") -> None:
        self.color = target_arrow.color
        self.motion_type = target_arrow.motion_type
        self.quadrant = target_arrow.quadrant
        self.rotation_direction = target_arrow.rotation_direction
        self.start_location = target_arrow.start_location
        self.end_location = target_arrow.end_location
        self.turns = target_arrow.turns

    def update_staff_during_drag(self) -> None:
        for staff in self.graphboard.staff_set.values():
            if staff.color == self.color:
                if staff not in self.graphboard.staffs:
                    self.graphboard.staffs.append(staff)

                staff.set_attributes_from_dict(
                    {
                        COLOR: self.color,
                        LOCATION: self.end_location,
                        LAYER: 1,
                    }
                )
                staff.arrow = self.ghost_arrow

                if staff not in self.graphboard.items():
                    self.graphboard.addItem(staff)
                staff.show()
                staff.update_appearance()
                self.graphboard.update_staffs()

    def set_arrow_transform_origin_to_center(self) -> None:
        self.center = self.boundingRect().center()
        self.setTransformOriginPoint(self.center)

    ### GETTERS ###

    def get_svg_data(self, svg_file: str) -> bytes:
        with open(svg_file, "r") as f:
            svg_data = f.read()
        return svg_data.encode("utf-8")

    def get_rotation_angle(self, arrow: Optional["Arrow"] = None) -> RotationAngle:
        arrow = arrow or self
        quadrant_to_angle = self.get_quadrant_to_angle_map(
            arrow.motion_type, arrow.rotation_direction
        )
        return quadrant_to_angle.get(arrow.quadrant, 0)

    def get_quadrant_to_angle_map(
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

    def get_start_end_locations(
        self,
        motion_type: MotionType,
        rotation_direction: RotationDirection,
        quadrant: Quadrant,
    ) -> StartEndLocationTuple:
        return (
            start_end_location_mapping.get(quadrant, {})
            .get(rotation_direction, {})
            .get(motion_type, (None, None))
        )

    def get_svg_file(self, motion_type: MotionType, turns: Turns) -> str:
        svg_file = f"{ARROW_DIR}{motion_type}_{turns}.svg"
        return svg_file

    ### MANIPULATION ###

    def add_turn(self) -> None:
        self.turns += 1
        if self.turns > 2:
            self.turns = 0
        svg_file = self.get_svg_file(self.motion_type, self.turns)
        self.update_svg(svg_file)
        self.update_appearance()
        self.attributes[TURNS] = self.turns
        self.graphboard.update()

    def subtract_turn(self) -> None:
        self.turns -= 1
        if self.turns < 0:
            self.turns = 2
        svg_file = self.get_svg_file(self.motion_type, self.turns)
        self.update_svg(svg_file)
        self.update_appearance()
        self.attributes[TURNS] = self.turns
        self.graphboard.update()

    def move_wasd(self, direction: Direction) -> None:
        wasd_quadrant_mapping = {
            UP: {SOUTHEAST: NORTHEAST, SOUTHWEST: NORTHWEST},
            LEFT: {NORTHEAST: NORTHWEST, SOUTHEAST: SOUTHWEST},
            DOWN: {NORTHEAST: SOUTHEAST, NORTHWEST: SOUTHWEST},
            RIGHT: {NORTHWEST: NORTHEAST, SOUTHWEST: SOUTHEAST},
        }
        current_quadrant = self.quadrant
        new_quadrant = wasd_quadrant_mapping.get(direction, {}).get(
            current_quadrant, current_quadrant
        )
        self.quadrant = new_quadrant
        (
            new_start_location,
            new_end_location,
        ) = self.get_start_end_locations(
            self.motion_type, self.rotation_direction, new_quadrant
        )

        updated_arrow_dict = {
            COLOR: self.color,
            MOTION_TYPE: self.motion_type,
            QUADRANT: new_quadrant,
            ROTATION_DIRECTION: self.rotation_direction,
            START_LOCATION: new_start_location,
            END_LOCATION: new_end_location,
            TURNS: self.turns,
        }

        updated_staff_dict = {
            COLOR: self.color,
            LOCATION: new_end_location,
            LAYER: 1,
        }

        self.update(updated_arrow_dict)
        self.staff.update(updated_staff_dict)

        self.graphboard.update()

    def rotate(self, rotation_direction: RotationDirection) -> None:
        quadrants = [NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST]
        current_quadrant_index = quadrants.index(self.quadrant)
        new_quadrant_index = (
            (current_quadrant_index + 1) % 4
            if rotation_direction == RIGHT
            else (current_quadrant_index - 1) % 4
        )
        new_quadrant = quadrants[new_quadrant_index]
        (
            new_start_location,
            new_end_location,
        ) = self.get_start_end_locations(
            self.motion_type, self.rotation_direction, new_quadrant
        )

        updated_arrow_dict = {
            COLOR: self.color,
            MOTION_TYPE: self.motion_type,
            QUADRANT: new_quadrant,
            ROTATION_DIRECTION: self.rotation_direction,
            START_LOCATION: new_start_location,
            END_LOCATION: new_end_location,
            TURNS: self.turns,
        }

        updated_staff_dict = {
            COLOR: self.color,
            LOCATION: new_end_location,
            LAYER: 1,
        }

        self.update(updated_arrow_dict)
        self.staff.update(updated_staff_dict)
        self.graphboard.update()

    def swap_color(self) -> None:
        if self.color == RED:
            new_color = BLUE
        elif self.color == BLUE:
            new_color = RED

        self.color = new_color
        self.update_appearance()

        self.staff.color = new_color
        self.staff.update_appearance()

        self.graphboard.update()

    def swap_rot_dir(self) -> None:
        from objects.ghosts.ghost_arrow import GhostArrow



        if self.is_mirrored:
            self.unmirror()
        elif not self.is_mirrored:
            self.mirror()

        if self.rotation_direction == COUNTER_CLOCKWISE:
            new_rotation_direction = CLOCKWISE
        elif self.rotation_direction == CLOCKWISE:
            new_rotation_direction = COUNTER_CLOCKWISE
        elif self.rotation_direction == "None":
            new_rotation_direction = "None"

        old_start_location = self.start_location
        old_end_location = self.end_location
        new_start_location = old_end_location
        new_end_location = old_start_location

        svg_file = self.get_svg_file(self.motion_type, self.turns)
        self.update_svg(svg_file)

        self.rotation_direction = new_rotation_direction
        self.start_location = new_start_location
        self.end_location = new_end_location

        self.staff.color = self.color
        self.staff.location = new_end_location
        self.staff.layer = 1

        self.update_appearance()
        self.staff.update_appearance()

        if not isinstance(self, GhostArrow) and self.ghost_arrow:
            self.ghost_arrow.is_mirrored = self.is_mirrored
            self.ghost_arrow.update(self.attributes)
        self.graphboard.update()

    def mirror(self) -> None:
        transform = QTransform()
        transform.translate(self.center_x, self.center_y)
        transform.scale(-1, 1)
        transform.translate(-self.center_x, -self.center_y)
        self.setTransform(transform)
        if hasattr(self, 'ghost_arrow'):
            self.ghost_arrow.setTransform(transform)
            self.ghost_arrow.is_mirrored = True
        self.is_mirrored = True

    def unmirror(self) -> None:
        transform = QTransform()
        transform.translate(self.center.x(), self.center.y())
        transform.scale(1, 1)
        transform.translate(-self.center.x(), -self.center.y())
        self.setTransform(transform)
        if hasattr(self, 'ghost_arrow'):
            self.ghost_arrow.setTransform(transform)
            self.ghost_arrow.is_mirrored = False
        self.is_mirrored = False

    def swap_motion_type(self) -> None:
        if self.motion_type == ANTI:
            new_motion_type = PRO
        elif self.motion_type == PRO:
            new_motion_type = ANTI
        elif self.motion_type == STATIC:
            new_motion_type = STATIC

        if self.rotation_direction == COUNTER_CLOCKWISE:
            new_rotation_direction = CLOCKWISE
        elif self.rotation_direction == CLOCKWISE:
            new_rotation_direction = COUNTER_CLOCKWISE
        elif self.rotation_direction == "None":
            new_rotation_direction = "None"

        new_arrow_dict = {
            COLOR: self.color,
            MOTION_TYPE: new_motion_type,
            QUADRANT: self.quadrant,
            ROTATION_DIRECTION: new_rotation_direction,
            START_LOCATION: self.start_location,
            END_LOCATION: self.end_location,
            TURNS: self.turns,
        }

        new_staff_dict = {
            COLOR: self.color,
            LOCATION: self.end_location,
            LAYER: 1,
        }

        self.motion_type = new_motion_type
        svg_file = self.get_svg_file(self.motion_type, self.turns)
        self.update_svg(svg_file)
        self.update(new_arrow_dict)
        self.staff.update(new_staff_dict)
        self.graphboard.update()

    def delete(self, keep_staff: bool = False) -> None:
        self.graphboard.removeItem(self)
        if self in self.graphboard.arrows:
            self.graphboard.arrows.remove(self)
        if keep_staff:
            self.graphboard.create_blank_arrow(self)
        else:
            self.staff.delete()

        self.graphboard.update()


class BlankArrow(Arrow):
    def __init__(self, graphboard, attributes) -> None:
        super().__init__(graphboard, attributes)
        self._disable_interactivity()
        self.hide()

    def _disable_interactivity(self) -> None:
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, False)
