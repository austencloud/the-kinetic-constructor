
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import QPointF, Qt
import re
from settings.string_constants import MOTION_TYPE, TURNS, COLOR, COUNTER_CLOCKWISE, CLOCKWISE, RED, BLUE, RED_HEX, BLUE_HEX, PRO, ANTI, STATIC, ROTATION_DIRECTION, QUADRANT, NORTHEAST, SOUTHEAST, SOUTHWEST, NORTHWEST, START_LOCATION, END_LOCATION, ARROW_ATTRIBUTES, ARROW_DIR
from data.start_end_location_mapping import start_end_location_mapping


class Arrow(QGraphicsSvgItem):
    def __init__(self, graphboard, attributes):
        super().__init__()
        if attributes:
            self.svg_file = self.get_svg_file( 
                attributes.get(MOTION_TYPE), attributes.get(TURNS)
            )
            self._setup_svg_renderer(self.svg_file)
        self._setup(graphboard, attributes)

    ### SETUP ###
    def _setup(self, graphboard, attributes):
        self._setup_attributes(graphboard, attributes)
        self._setup_graphics_flags()

    def _setup_attributes(self, graphboard, attributes):
        self.graphboard = graphboard
        if hasattr(graphboard, "infobox"):
            self.infobox = graphboard.infobox

        self.in_graphboard = False
        self.drag_offset = QPointF(0, 0)
        self.is_still = False
        self.staff = None
        self.is_mirrored = False
        self.previous_arrow = None

        self.color = None
        self.motion_type = None
        self.rotation_direction = None
        self.quadrant = None
        self.start_location = None
        self.end_location = None
        self.turns = None
        self.mirror_transform = None # carries the transform to be applied to the ghost arrow

        if attributes:
            self.set_object_attr_from_dict(attributes)
            self.update_appearance()
        self.center = self.boundingRect().center()

    def _setup_graphics_flags(self):
        self.setFlags(
            QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable
            | QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable
            | QGraphicsSvgItem.GraphicsItemFlag.ItemSendsGeometryChanges
            | QGraphicsSvgItem.GraphicsItemFlag.ItemIsFocusable
        )
        self.setTransformOriginPoint(self.center)

    def _setup_svg_renderer(self, svg_file):
        self.renderer = QSvgRenderer(svg_file)
        self.setSharedRenderer(self.renderer)


    ### MOUSE EVENTS ###

    def mousePressEvent(self, event):
        self.setSelected(True)
        self.ghost_arrow = self.graphboard.ghost_arrows[self.color]
        if self.mirror_transform:
            self.ghost_arrow.setTransform(self.mirror_transform)
        self.ghost_arrow.update(self.quadrant, self)
        self.graphboard.addItem(self.ghost_arrow)
        self.ghost_arrow.staff = self.staff
        self.graphboard.arrows.append(self.ghost_arrow)
        self.graphboard.arrows.remove(self)
        self.graphboard.arrow_positioner.update()
        self.graphboard.arrows.append(self)
        for arrow in self.graphboard.arrows:
            if arrow != self:
                arrow.setSelected(False)

        self.drag_start_pos = self.pos()
        self.drag_offset = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            scene_event_pos = self.mapToScene(event.pos())
            view_event_pos = self.graphboard.view.mapFromScene(scene_event_pos)
            in_view = self.graphboard.view.rect().contains(view_event_pos)
            new_pos = self.mapToScene(event.pos()) - self.boundingRect().center()
            self.setPos(new_pos)

            scene_pos = new_pos + self.center
            new_quadrant = self.graphboard.determine_quadrant(
                scene_pos.x(), scene_pos.y()
            )

            if self.quadrant != new_quadrant:
                if in_view:
                    self.update_for_new_quadrant(new_quadrant)


    def mouseReleaseEvent(self, event):
        self.graphboard.removeItem(self.ghost_arrow)
        self.graphboard.arrows.remove(self.ghost_arrow)
        self.ghost_arrow.staff = None
        self.ghost_arrow = None
        self.graphboard.arrow_positioner.update()

    ### GETTERS ###

    def get_svg_data(self, svg_file):
        with open(svg_file, CLOCKWISE) as f:
            svg_data = f.read()
        return svg_data.encode("utf-8")

    def get_rotation_angle(self, quadrant, motion_type, rotation_direction):
        quadrant_to_angle = self.get_quadrant_to_angle_map(
            motion_type, rotation_direction
        )
        return quadrant_to_angle.get(quadrant, 0)

    def get_quadrant_to_angle_map(self, motion_type, rotation_direction):
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

    def get_attributes(self):
        return {attr: getattr(self, attr) for attr in ARROW_ATTRIBUTES}

    def get_start_end_locations(self, motion_type, rotation_direction, quadrant):
        return (
            start_end_location_mapping.get(quadrant, {})
            .get(rotation_direction, {})
            .get(motion_type, (None, None))
        )

    ### UPDATERS ###

    def update(self, attributes):
        self.set_object_attr_from_dict(attributes)
        self.update_appearance()
        svg_file = self.get_svg_file(self.motion_type, self.turns)
        self.update_svg(svg_file)

    def update_appearance(self):
        self.update_color()
        self.update_rotation()

    def set_transform_origin_to_center(self):
        # Call this method after any changes that might affect the boundingRect.
        self.center = self.boundingRect().center()
        self.setTransformOriginPoint(self.center)

    def update_color(self):
        if self.motion_type in [PRO, ANTI]:
            new_svg_data = self.set_svg_color(self.color)
            self.renderer.load(new_svg_data)
            self.setSharedRenderer(self.renderer)

    def update_rotation(self):
        # Ensure transformation origin point is at the center.
        # Proceed with obtaining the rotation angle and rotate.
        angle = self.get_rotation_angle(
            self.quadrant, self.motion_type, self.rotation_direction
        )
        self.setRotation(angle)

    def set_dict_attr_from_object(self):
        for attr in ARROW_ATTRIBUTES:
            self.attributes[attr] = getattr(self, attr)

    def set_object_attr_from_dict(self, attributes):
        
        for attr in ARROW_ATTRIBUTES:
            value = attributes.get(attr)
            if attr == TURNS:
                value = int(value)
            setattr(self, attr, value)

        self.attributes = {
            COLOR: attributes.get(COLOR, None),
            MOTION_TYPE: attributes.get(MOTION_TYPE, None),
            ROTATION_DIRECTION: attributes.get(ROTATION_DIRECTION, None),
            QUADRANT: attributes.get(QUADRANT, None),
            START_LOCATION: attributes.get(START_LOCATION, None),
            END_LOCATION: attributes.get(END_LOCATION, None),
            TURNS: attributes.get(TURNS, None),
        }

    def update_svg(self, svg_file):
        self.svg_file = svg_file
        self._setup_svg_renderer(svg_file)
        self.set_svg_color(self.color)

    def get_svg_file(self, motion_type, turns):
        svg_file = f"{ARROW_DIR}{motion_type}_{turns}.svg"
        return svg_file

    def update_for_new_quadrant(self, new_quadrant):
        self.quadrant = new_quadrant
        self.start_location, self.end_location = self.get_start_end_locations(
            self.motion_type, self.rotation_direction, self.quadrant
        )
        
        self.attributes[QUADRANT] = new_quadrant
        self.attributes[START_LOCATION] = self.start_location
        self.attributes[END_LOCATION] = self.end_location
        
        self.update_appearance()
        self.previous_arrow = (
            self.staff.arrow
        )  # Consider storing the old arrow before changing.
        self.staff.location = self.end_location
        self.staff.update_attributes_from_arrow(self)
        self.update_appearance()
        
        self.ghost_arrow.update(new_quadrant, self)
        self.graphboard.arrows.remove(self)
        self.graphboard.arrow_positioner.update()
        self.graphboard.update()
        self.graphboard.arrows.append(self)
        
    ### MANIPULATION ###

    def increment_turns(self):
        self.turns += 1
        if self.turns > 2:
            self.turns = 0
        svg_file = self.get_svg_file(self.motion_type, self.turns)
        self.update_svg(svg_file)
        self.update_appearance()
        self.set_dict_attr_from_object()
        self.graphboard.update()

    def decrement_turns(self):
        self.turns -= 1
        if self.turns < 0:
            self.turns = 2
        svg_file = self.get_svg_file(self.motion_type, self.turns)
        self.update_svg(svg_file)
        self.update_appearance()
        self.set_dict_attr_from_object()
        self.graphboard.update()

    def set_svg_color(self, new_color):
        color_map = {RED: RED_HEX, BLUE: BLUE_HEX}
        new_hex_color = color_map.get(new_color)

        with open(self.svg_file, CLOCKWISE) as f:
            svg_data = f.read()

        style_tag_pattern = re.compile(
            r"\.st0{fill\s*:\s*(#[a-fA-F0-9]{6})\s*;}", re.DOTALL
        )
        match = style_tag_pattern.search(svg_data)

        if match:
            old_color = match.group(1)
            svg_data = svg_data.replace(old_color, new_hex_color)
        return svg_data.encode("utf-8")


class BlankArrow(Arrow):
    def __init__(self, graphboard, attributes):
        super().__init__(graphboard, attributes)
        self._disable_interactivity()
        self.hide()
        
    def _disable_interactivity(self):
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, False)