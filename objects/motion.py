from utilities.TypeChecking.TypeChecking import (
    MotionAttributesDicts,
    Color,
    MotionType,
    Turns,
    RotationDirection,
    Quadrant,
    Location,
    Orientation,
    Layer,
)
from settings.string_constants import *
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graph_editor.graphboard.graphboard import GraphBoard
    from objects.arrow import Arrow
    from objects.props.staff import Staff
from settings.string_constants import DASH


class Motion:
    def __init__(
        self,
        graphboard: "GraphBoard",
        arrow: "Arrow",
        staff: "Staff",
        attributes: MotionAttributesDicts,
    ) -> None:
        self.graphboard = graphboard
        self.arrow = arrow
        self.staff = staff
        self.attributes = attributes

        self.setup_attributes(attributes)

        self.staff.layer = self.end_layer
        self.staff.orientation = self.end_orientation

        staff.update_rotation()

    def setup_attributes(self, attributes) -> None:
        self.color: Color = attributes[COLOR]
        self.motion_type: MotionType = attributes[MOTION_TYPE]
        self.turns: Turns = attributes[TURNS]
        self.rotation_direction: RotationDirection = attributes[ROTATION_DIRECTION]
        self.quadrant: Quadrant = attributes[QUADRANT]

        self.start_location: Location = attributes[START_LOCATION]
        self.end_location: Location = attributes[END_LOCATION]

        self.start_orientation: Orientation = attributes[START_ORIENTATION]
        self.end_orientation: Orientation = self.get_end_orientation()

        self.start_layer: Layer = attributes[START_LAYER]
        self.end_layer: Layer = self.get_end_layer()


    def get_end_layer(self) -> Layer:
        if self.turns in [0, 1, 2]:
            end_layer = self.start_layer
        elif self.turns in [0.5, 1.5]:
            end_layer = 3 - self.start_layer  # Switches between 1 and 2
        return end_layer

    def get_end_orientation(self) -> Orientation:
        orientation_map: dict[
            tuple[Orientation], dict[MotionType, dict[Turns, Orientation]]
        ] = {
            (IN, CLOCKWISE): {
                PRO: {0: IN, 0.5: COUNTER_CLOCKWISE, 1: OUT, 1.5: CLOCKWISE, 2: IN},
                ANTI: {0: OUT, 0.5: CLOCKWISE, 1: IN, 1.5: COUNTER_CLOCKWISE, 2: OUT},
            },
            (OUT, CLOCKWISE): {
                PRO: {0: OUT, 0.5: CLOCKWISE, 1: IN, 1.5: COUNTER_CLOCKWISE, 2: OUT},
                ANTI: {0: IN, 0.5: COUNTER_CLOCKWISE, 1: OUT, 1.5: CLOCKWISE, 2: IN},
            },
            (IN, COUNTER_CLOCKWISE): {
                PRO: {0: IN, 0.5: CLOCKWISE, 1: OUT, 1.5: COUNTER_CLOCKWISE, 2: IN},
                ANTI: {0: OUT, 0.5: COUNTER_CLOCKWISE, 1: IN, 1.5: CLOCKWISE, 2: OUT},
            },
            (OUT, COUNTER_CLOCKWISE): {
                PRO: {0: OUT, 0.5: COUNTER_CLOCKWISE, 1: IN, 1.5: CLOCKWISE, 2: OUT},
                ANTI: {0: IN, 0.5: CLOCKWISE, 1: OUT, 1.5: COUNTER_CLOCKWISE, 2: IN},
            },
        }
        # Update repetitive mappings for STATIC and DASH
        for key in orientation_map:
            orientation_map[key][STATIC] = orientation_map[key][PRO]
            orientation_map[key][DASH] = orientation_map[key][ANTI]

        # Retrieve end orientation
        key = (self.start_orientation, self.rotation_direction)
        motion_map = orientation_map.get(key, {})
        return motion_map.get(self.motion_type, {}).get(self.turns)