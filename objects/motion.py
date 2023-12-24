from enum import Enum
from Enums import MotionType, Orientation
from utilities.TypeChecking.TypeChecking import (
    MotionAttribute,
    MotionAttributesDicts,
    PropAttribute,
)
from constants.string_constants import *
from typing import TYPE_CHECKING, Literal, Union


if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from objects.arrow.arrow import Arrow
    from objects.prop.prop import Prop
    from widgets.graph_editor_tab.object_panel.arrowbox.arrowbox import ArrowBox


MotionType = MotionType
Orientation = Orientation
MA = MotionAttribute


class Motion:
    def __init__(
        self,
        scene: Union["Pictograph", "ArrowBox"],
        motion_dict: MotionAttributesDicts,
        blank=False,
    ) -> None:
        self.scene = scene
        self.motion_dict = motion_dict
        self.initialize_attributes()
        self.color: MotionAttribute.COLOR = motion_dict["color"]

        if not blank:
            self.setup_attributes(motion_dict)

    def initialize_attributes(self):
        self.arrow: Arrow = None
        self.prop: Prop = None
        self.color: MA.COLOR = None
        self.motion_type: MA.MOTION_TYPE = None
        self.turns: MA.TURNS = None
        self.rotation_direction: MA.ROTATION_DIRECTION = None
        self.start_location: MA.START_LOCATION = None
        self.end_location: MA.END_LOCATION = None
        self.start_orientation: MA.START_ORIENTATION = None
        self.end_orientation: MA.END_ORIENTATION = None

    ### SETUP ###

    def setup_attributes(self, motion_dict) -> None:
        if MA.ARROW in motion_dict and MA.PROP in motion_dict:
            if motion_dict[MA.ARROW] and motion_dict[MA.PROP]:
                self.arrow.motion = self
                self.prop.motion = self
                self.arrow: Arrow = motion_dict[MA.ARROW]
                self.prop: Prop = motion_dict[MA.PROP]
        else:
            self.arrow: Arrow = None
            self.prop: Prop = None

        self.motion_type: MotionAttribute.MOTION_TYPE = motion_dict[MA.MOTION_TYPE]
        self.turns: MotionAttribute.TURNS = motion_dict[MA.TURNS]
        self.rotation_direction: MotionAttribute.ROTATION_DIRECTION = motion_dict[
            MA.ROTATION_DIRECTION
        ]
        self.start_location: MotionAttribute.START_LOCATION = motion_dict[
            MA.START_LOCATION
        ]
        self.end_location: MotionAttribute.END_LOCATION = motion_dict[MA.END_LOCATION]
        self.start_orientation: MotionAttribute.START_ORIENTATION = motion_dict[
            MA.START_ORIENTATION
        ]

        self.assign_location_to_arrow()

        self.end_orientation: MotionAttribute.END_ORIENTATION = (
            self.get_end_orientation()
        )
        self.update_prop_orientation()

    def assign_location_to_arrow(self):
        if hasattr(self, "arrow") and self.arrow:
            self.arrow.location = self.get_arrow_location(
                self.start_location, self.end_location
            )

    ### UPDATE ###

    def update_attr_from_arrow(self) -> None:
        self.color = self.arrow.color
        self.motion_type = self.arrow.motion_type
        self.turns = self.arrow.turns

    def update_turns(self, turns: int) -> None:
        self.arrow.turns = turns
        self.turns = self.arrow.turns
        self.end_orientation = self.get_end_orientation()
        self.update_prop_orientation()
        self.prop.update_appearance()
        self.prop.update_rotation()
        svg_file = self.arrow.get_svg_file(self.arrow.motion_type, self.arrow.turns)
        self.arrow.update_svg(svg_file)
        self.arrow.update_appearance()
        self.arrow.arrow_dict[MotionAttribute.TURNS] = self.arrow.turns
        if hasattr(self.arrow, "ghost"):
            if self.arrow.ghost:
                self.arrow.ghost.turns = self.arrow.turns
                self.arrow.ghost.update_svg(svg_file)
                self.arrow.ghost.update_appearance()
        self.scene.update_pictograph()

    def update_prop_orientation(self) -> None:
        if hasattr(self, "prop") and self.prop:
            self.prop.orientation = self.end_orientation
            self.prop.location = self.end_location
            self.prop.axis: PropAttribute.AXIS = self.prop.get_axis_from_orientation(
                self.prop.orientation, self.prop.location
            )
            self.prop.update_rotation()
            self.prop.update_appearance()

    def clear_attributes(self):
        self.start_location = None
        self.end_location = None
        self.turns = None
        self.motion_type = None

        self.rotation_direction = None
        self.start_orientation = None
        self.end_orientation = None

    ### GETTERS ###

    def get_attributes(self) -> MotionAttributesDicts:
        return {
            MotionAttribute.COLOR: self.color,
            MotionAttribute.MOTION_TYPE: self.motion_type,
            MotionAttribute.TURNS: self.turns,
            MotionAttribute.ROTATION_DIRECTION: self.rotation_direction,
            MotionAttribute.START_LOCATION: self.start_location,
            MotionAttribute.END_LOCATION: self.end_location,
            MotionAttribute.START_ORIENTATION: self.start_orientation,
            MotionAttribute.END_ORIENTATION: self.end_orientation,
        }

    def get_end_orientation(self) -> MotionAttribute.END_ORIENTATION:
        # Combine layer1 maps

        # Combine layer1 maps
        whole_turn_orientation_map = {
            (MotionType.PRO, 0, Orientation.IN): Orientation.IN,
            (MotionType.PRO, 1, Orientation.IN): Orientation.OUT,
            (MotionType.PRO, 2, Orientation.IN): Orientation.IN,
            (MotionType.PRO, 3, Orientation.IN): Orientation.OUT,
            (MotionType.PRO, 0, Orientation.OUT): Orientation.OUT,
            (MotionType.PRO, 1, Orientation.OUT): Orientation.IN,
            (MotionType.PRO, 2, Orientation.OUT): Orientation.OUT,
            (MotionType.PRO, 3, Orientation.OUT): Orientation.IN,
            (MotionType.ANTI, 0, Orientation.IN): Orientation.OUT,
            (MotionType.ANTI, 1, Orientation.IN): Orientation.IN,
            (MotionType.ANTI, 2, Orientation.IN): Orientation.OUT,
            (MotionType.ANTI, 3, Orientation.IN): Orientation.IN,
            (MotionType.ANTI, 0, Orientation.OUT): Orientation.IN,
            (MotionType.ANTI, 1, Orientation.OUT): Orientation.OUT,
            (MotionType.ANTI, 2, Orientation.OUT): Orientation.IN,
            (MotionType.ANTI, 3, Orientation.OUT): Orientation.OUT,
            (MotionType.PRO, 0, Orientation.CLOCK): Orientation.CLOCK,
            (MotionType.PRO, 1, Orientation.CLOCK): Orientation.COUNTER,
            (MotionType.PRO, 2, Orientation.CLOCK): Orientation.CLOCK,
            (MotionType.PRO, 3, Orientation.CLOCK): Orientation.COUNTER,
            (MotionType.PRO, 0, Orientation.COUNTER): Orientation.COUNTER,
            (MotionType.PRO, 1, Orientation.COUNTER): Orientation.CLOCK,
            (MotionType.PRO, 2, Orientation.COUNTER): Orientation.COUNTER,
            (MotionType.PRO, 3, Orientation.COUNTER): Orientation.CLOCK,
            (MotionType.ANTI, 0, Orientation.CLOCK): Orientation.COUNTER,
            (MotionType.ANTI, 1, Orientation.CLOCK): Orientation.CLOCK,
            (MotionType.ANTI, 2, Orientation.CLOCK): Orientation.COUNTER,
            (MotionType.ANTI, 3, Orientation.CLOCK): Orientation.CLOCK,
            (MotionType.ANTI, 0, Orientation.COUNTER): Orientation.CLOCK,
            (MotionType.ANTI, 1, Orientation.COUNTER): Orientation.COUNTER,
            (MotionType.ANTI, 2, Orientation.COUNTER): Orientation.CLOCK,
            (MotionType.ANTI, 3, Orientation.COUNTER): Orientation.COUNTER,
        }

        # Combine layer2 maps

        # ({HANDPATH_DIRECTION}, {START_ORIENTATION}, {END_ORIENTATION}})
        clockwise_handpath_half_turns_map = {
            (MotionType.PRO, 0.5, Orientation.IN): Orientation.COUNTER,
            (MotionType.PRO, 1.5, Orientation.IN): Orientation.CLOCK,
            (MotionType.PRO, 2.5, Orientation.IN): Orientation.COUNTER,
            (MotionType.PRO, 0.5, Orientation.OUT): Orientation.CLOCK,
            (MotionType.PRO, 1.5, Orientation.OUT): Orientation.COUNTER,
            (MotionType.PRO, 2.5, Orientation.OUT): Orientation.CLOCK,
            (MotionType.ANTI, 0.5, Orientation.IN): Orientation.CLOCK,
            (MotionType.ANTI, 1.5, Orientation.IN): Orientation.COUNTER,
            (MotionType.ANTI, 2.5, Orientation.IN): Orientation.CLOCK,
            (MotionType.ANTI, 0.5, Orientation.OUT): Orientation.COUNTER,
            (MotionType.ANTI, 1.5, Orientation.OUT): Orientation.CLOCK,
            (MotionType.ANTI, 2.5, Orientation.OUT): Orientation.COUNTER,
            (MotionType.PRO, 0.5, Orientation.CLOCK): Orientation.IN,
            (MotionType.PRO, 1.5, Orientation.CLOCK): Orientation.OUT,
            (MotionType.PRO, 2.5, Orientation.CLOCK): Orientation.IN,
            (MotionType.PRO, 0.5, Orientation.COUNTER): Orientation.OUT,
            (MotionType.PRO, 1.5, Orientation.COUNTER): Orientation.IN,
            (MotionType.PRO, 2.5, Orientation.COUNTER): Orientation.OUT,
            (MotionType.ANTI, 0.5, Orientation.CLOCK): Orientation.OUT,
            (MotionType.ANTI, 1.5, Orientation.CLOCK): Orientation.IN,
            (MotionType.ANTI, 2.5, Orientation.CLOCK): Orientation.OUT,
            (MotionType.ANTI, 0.5, Orientation.COUNTER): Orientation.IN,
            (MotionType.ANTI, 1.5, Orientation.COUNTER): Orientation.OUT,
            (MotionType.ANTI, 2.5, Orientation.COUNTER): Orientation.IN,
        }

        counter_handpath_half_turns_map = {
            (MotionType.PRO, 0.5, Orientation.IN): Orientation.CLOCK,
            (MotionType.PRO, 1.5, Orientation.IN): Orientation.COUNTER,
            (MotionType.PRO, 2.5, Orientation.IN): Orientation.CLOCK,
            (MotionType.PRO, 0.5, Orientation.OUT): Orientation.COUNTER,
            (MotionType.PRO, 1.5, Orientation.OUT): Orientation.CLOCK,
            (MotionType.PRO, 2.5, Orientation.OUT): Orientation.COUNTER,
            (MotionType.ANTI, 0.5, Orientation.IN): Orientation.COUNTER,
            (MotionType.ANTI, 1.5, Orientation.IN): Orientation.CLOCK,
            (MotionType.ANTI, 2.5, Orientation.IN): Orientation.COUNTER,
            (MotionType.ANTI, 0.5, Orientation.OUT): Orientation.CLOCK,
            (MotionType.ANTI, 1.5, Orientation.OUT): Orientation.COUNTER,
            (MotionType.ANTI, 2.5, Orientation.OUT): Orientation.CLOCK,
            (MotionType.PRO, 0.5, Orientation.CLOCK): Orientation.OUT,
            (MotionType.PRO, 1.5, Orientation.CLOCK): Orientation.IN,
            (MotionType.PRO, 2.5, Orientation.CLOCK): Orientation.OUT,
            (MotionType.PRO, 0.5, Orientation.COUNTER): Orientation.IN,
            (MotionType.PRO, 1.5, Orientation.COUNTER): Orientation.OUT,
            (MotionType.PRO, 2.5, Orientation.COUNTER): Orientation.IN,
            (MotionType.ANTI, 0.5, Orientation.CLOCK): Orientation.IN,
            (MotionType.ANTI, 1.5, Orientation.CLOCK): Orientation.OUT,
            (MotionType.ANTI, 2.5, Orientation.CLOCK): Orientation.IN,
            (MotionType.ANTI, 0.5, Orientation.COUNTER): Orientation.OUT,
            (MotionType.ANTI, 1.5, Orientation.COUNTER): Orientation.IN,
            (MotionType.ANTI, 2.5, Orientation.COUNTER): Orientation.OUT,
        }

        float_map = {
            (Orientation.IN, "cw_hp"): Orientation.CLOCK,
            (Orientation.IN, "ccw_hp"): Orientation.COUNTER,
            (Orientation.OUT, "cw_hp"): Orientation.COUNTER,
            (Orientation.OUT, "ccw_hp"): Orientation.CLOCK,
            (Orientation.CLOCK, "cw_hp"): Orientation.OUT,
            (Orientation.CLOCK, "ccw_hp"): Orientation.IN,
            (Orientation.COUNTER, "cw_hp"): Orientation.IN,
            (Orientation.COUNTER, "ccw_hp"): Orientation.OUT,
        }

        def get_handpath_direction(
            start_location, end_location
        ) -> Literal["cw_hp", "ccw_hp"]:
            clockwise_paths = [("n", "e"), ("e", "s"), ("s", "w"), ("w", "n")]
            return (
                "cw_hp"
                if (start_location, end_location) in clockwise_paths
                else "ccw_hp"
            )

        handpath_direction = get_handpath_direction(
            self.start_location, self.end_location
        )
        if self.motion_type == MotionType.FLOAT:
            key = (self.start_orientation, handpath_direction)
            return float_map.get(key)

        elif self.turns in [0, 1, 2, 3] or self.turns in ["0", "1", "2", "3"]:
            # For pro and anti motions
            if self.motion_type in [PRO, ANTI]:
                key = (self.motion_type, int(self.turns), self.start_orientation)
                return whole_turn_orientation_map.get(key)

            # For static motion
            if self.motion_type == STATIC:
                key = (MotionType.PRO, int(self.turns), self.start_orientation)
                return whole_turn_orientation_map.get(key)

            # For dash motion
            if self.motion_type == DASH:
                key = (ANTI, int(self.turns), self.start_orientation)
                return whole_turn_orientation_map.get(key)

        elif self.turns in [0.5, 1.5, 2.5] or self.turns in ["0.5", "1.5", "2.5"]:
            if handpath_direction == "cw_hp":
                map_to_use = clockwise_handpath_half_turns_map
            else:
                map_to_use = counter_handpath_half_turns_map

            if self.motion_type in [PRO, ANTI]:
                key = (self.motion_type, float(self.turns), self.start_orientation)
                return map_to_use.get(key)

            if self.motion_type == STATIC:
                key = (MotionType.PRO, float(self.turns), self.start_orientation)
                return map_to_use.get(key)

            elif self.motion_type == DASH:
                key = (ANTI, float(self.turns), self.start_orientation)
                return map_to_use.get(key)

    def get_arrow_location(self, start_location: str, end_location: str) -> str:
        if self.arrow:
            if start_location == end_location:
                return start_location

            direction_map = {
                ("n", "e"): "ne",
                ("e", "s"): "se",
                ("s", "w"): "sw",
                ("w", "n"): "nw",
                ("n", "w"): "nw",
                ("w", "s"): "sw",
                ("s", "e"): "se",
                ("e", "n"): "ne",
            }

            return direction_map.get(
                (start_location, end_location)
            ) or direction_map.get((end_location, start_location))

    ### MANIPULATORS ###

    def adjust_turns(self, adjustment: float) -> None:
        potential_new_turns = self.arrow.turns + adjustment
        new_turns_float: float = max(0, min(3, potential_new_turns))

        if new_turns_float % 1 == 0:
            new_turns_int: int = int(new_turns_float)
            if new_turns_int != self.arrow.turns:
                self.update_turns(new_turns_int)
        else:
            if new_turns_float != self.arrow.turns:
                self.update_turns(new_turns_float)

    def add_half_turn(self) -> None:
        self.adjust_turns(0.5)

    def subtract_half_turn(self) -> None:
        self.adjust_turns(-0.5)

    def add_turn(self) -> None:
        self.adjust_turns(1)

    def subtract_turn(self) -> None:
        self.adjust_turns(-1)
