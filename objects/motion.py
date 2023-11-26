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

    def get_end_orientation(self) -> Orientation:
        orientation_behavior_map = {
            (1, IN, [PRO, STATIC]): {0: IN, 1: OUT, 2: IN},
            (1, OUT, [PRO, STATIC]): {0: OUT, 1: IN, 2: OUT},
            (1, IN, [ANTI, DASH]): {0: OUT, 1: IN, 2: OUT},
            (1, OUT, [ANTI, DASH]): {0: IN, 1: OUT, 2: IN},
            (2, CLOCKWISE, [PRO, STATIC]): {
                0: CLOCKWISE,
                1: COUNTER_CLOCKWISE,
                2: CLOCKWISE,
            },
            (2, COUNTER_CLOCKWISE, [PRO, STATIC]): {
                0: COUNTER_CLOCKWISE,
                1: CLOCKWISE,
                2: COUNTER_CLOCKWISE,
            },
            (2, CLOCKWISE, [ANTI, DASH]): {
                0: COUNTER_CLOCKWISE,
                1: CLOCKWISE,
                2: COUNTER_CLOCKWISE,
            },
            (2, COUNTER_CLOCKWISE, [ANTI, DASH]): {
                0: CLOCKWISE,
                1: COUNTER_CLOCKWISE,
                2: CLOCKWISE,
            },
        }

        # Determine end orientation
        for (
            layer,
            orientation,
            motion_types,
        ), turns_map in orientation_behavior_map.items():
            if (
                self.start_layer == layer
                and self.start_orientation == orientation
                and self.motion_type in motion_types
            ):
                end_orientation = turns_map.get(self.turns)
                break

        return end_orientation

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
        for start_orientation in [IN, OUT]:
            for rotation_direction in [CLOCKWISE, COUNTER_CLOCKWISE]:
                key = (start_orientation, rotation_direction)
                orientation_map[key][STATIC] = orientation_map[key][PRO]
                orientation_map[key][DASH] = orientation_map[key][ANTI]

        key = (self.start_orientation, self.rotation_direction)
        motion_map: dict[MotionType, dict[Turns, Orientation]] = orientation_map.get(
            key, {}
        )
        end_orientation = motion_map.get(self.motion_type, {}).get(self.turns, IN)

        return end_orientation
