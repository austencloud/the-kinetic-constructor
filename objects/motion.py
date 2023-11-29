from utilities.TypeChecking.TypeChecking import (
    MotionAttributesDicts,
    Colors,
    MotionTypes,
    Turns,
    RotationDirections,
    Locations,
    Locations,
    Orientations,
    Layers,
)
from settings.string_constants import *
from typing import TYPE_CHECKING, Dict, Tuple

if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from objects.arrow import Arrow
    from objects.prop import Prop
from settings.string_constants import DASH


class Motion:
    def __init__(
        self,
        pictograph: "Pictograph",
        arrow: "Arrow",
        prop: "Prop",
        attributes: MotionAttributesDicts,
    ) -> None:
        self.pictograph = pictograph
        self.arrow = arrow
        self.prop = prop
        self.attributes = attributes

        self.setup_attributes(attributes)

        prop.update_rotation()

    def setup_attributes(self, attributes) -> None:
        self.color: Colors = attributes[COLOR]
        self.motion_type: MotionTypes = attributes[MOTION_TYPE]
        self.turns: Turns = attributes[TURNS]
        self.rotation_direction: RotationDirections = attributes[ROTATION_DIRECTION]
        self.arrow_location: Locations = attributes[ARROW_LOCATION]

        self.start_location: Locations = attributes[START_LOCATION]
        self.end_location: Locations = attributes[END_LOCATION]

        self.start_orientation: Orientations = attributes[START_ORIENTATION]
        self.end_orientation: Orientations = self.get_end_orientation()

        self.start_layer: Layers = attributes[START_LAYER]
        self.end_layer: Layers = self.get_end_layer()

        from objects.arrow import StaticArrow

        if not isinstance(self.arrow, StaticArrow):
            self.prop.orientation = self.end_orientation
            self.prop.layer = self.end_layer
            self.prop.update_appearance()

    def get_end_layer(self) -> Layers:
        if self.turns in [0, 1, 2]:
            end_layer = self.start_layer
        elif self.turns in [0.5, 1.5]:
            end_layer = 3 - self.start_layer  # Switches between 1 and 2
        return end_layer

    def get_end_orientation(self) -> Orientations:
        orientation_map: dict[
            Tuple[Orientations], Dict[MotionTypes, Dict[Turns, Orientations]]
        ] = {
            (IN, CLOCKWISE): {
                PRO: {
                    0: IN,
                    0.5: COUNTER_CLOCKWISE,
                    1: OUT,
                    1.5: CLOCKWISE,
                    2: IN,
                    2.5: COUNTER_CLOCKWISE,
                    3: OUT,
                },
                ANTI: {
                    0: OUT,
                    0.5: CLOCKWISE,
                    1: IN,
                    1.5: COUNTER_CLOCKWISE,
                    2: OUT,
                    2.5: CLOCKWISE,
                    3: IN,
                },
            },
            (OUT, CLOCKWISE): {
                PRO: {
                    0: OUT,
                    0.5: CLOCKWISE,
                    1: IN,
                    1.5: COUNTER_CLOCKWISE,
                    2: OUT,
                    2.5: CLOCKWISE,
                    3: IN,
                },
                ANTI: {
                    0: IN,
                    0.5: COUNTER_CLOCKWISE,
                    1: OUT,
                    1.5: CLOCKWISE,
                    2: IN,
                    2.5: COUNTER_CLOCKWISE,
                    3: OUT,
                },
            },
            (IN, COUNTER_CLOCKWISE): {
                PRO: {
                    0: IN,
                    0.5: CLOCKWISE,
                    1: OUT,
                    1.5: COUNTER_CLOCKWISE,
                    2: IN,
                    2.5: CLOCKWISE,
                    3: OUT,
                },
                ANTI: {
                    0: OUT,
                    0.5: COUNTER_CLOCKWISE,
                    1: IN,
                    1.5: CLOCKWISE,
                    2: OUT,
                    2.5: COUNTER_CLOCKWISE,
                    3: IN,
                },
            },
            (OUT, COUNTER_CLOCKWISE): {
                PRO: {
                    0: OUT,
                    0.5: COUNTER_CLOCKWISE,
                    1: IN,
                    1.5: CLOCKWISE,
                    2: OUT,
                    2.5: COUNTER_CLOCKWISE,
                    3: IN,
                },
                ANTI: {
                    0: IN,
                    0.5: CLOCKWISE,
                    1: OUT,
                    1.5: COUNTER_CLOCKWISE,
                    2: IN,
                    2.5: CLOCKWISE,
                    3: OUT,
                },
            },
        }
        for key in orientation_map:
            orientation_map[key][STATIC] = orientation_map[key][PRO]
            orientation_map[key][DASH] = orientation_map[key][ANTI]

        key: Tuple[Orientations] = (self.start_orientation, self.rotation_direction)
        motion_map = orientation_map.get(key, {})
        return motion_map.get(self.motion_type, {}).get(self.turns)

    def update_attr_from_arrow(self) -> None:
        self.color = self.arrow.color
        self.motion_type = self.arrow.motion_type
        self.turns = self.arrow.turns
        self.rotation_direction = self.arrow.rotation_direction
        self.arrow_location = self.arrow.arrow_location
        self.start_location = self.arrow.start_location
        self.end_location = self.arrow.end_location

    def update_turns(self, turns: int) -> None:
        self.arrow.turns = turns
        self.turns = self.arrow.turns
        self.end_orientation = self.get_end_orientation()
        self.prop.orientation = self.end_orientation
        self.prop.update_appearance()
        self.prop.update_rotation()
        svg_file = self.arrow.get_svg_file(self.arrow.motion_type, self.arrow.turns)
        self.arrow.update_svg(svg_file)
        self.arrow.update_appearance()
        self.arrow.attributes[TURNS] = self.arrow.turns
        if hasattr(self.arrow, "ghost_arrow"):
            self.arrow.ghost_arrow.turns = self.arrow.turns
            self.arrow.ghost_arrow.update_svg(svg_file)
            self.arrow.ghost_arrow.update_appearance()
        self.pictograph.update_pictograph()

    def add_half_turn(self) -> None:
        if self.arrow.turns < 3.0:
            self.prop.swap_layer()
            self.prop.motion.end_layer = self.prop.layer
            self.prop.swap_axis()
            self.update_turns(self.arrow.turns + 0.5)
        else:
            self.update_turns(3.0)

    def subtract_half_turn(self) -> None:
        if self.arrow.turns > 0:
            self.prop.swap_layer()
            self.prop.motion.end_layer = self.prop.layer
            self.prop.swap_axis()
            self.update_turns(self.arrow.turns - 0.5)
            if self.arrow.turns == 0:
                self.update_turns(0)
        else:
            self.update_turns(0)

    def add_turn(self) -> None:
        self.update_turns(self.arrow.turns + 1 if self.arrow.turns < 3 else 3)

    def subtract_turn(self) -> None:
        self.update_turns(self.arrow.turns - 1 if self.arrow.turns > 0 else 0)
