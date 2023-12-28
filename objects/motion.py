from Enums import (
    MotionAttributesDicts,
    MotionType,
    Orientation,
)

from constants import *
from typing import TYPE_CHECKING, Dict, Literal, Union


if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from objects.arrow.arrow import Arrow
    from objects.prop.prop import Prop
    from widgets.graph_editor_tab.object_panel.arrowbox.arrowbox import ArrowBox


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
        self.color: COLOR = motion_dict["color"]

        if not blank:
            self.setup_attributes(motion_dict)

    def initialize_attributes(self):
        self.arrow: Arrow = None
        self.prop: Prop = None
        self.color: COLOR = None
        self.motion_type: MOTION_TYPE = None
        self.turns: TURNS = None
        self.rot_dir: ROT_DIR = None
        self.start_location: START_LOC = None
        self.end_location: END_LOC = None
        self.start_orientation: START_OR = None
        self.end_orientation: END_OR = None

    ### SETUP ###

    def setup_attributes(self, motion_dict: Dict) -> None:
        self.arrow = motion_dict.get(ARROW)
        self.prop = motion_dict.get(PROP)

        if self.arrow and self.prop:
            self.arrow.motion = self
            self.prop.motion = self
        else:
            self.arrow = None
            self.prop = None

        self.motion_type: MOTION_TYPE = motion_dict[MOTION_TYPE]
        self.turns: TURNS = motion_dict[TURNS]
        self.rot_dir: ROT_DIR = motion_dict[ROT_DIR]
        self.start_location: START_LOC = motion_dict[START_LOC]
        self.end_location: END_LOC = motion_dict[END_LOC]
        self.start_orientation: START_OR = motion_dict[START_OR]

        self.assign_location_to_arrow()

        self.end_orientation: END_OR = self.get_end_orientation()
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
        self.arrow.arrow_dict[TURNS] = self.arrow.turns
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
            self.prop.axis = self.prop.get_axis_from_orientation(
                self.prop.orientation, self.prop.location
            )
            self.prop.update_rotation()
            self.prop.update_appearance()

    def clear_attributes(self):
        self.start_location = None
        self.end_location = None
        self.turns = None
        self.motion_type = None

        self.rot_dir = None
        self.start_orientation = None
        self.end_orientation = None

    ### GETTERS ###

    def get_attributes(self) -> MotionAttributesDicts:
        return {
            COLOR: self.color,
            MOTION_TYPE: self.motion_type,
            TURNS: self.turns,
            ROT_DIR: self.rot_dir,
            START_LOC: self.start_location,
            END_LOC: self.end_location,
            START_OR: self.start_orientation,
            END_OR: self.end_orientation,
        }

    def get_end_orientation(self) -> Orientation:
        whole_turn_orientation_map = {
            (PRO, 0, IN): IN,
            (PRO, 1, IN): OUT,
            (PRO, 2, IN): IN,
            (PRO, 3, IN): OUT,
            (PRO, 0, OUT): OUT,
            (PRO, 1, OUT): IN,
            (PRO, 2, OUT): OUT,
            (PRO, 3, OUT): IN,
            (ANTI, 0, IN): OUT,
            (ANTI, 1, IN): IN,
            (ANTI, 2, IN): OUT,
            (ANTI, 3, IN): IN,
            (ANTI, 0, OUT): IN,
            (ANTI, 1, OUT): OUT,
            (ANTI, 2, OUT): IN,
            (ANTI, 3, OUT): OUT,
            (PRO, 0, CLOCK): CLOCK,
            (PRO, 1, CLOCK): COUNTER,
            (PRO, 2, CLOCK): CLOCK,
            (PRO, 3, CLOCK): COUNTER,
            (PRO, 0, COUNTER): COUNTER,
            (PRO, 1, COUNTER): CLOCK,
            (PRO, 2, COUNTER): COUNTER,
            (PRO, 3, COUNTER): CLOCK,
            (ANTI, 0, CLOCK): COUNTER,
            (ANTI, 1, CLOCK): CLOCK,
            (ANTI, 2, CLOCK): COUNTER,
            (ANTI, 3, CLOCK): CLOCK,
            (ANTI, 0, COUNTER): CLOCK,
            (ANTI, 1, COUNTER): COUNTER,
            (ANTI, 2, COUNTER): CLOCK,
            (ANTI, 3, COUNTER): COUNTER,
        }

        clockwise_handpath_half_turns_map = {
            (PRO, 0.5, IN): COUNTER,
            (PRO, 1.5, IN): CLOCK,
            (PRO, 2.5, IN): COUNTER,
            (PRO, 0.5, OUT): CLOCK,
            (PRO, 1.5, OUT): COUNTER,
            (PRO, 2.5, OUT): CLOCK,
            (ANTI, 0.5, IN): CLOCK,
            (ANTI, 1.5, IN): COUNTER,
            (ANTI, 2.5, IN): CLOCK,
            (ANTI, 0.5, OUT): COUNTER,
            (ANTI, 1.5, OUT): CLOCK,
            (ANTI, 2.5, OUT): COUNTER,
            (PRO, 0.5, CLOCK): IN,
            (PRO, 1.5, CLOCK): OUT,
            (PRO, 2.5, CLOCK): IN,
            (PRO, 0.5, COUNTER): OUT,
            (PRO, 1.5, COUNTER): IN,
            (PRO, 2.5, COUNTER): OUT,
            (ANTI, 0.5, CLOCK): OUT,
            (ANTI, 1.5, CLOCK): IN,
            (ANTI, 2.5, CLOCK): OUT,
            (ANTI, 0.5, COUNTER): IN,
            (ANTI, 1.5, COUNTER): OUT,
            (ANTI, 2.5, COUNTER): IN,
        }

        counter_handpath_half_turns_map = {
            (PRO, 0.5, IN): CLOCK,
            (PRO, 1.5, IN): COUNTER,
            (PRO, 2.5, IN): CLOCK,
            (PRO, 0.5, OUT): COUNTER,
            (PRO, 1.5, OUT): CLOCK,
            (PRO, 2.5, OUT): COUNTER,
            (ANTI, 0.5, IN): COUNTER,
            (ANTI, 1.5, IN): CLOCK,
            (ANTI, 2.5, IN): COUNTER,
            (ANTI, 0.5, OUT): CLOCK,
            (ANTI, 1.5, OUT): COUNTER,
            (ANTI, 2.5, OUT): CLOCK,
            (PRO, 0.5, CLOCK): OUT,
            (PRO, 1.5, CLOCK): IN,
            (PRO, 2.5, CLOCK): OUT,
            (PRO, 0.5, COUNTER): IN,
            (PRO, 1.5, COUNTER): OUT,
            (PRO, 2.5, COUNTER): IN,
            (ANTI, 0.5, CLOCK): IN,
            (ANTI, 1.5, CLOCK): OUT,
            (ANTI, 2.5, CLOCK): IN,
            (ANTI, 0.5, COUNTER): OUT,
            (ANTI, 1.5, COUNTER): IN,
            (ANTI, 2.5, COUNTER): OUT,
        }

        float_map = {
            (IN, "cw_hp"): CLOCK,
            (IN, "ccw_hp"): COUNTER,
            (OUT, "cw_hp"): COUNTER,
            (OUT, "ccw_hp"): CLOCK,
            (CLOCK, "cw_hp"): OUT,
            (CLOCK, "ccw_hp"): IN,
            (COUNTER, "cw_hp"): IN,
            (COUNTER, "ccw_hp"): OUT,
        }

        def get_handpath_direction(
            start_location, end_location
        ) -> Literal["cw_hp", "ccw_hp"]:
            clockwise_handpaths = [("n", "e"), ("e", "s"), ("s", "w"), ("w", "n")]
            counter_clockwise_handpaths = [
                ("n", "w"),
                ("w", "s"),
                ("s", "e"),
                ("e", "n"),
            ]
            if (start_location, end_location) in clockwise_handpaths:
                return "cw_hp"
            elif (start_location, end_location) in counter_clockwise_handpaths:
                return "ccw_hp"
            elif start_location == end_location:
                return None
            else:
                print("Unrecognized handpath direction")

        handpath_direction = get_handpath_direction(
            self.start_location, self.end_location
        )
        if self.motion_type == MotionType.FLOAT:
            key = (self.start_orientation, handpath_direction)
            return float_map.get(key)
        elif self.turns in [0, 1, 2, 3] or self.turns in ["0", "1", "2", "3"]:
            if self.motion_type in [PRO, ANTI]:
                key = (self.motion_type, int(self.turns), self.start_orientation)
                return whole_turn_orientation_map.get(key)
            if self.motion_type == STATIC:
                key = (PRO, int(self.turns), self.start_orientation)
                return whole_turn_orientation_map.get(key)
            if self.motion_type == MotionType.DASH:
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
                key = (PRO, float(self.turns), self.start_orientation)
                return map_to_use.get(key)

            elif self.motion_type == MotionType.DASH:
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
