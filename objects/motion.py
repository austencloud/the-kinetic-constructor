from utilities.TypeChecking.TypeChecking import (
    Axes,
    MotionAttributesDicts,
    Colors,
    MotionTypes,
    Turns,
    RotationDirections,
    Locations,
    Locations,
    Orientations,
)
from constants.string_constants import *
from typing import TYPE_CHECKING, Literal, Union


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
    ) -> None:
        self.scene = scene
        self.motion_dict = motion_dict

        self.setup_attributes(motion_dict)

    ### SETUP ###

    def setup_attributes(self, motion_dict) -> None:
        if ARROW in motion_dict and PROP in motion_dict:
            if motion_dict[ARROW] and motion_dict[PROP]:
                self.arrow.motion = self
                self.prop.motion = self
                self.arrow: Arrow = motion_dict[ARROW]
                self.prop: Prop = motion_dict[PROP]
        else:
            self.arrow: Arrow = None
            self.prop: Prop = None

        self.color: Colors = motion_dict[COLOR]
        self.motion_type: MotionTypes = motion_dict[MOTION_TYPE]
        self.turns: Turns = motion_dict[TURNS]
        self.rotation_direction: RotationDirections = motion_dict[ROTATION_DIRECTION]
        self.start_location: Locations = motion_dict[START_LOCATION]
        self.end_location: Locations = motion_dict[END_LOCATION]
        self.start_orientation: Orientations = motion_dict[START_ORIENTATION]

        self.assign_location_to_arrow()

        self.end_orientation: Orientations = self.get_end_orientation()
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
            self.prop.axis: Axes = self.prop.update_axis_from_orientation(
                self.prop.location
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
            COLOR: self.color,
            MOTION_TYPE: self.motion_type,
            TURNS: self.turns,
            ROTATION_DIRECTION: self.rotation_direction,
            START_LOCATION: self.start_location,
            END_LOCATION: self.end_location,
            START_ORIENTATION: self.start_orientation,
            END_ORIENTATION: self.end_orientation,
        }


    def get_end_orientation(self) -> Orientations:
        # Combine layer1 maps

        # Combine layer1 maps
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
            (PRO, 0, CLOCKWISE): CLOCKWISE,
            (PRO, 1, CLOCKWISE): COUNTER_CLOCKWISE,
            (PRO, 2, CLOCKWISE): CLOCKWISE,
            (PRO, 3, CLOCKWISE): COUNTER_CLOCKWISE,
            (PRO, 0, COUNTER_CLOCKWISE): COUNTER_CLOCKWISE,
            (PRO, 1, COUNTER_CLOCKWISE): CLOCKWISE,
            (PRO, 2, COUNTER_CLOCKWISE): COUNTER_CLOCKWISE,
            (PRO, 3, COUNTER_CLOCKWISE): CLOCKWISE,
            (ANTI, 0, CLOCKWISE): COUNTER_CLOCKWISE,
            (ANTI, 1, CLOCKWISE): CLOCKWISE,
            (ANTI, 2, CLOCKWISE): COUNTER_CLOCKWISE,
            (ANTI, 3, CLOCKWISE): CLOCKWISE,
            (ANTI, 0, COUNTER_CLOCKWISE): CLOCKWISE,
            (ANTI, 1, COUNTER_CLOCKWISE): COUNTER_CLOCKWISE,
            (ANTI, 2, COUNTER_CLOCKWISE): CLOCKWISE,
            (ANTI, 3, COUNTER_CLOCKWISE): COUNTER_CLOCKWISE,
        }

        # Combine layer2 maps

        # ({HANDPATH_DIRECTION}, {START_ORIENTATION}, {END_ORIENTATION}})
        clockwise_handpath_half_turns_map = {
            (PRO, 0.5, IN): COUNTER_CLOCKWISE,
            (PRO, 1.5, IN): CLOCKWISE,
            (PRO, 2.5, IN): COUNTER_CLOCKWISE,
            (PRO, 0.5, OUT): CLOCKWISE,
            (PRO, 1.5, OUT): COUNTER_CLOCKWISE,
            (PRO, 2.5, OUT): CLOCKWISE,
            (ANTI, 0.5, IN): CLOCKWISE,
            (ANTI, 1.5, IN): COUNTER_CLOCKWISE,
            (ANTI, 2.5, IN): CLOCKWISE,
            (ANTI, 0.5, OUT): COUNTER_CLOCKWISE,
            (ANTI, 1.5, OUT): CLOCKWISE,
            (ANTI, 2.5, OUT): COUNTER_CLOCKWISE,
            (PRO, 0.5, CLOCKWISE): IN,
            (PRO, 1.5, CLOCKWISE): OUT,
            (PRO, 2.5, CLOCKWISE): IN,
            (PRO, 0.5, COUNTER_CLOCKWISE): OUT,
            (PRO, 1.5, COUNTER_CLOCKWISE): IN,
            (PRO, 2.5, COUNTER_CLOCKWISE): OUT,
            (ANTI, 0.5, CLOCKWISE): OUT,
            (ANTI, 1.5, CLOCKWISE): IN,
            (ANTI, 2.5, CLOCKWISE): OUT,
            (ANTI, 0.5, COUNTER_CLOCKWISE): IN,
            (ANTI, 1.5, COUNTER_CLOCKWISE): OUT,
            (ANTI, 2.5, COUNTER_CLOCKWISE): IN,
        }

        counter_handpath_half_turns_map = {
            (PRO, 0.5, IN): CLOCKWISE,
            (PRO, 1.5, IN): COUNTER_CLOCKWISE,
            (PRO, 2.5, IN): CLOCKWISE,
            (PRO, 0.5, OUT): COUNTER_CLOCKWISE,
            (PRO, 1.5, OUT): CLOCKWISE,
            (PRO, 2.5, OUT): COUNTER_CLOCKWISE,
            (ANTI, 0.5, IN): COUNTER_CLOCKWISE,
            (ANTI, 1.5, IN): CLOCKWISE,
            (ANTI, 2.5, IN): COUNTER_CLOCKWISE,
            (ANTI, 0.5, OUT): CLOCKWISE,
            (ANTI, 1.5, OUT): COUNTER_CLOCKWISE,
            (ANTI, 2.5, OUT): CLOCKWISE,
            (PRO, 0.5, CLOCKWISE): OUT,
            (PRO, 1.5, CLOCKWISE): IN,
            (PRO, 2.5, CLOCKWISE): OUT,
            (PRO, 0.5, COUNTER_CLOCKWISE): IN,
            (PRO, 1.5, COUNTER_CLOCKWISE): OUT,
            (PRO, 2.5, COUNTER_CLOCKWISE): IN,
            (ANTI, 0.5, CLOCKWISE): IN,
            (ANTI, 1.5, CLOCKWISE): OUT,
            (ANTI, 2.5, CLOCKWISE): IN,
            (ANTI, 0.5, COUNTER_CLOCKWISE): OUT,
            (ANTI, 1.5, COUNTER_CLOCKWISE): IN,
            (ANTI, 2.5, COUNTER_CLOCKWISE): OUT,
        }


        float_map = {
            (IN, "cw_hp"): CLOCKWISE,
            (IN, "ccw_hp"): COUNTER_CLOCKWISE,
            (OUT, "cw_hp"): COUNTER_CLOCKWISE,
            (OUT, "ccw_hp"): CLOCKWISE,
            (CLOCKWISE, "cw_hp"): OUT,
            (CLOCKWISE, "ccw_hp"): IN,
            (COUNTER_CLOCKWISE, "cw_hp"): IN,
            (COUNTER_CLOCKWISE, "ccw_hp"): OUT,
        }

        def get_handpath_direction(start_location, end_location) -> Literal['cw_hp', 'ccw_hp']:
            clockwise_paths = [("n", "e"), ("e", "s"), ("s", "w"), ("w", "n")]
            return "cw_hp" if (start_location, end_location) in clockwise_paths else "ccw_hp"

        handpath_direction = get_handpath_direction(self.start_location, self.end_location)
        if self.motion_type == FLOAT:
            key = (self.start_orientation, handpath_direction)
            return float_map.get(key)

        elif self.turns in [0, 1, 2, 3]:
            # For pro and anti motions
            if self.motion_type in [PRO, ANTI]:
                key = (self.motion_type, self.turns, self.start_orientation)
                return whole_turn_orientation_map.get(key)

            # For static motion
            if self.motion_type == STATIC:
                key = (PRO, self.turns, self.start_orientation)
                return whole_turn_orientation_map.get(key)

            # For dash motion
            if self.motion_type == DASH:
                key = (ANTI, self.turns, self.start_orientation)
                return whole_turn_orientation_map.get(key)

        elif self.turns in [0.5, 1.5, 2.5]:
            if handpath_direction == "cw_hp":
                map_to_use = clockwise_handpath_half_turns_map
            else:
                map_to_use = counter_handpath_half_turns_map

            if self.motion_type in [PRO, ANTI]:
                key = (self.motion_type, self.turns, self.start_orientation)
                return map_to_use.get(key)

            if self.motion_type == STATIC:
                key = (PRO, self.turns, self.start_orientation)
                return map_to_use.get(key)

            elif self.motion_type == DASH:
                key = (ANTI, self.turns, self.start_orientation)
                return map_to_use.get(key)



        # For float motion, determine handpath direction
        if self.motion_type == FLOAT:
            handpath_direction = get_handpath_direction(self.start_location, self.end_location)
            key = (self.start_orientation, handpath_direction)
            return float_map.get(key)

        # For pro and anti motions with whole turns
        if self.turns in [0, 1, 2, 3]:
            key = (self.motion_type, self.turns, self.start_orientation)
            return whole_turn_orientation_map.get(key)

        # For half turns, determine handpath direction
        elif self.turns in [0.5, 1.5, 2.5]:
            handpath_direction = get_handpath_direction(self.start_location, self.end_location)
            if handpath_direction == "cw_hp":
                map_to_use = clockwise_handpath_half_turns_map
            else:
                map_to_use = counter_handpath_half_turns_map

            key = (self.motion_type, self.turns, self.start_orientation)
            return map_to_use.get(key)

        # For static and dash motions
        if self.motion_type == STATIC:
            return self.start_orientation
        if self.motion_type == DASH:
            key = (ANTI, self.turns, self.start_orientation)
            return whole_turn_orientation_map.get(key)

        return None  # Default case if none match

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
