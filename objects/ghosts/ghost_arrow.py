from settings.string_constants import COLOR
from objects.arrow import Arrow
from settings.string_constants import (
    ARROW_ATTRIBUTES,
    COLOR,
    MOTION_TYPE,
    ROTATION_DIRECTION,
    QUADRANT,
    START_LOCATION,
    END_LOCATION,
    TURNS,
    STATIC,
    PRO,
    CLOCKWISE,
    NORTHEAST,
    SOUTHEAST,
    SOUTHWEST,
    NORTHWEST,
    ANTI,
    COUNTER_CLOCKWISE,
)
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from PyQt6.QtCore import QPointF


class GhostArrow(Arrow):
    def __init__(self, graphboard, attributes):
        super().__init__(graphboard, attributes)
        self.setOpacity(0.2)
        self.graphboard = graphboard
        self.color = attributes.get(COLOR)
        self.target_arrow = None
        self.setup_svg_renderer(self.svg_file)

    ### SETUP ###

    def _setup_attributes(self, graphboard, attributes):
        self.graphboard = graphboard

        self.drag_offset = QPointF(0, 0)

        self.staff = None
        self.ghost_arrow = None

        self.is_mirrored = False

        self.color = None
        self.motion_type = None
        self.rotation_direction = None
        self.quadrant = None
        self.start_location = None
        self.end_location = None
        self.turns = None

        self.mirror_transform = None

        if attributes:
            self.set_attributes_from_dict(attributes)
            self.update_appearance()

        self.center = self.boundingRect().center()
        self.setTransformOriginPoint(self.center)

    ### UPDATE ###

    def update(self, target_arrow, drag=None):
        if not drag:
            self.set_attributes_from_dict(target_arrow.get_attributes())
        else:
            self.set_attributes_from_dict(drag.get_attributes())
        self.update_svg(target_arrow.svg_file)
        self.setup_graphics_flags()
        self.update_appearance()
        self.show()

    def update_svg(self, svg_file):
        self.svg_file = svg_file
        self.setup_svg_renderer(svg_file)
        self.update_appearance()
    def update_appearance(self):
        self.update_color()
        self.update_rotation()

    def update_color(self):
        if self.motion_type is not STATIC:
            new_svg_data = self.set_svg_color(self.color)
            self.renderer.load(new_svg_data)
            self.setSharedRenderer(self.renderer)

    def update_rotation(self):
        angle = self.get_rotation_angle()
        self.setRotation(angle)

    def set_attributes_from_dict(self, attributes):
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

    def set_transform_origin_to_center(self):
        # Call this method after any changes that might affect the boundingRect.
        self.center = self.boundingRect().center()
        self.setTransformOriginPoint(self.center)

    ### GETTERS ###

    def get_rotation_angle(self, arrow=None):
        arrow = arrow or self
        quadrant_to_angle = self.get_quadrant_to_angle_map(
            arrow.motion_type, arrow.rotation_direction
        )
        return quadrant_to_angle.get(arrow.quadrant, 0)

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
