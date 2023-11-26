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
from settings.string_constants import (
    COLOR,
    MOTION_TYPE,
    TURNS,
    ROTATION_DIRECTION,
    QUADRANT,
    START_LOCATION,
    END_LOCATION,
    START_ORIENTATION,
    END_ORIENTATION,
    START_LAYER,
    END_LAYER,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graph_editor.graphboard.graphboard import GraphBoard
    from objects.arrow import Arrow
    from objects.props.staff import Staff


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

    def setup_attributes(self, attributes) -> None:
        self.color: Color = attributes[COLOR]
        self.motion_type: MotionType = attributes[MOTION_TYPE]
        self.turns: Turns = attributes[TURNS]
        self.rotation_direction: RotationDirection = attributes[ROTATION_DIRECTION]
        self.quadrant: Quadrant = attributes[QUADRANT]
        
        self.start_location: Location = attributes[START_LOCATION]
        self.end_location: Location = attributes[END_LOCATION]
        
        self.start_orientation: Orientation = attributes[START_ORIENTATION]
        self.end_orientation: Orientation = attributes[END_ORIENTATION]
        
        self.start_layer: Layer = attributes[START_LAYER]
        self.end_layer: Layer = attributes[END_LAYER]

