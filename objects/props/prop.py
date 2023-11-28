from objects.graphical_object import GraphicalObject
from PyQt6.QtCore import Qt, QPointF
from settings.string_constants import (
    ORIENTATION,
    OUT,
    COLOR,
    LOCATION,
    LAYER,
    NORTH,
    PROP_DIR,
    PROP_TYPE,
    SOUTH,
    WEST,
    EAST,
    HORIZONTAL,
    VERTICAL,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    NORTHEAST,
    NORTHWEST,
    SOUTHEAST,
    SOUTHWEST,
    PRO,
    ANTI,
    STATIC,
    COLOR_MAP,
    IN,
)
import re

from PyQt6.QtWidgets import QGraphicsSceneMouseEvent
from utilities.TypeChecking.TypeChecking import (
    Layer,
    Orientation,
    PropType,
    RotationAngle,
    PropAttributesDicts,
    Location,
    Quadrant,
    RotationDirection,
    MotionType,
    Axis,
    Color,
    TYPE_CHECKING,
    Dict,
    Tuple,
    ColorHex,
)

if TYPE_CHECKING:
    from objects.arrow import Arrow
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from objects.motion import Motion

class Prop(GraphicalObject):
    def __init__(self, pictograph, attributes: Dict) -> None:
        svg_file = self.get_svg_file(attributes[PROP_TYPE])
        super().__init__(svg_file, pictograph)
        self._setup_attributes(pictograph, attributes)
        self.update_appearance()

    def _setup_attributes(
        self, pictograph: 'Pictograph', attributes: 'PropAttributesDicts'
    ) -> None:
        self.pictograph = pictograph
        self.motion: Motion = None
        self.prop_type = None
        
        self.drag_offset = QPointF(0, 0)
        self.previous_location = None
        self.arrow: Arrow = None
        self.ghost_prop: Prop = None

        self.color = attributes[COLOR]
        self.location = attributes[LOCATION]
        self.layer = attributes[LAYER]
        self.orientation = attributes[ORIENTATION]

        self.axis = self.get_axis(self.location)
        self.center = self.boundingRect().center()
        self.update_rotation()

        if attributes:
            self.update_attributes(attributes)

    ### MOUSE EVENTS ###

    def mousePressEvent(self, event) -> None:
        self.setSelected(True)
        if isinstance(self.scene(), self.pictograph.__class__):
            if not self.ghost_prop:
                self.ghost_prop = self.pictograph.ghost_props[self.color]
            self.ghost_prop.color = self.color
            self.ghost_prop.location = self.location
            self.ghost_prop.layer = self.layer
            self.ghost_prop.orientation = self.orientation
            self.ghost_prop.update_appearance()
            self.pictograph.addItem(self.ghost_prop)
            self.ghost_prop.arrow = self.arrow
            self.pictograph.props.append(self.ghost_prop)
            self.pictograph.props.remove(self)
            self.pictograph.update()
            self.pictograph.props.append(self)
            for item in self.pictograph.items():
                if item != self:
                    item.setSelected(False)
            self.previous_location = self.location

    def mouseMoveEvent(self, event) -> None:
        if isinstance(self.scene(), self.pictograph.__class__):
            if event.buttons() == Qt.MouseButton.LeftButton:
                new_pos = event.scenePos() - self.get_prop_center()
                self.set_drag_pos(new_pos)
                self.update_location(event.scenePos())

    def update_location(self, new_pos: QPointF) -> None:
        new_location = self.get_closest_location(new_pos)

        if new_location != self.previous_location:
            self.location = new_location
            self.axis = self.get_axis(self.location)
            self.update_appearance()
            self.update_arrow_quadrant(new_location)

            self.ghost_prop.color = self.color
            self.ghost_prop.location = self.location
            self.ghost_prop.layer = self.layer
            self.ghost_prop.update_appearance()

            self.pictograph.props.remove(self)
            if self.arrow.motion_type == STATIC:
                self.arrow.start_location = new_location
                self.arrow.end_location = new_location

            self.pictograph.update()
            self.pictograph.props.append(self)
            new_pos = new_pos - self.get_prop_center()
            self.set_drag_pos(new_pos)
            self.previous_location = new_location

    def set_drag_pos(self, new_pos: QPointF) -> None:
        staff_length = self.boundingRect().width()
        staff_width = self.boundingRect().height()

        self.setTransformOriginPoint(0, 0)
        if self.layer == 1:
            if self.orientation == IN:
                if self.location == WEST:
                    self.setPos(new_pos)
                elif self.location == EAST:
                    self.setPos(new_pos + QPointF(staff_length, staff_width))
                elif self.location == NORTH:
                    self.setPos(new_pos + QPointF(staff_width, 0))
                elif self.location == SOUTH:
                    self.setPos(new_pos + QPointF(0, staff_length))
            elif self.orientation == OUT:
                if self.location == WEST:
                    self.setPos(new_pos + QPointF(staff_length, staff_width))
                elif self.location == EAST:
                    self.setPos(new_pos + QPointF(0, 0))
                elif self.location == NORTH:
                    self.setPos(new_pos + QPointF(0, staff_length))
                elif self.location == SOUTH:
                    self.setPos(new_pos + QPointF(staff_width, 0))
        elif self.layer == 2:
            if self.orientation == CLOCKWISE:
                if self.location == WEST:
                    self.setPos(new_pos + QPointF(0, staff_length))
                elif self.location == EAST:
                    self.setPos(new_pos + QPointF(staff_width, 0))
                elif self.location == NORTH:
                    self.setPos(new_pos)
                elif self.location == SOUTH:
                    self.setPos(new_pos + QPointF(staff_length, staff_width))
            elif self.orientation == COUNTER_CLOCKWISE:
                if self.location == WEST:
                    self.setPos(new_pos + QPointF(staff_width, 0))
                elif self.location == EAST:
                    self.setPos(new_pos + QPointF(0, staff_length))
                elif self.location == NORTH:
                    self.setPos(new_pos + QPointF(staff_length, staff_width))
                elif self.location == SOUTH:
                    self.setPos(new_pos)

    def update_arrow_quadrant(self, new_location: Location) -> None:
        quadrant_mapping: Dict[
            Tuple(Quadrant, RotationDirection, MotionType), Dict[Location, Quadrant]
        ] = {
            ### ISO ###
            (NORTHEAST, CLOCKWISE, PRO): {NORTH: NORTHWEST, SOUTH: SOUTHEAST},
            (NORTHWEST, CLOCKWISE, PRO): {EAST: NORTHEAST, WEST: SOUTHWEST},
            (SOUTHWEST, CLOCKWISE, PRO): {NORTH: NORTHWEST, SOUTH: SOUTHEAST},
            (SOUTHEAST, CLOCKWISE, PRO): {WEST: SOUTHWEST, EAST: NORTHEAST},
            (NORTHEAST, COUNTER_CLOCKWISE, PRO): {WEST: NORTHWEST, EAST: SOUTHEAST},
            (NORTHWEST, COUNTER_CLOCKWISE, PRO): {SOUTH: SOUTHWEST, NORTH: NORTHEAST},
            (SOUTHWEST, COUNTER_CLOCKWISE, PRO): {EAST: SOUTHEAST, WEST: NORTHWEST},
            (SOUTHEAST, COUNTER_CLOCKWISE, PRO): {NORTH: NORTHEAST, SOUTH: SOUTHWEST},
            ### ANTI ###
            (NORTHEAST, CLOCKWISE, ANTI): {EAST: SOUTHEAST, WEST: NORTHWEST},
            (NORTHWEST, CLOCKWISE, ANTI): {NORTH: NORTHEAST, SOUTH: SOUTHWEST},
            (SOUTHWEST, CLOCKWISE, ANTI): {EAST: SOUTHEAST, WEST: NORTHWEST},
            (SOUTHEAST, CLOCKWISE, ANTI): {NORTH: NORTHEAST, SOUTH: SOUTHWEST},
            (NORTHEAST, COUNTER_CLOCKWISE, ANTI): {NORTH: NORTHWEST, SOUTH: SOUTHEAST},
            (NORTHWEST, COUNTER_CLOCKWISE, ANTI): {WEST: SOUTHWEST, EAST: NORTHEAST},
            (SOUTHWEST, COUNTER_CLOCKWISE, ANTI): {SOUTH: SOUTHEAST, NORTH: NORTHWEST},
            (SOUTHEAST, COUNTER_CLOCKWISE, ANTI): {EAST: NORTHEAST, WEST: SOUTHWEST},
        }

        current_quadrant = self.arrow.quadrant
        rotation_direction = self.arrow.rotation_direction
        motion_type = self.arrow.motion_type
        new_quadrant = quadrant_mapping.get(
            (current_quadrant, rotation_direction, motion_type), {}
        ).get(new_location)

        if new_quadrant:
            self.arrow.quadrant = new_quadrant
            start_location, end_location = self.arrow.get_start_end_locations(
                motion_type, rotation_direction, new_quadrant
            )
            self.arrow.start_location = start_location
            self.arrow.end_location = end_location
            self.arrow.update_appearance()

    def mouseReleaseEvent(self, event) -> None:
        if isinstance(self.scene(), self.pictograph.__class__):
            self.pictograph.removeItem(self.ghost_prop)
            self.pictograph.props.remove(self.ghost_prop)
            self.ghost_prop.arrow = None
            self.pictograph.update()
            self.finalize_prop_drop(event)

    def finalize_prop_drop(self, event: 'QGraphicsSceneMouseEvent') -> None:
        closest_handpoint = self.get_closest_handpoint(event.scenePos())
        new_location = self.get_closest_location(event.scenePos())

        self.location = new_location
        self.axis = self.get_axis(self.location)
        self.update_appearance()
        self.setPos(closest_handpoint)

        if self.arrow:
            self.arrow.update_appearance()
        self.previous_location = new_location
        self.pictograph.update()

    ### UPDATERS ###

    def get_axis(self, location) -> None:
        if self.layer == 1:
            axis: Axis = VERTICAL if location in [NORTH, SOUTH] else HORIZONTAL
        elif self.layer == 2:
            axis: Axis = HORIZONTAL if location in [NORTH, SOUTH] else VERTICAL
        return axis

    def set_prop_transform_origin_to_center(self: 'Prop') -> None:
        self.center = self.get_prop_center()
        self.setTransformOriginPoint(self.center)

    def set_prop_attrs_from_arrow(self, target_arrow: 'Arrow') -> None:
        self.color = target_arrow.color
        self.location = target_arrow.end_location
        self.axis = self.get_axis(self.location)
        self.update_appearance()

    ### GETTERS ###

    def get_rotation_angle(self) -> RotationAngle:
        angle_map: Dict[Tuple[Layer, Orientation], Dict[Location, RotationAngle]] = {
            (1, IN): {NORTH: 90, SOUTH: 270, WEST: 0, EAST: 180},
            (1, OUT): {NORTH: 270, SOUTH: 90, WEST: 180, EAST: 0},
            (2, CLOCKWISE): {NORTH: 0, SOUTH: 180, WEST: 270, EAST: 90},
            (2, COUNTER_CLOCKWISE): {NORTH: 180, SOUTH: 0, WEST: 90, EAST: 270},
        }

        key = (self.layer, self.orientation)
        return angle_map.get(key, {}).get(self.location, 0)  # Default to 0 if not found

    def update_rotation(self) -> None:
        rotation_angle = self.get_rotation_angle()
        self.setRotation(rotation_angle)

    def get_prop_center(self) -> QPointF:
        if self.axis == VERTICAL:
            return QPointF(
                (self.boundingRect().height() / 2), (self.boundingRect().width() / 2)
            )
        elif self.axis == HORIZONTAL:
            return QPointF(
                (self.boundingRect().width() / 2), (self.boundingRect().height() / 2)
            )

    def get_closest_handpoint(self, mouse_pos: QPointF) -> QPointF:
        closest_distance = float('inf')
        closest_handpoint = None
        for point in self.pictograph.grid.handpoints.values():
            distance = (point - mouse_pos).manhattanLength()
            if distance < closest_distance:
                closest_distance = distance
                closest_handpoint = point
        return closest_handpoint

    def get_closest_location(self, mouse_pos: QPointF) -> Location:
        closest_distance = float('inf')
        closest_location = None
        for location, point in self.pictograph.grid.handpoints.items():
            distance = (point - mouse_pos).manhattanLength()
            if distance < closest_distance:
                closest_distance = distance
                closest_location = location
        return closest_location

    def get_svg_file(self, prop_type: PropType) -> str:
        svg_file = f'{PROP_DIR}/{prop_type}.svg'
        return svg_file
    
    ### HELPERS ###

    def swap_axis(self) -> None:
        if self.axis == VERTICAL:
            self.axis = HORIZONTAL
        else:
            self.axis = VERTICAL
        self.update_rotation()

    def swap_layer(self) -> None:
        if self.layer == 1:
            self.layer = 2
        else:
            self.layer = 1
        self.update_rotation()

    def set_svg_color(self, new_color: Color) -> bytes:
        new_hex_color: ColorHex = COLOR_MAP.get(new_color)

        with open(self.svg_file, 'r') as f:
            svg_data = f.read()

        style_tag_pattern = re.compile(
            r'\.st0{fill\s*:\s*(#[a-fA-F0-9]{6})\s*;}', re.DOTALL
        )
        match = style_tag_pattern.search(svg_data)

        if match:
            old_hex_color: ColorHex = match.group(1)
            svg_data = svg_data.replace(old_hex_color, new_hex_color)
        return svg_data.encode('utf-8')

    def delete(self) -> None:
        self.pictograph.removeItem(self)
        self.pictograph.props.remove(self)
        self.pictograph.update()
