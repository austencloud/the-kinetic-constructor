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
    Layers,
)
from constants.string_constants import *
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
    from objects.arrow.arrow import Arrow
    from objects.prop.prop import Prop
    from widgets.graph_editor.object_panel.arrowbox.arrowbox import ArrowBox


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
        self.start_layer: Layers = motion_dict[START_LAYER]

        if hasattr(self, "arrow") and self.arrow:
            self.arrow.location = self.get_arrow_location(
                self.start_location, self.end_location
            )

        self.end_orientation: Orientations = self.get_end_orientation()
        self.end_layer: Layers = self.get_end_layer()
        self.update_prop_orientation_and_layer()

    ### UPDATE ###

    def update_attr_from_arrow(self) -> None:
        self.color = self.arrow.color
        self.motion_type = self.arrow.motion_type
        self.turns = self.arrow.turns

    def update_turns(self, turns: int) -> None:
        self.arrow.turns = turns
        self.turns = self.arrow.turns
        self.end_orientation = self.get_end_orientation()
        self.update_prop_orientation_and_layer()
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

    def update_prop_orientation_and_layer(self) -> None:
        if hasattr(self, "prop") and self.prop:
            self.prop.orientation = self.end_orientation
            self.prop.layer = self.end_layer
            self.prop.location = self.end_location
            self.prop.axis: Axes = self.prop.update_axis_from_layer(self.prop.location)
            self.prop.update_rotation()
            self.prop.update_appearance()

    def clear_attributes(self):
        self.start_location = None
        self.end_location = None
        self.turns = None
        self.motion_type = None
        self.start_layer = None
        self.end_layer = None
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
            START_LAYER: self.start_layer,
            END_LAYER: self.end_layer,
        }

    def get_end_layer(self) -> Layers:
        if self.start_layer:
            if self.turns or self.turns == 0:
                if self.turns in [0, 1, 2]:
                    end_layer = self.start_layer
                elif self.turns in [0.5, 1.5]:
                    end_layer = 3 - self.start_layer  # Switches between 1 and 2
                return end_layer

    def get_end_orientation(self) -> Orientations:
        anti_orientation_map = {
            (0, IN): OUT,
            (0.5, IN): COUNTER_CLOCKWISE,
            (1, IN): OUT,
            (1.5, IN): COUNTER_CLOCKWISE,
            (2, IN): OUT,
            (2.5, IN): COUNTER_CLOCKWISE,
            (3, IN): OUT,
            (0, OUT): IN,
            (0.5, OUT): CLOCKWISE,
            (1, OUT): IN,
            (1.5, OUT): CLOCKWISE,
            (2, OUT): IN,
            (2.5, OUT): CLOCKWISE,
            (3, OUT): IN,
        }

        pro_orientation_map = {
            (0, IN): IN,
            (0.5, IN): CLOCKWISE,
            (1, IN): IN,
            (1.5, IN): CLOCKWISE,
            (2, IN): IN,
            (2.5, IN): CLOCKWISE,
            (3, IN): IN,
            (0, OUT): OUT,
            (0.5, OUT): COUNTER_CLOCKWISE,
            (1, OUT): OUT,
            (1.5, OUT): COUNTER_CLOCKWISE,
            (2, OUT): OUT,
            (2.5, OUT): COUNTER_CLOCKWISE,
            (3, OUT): OUT,
        }

        float_orientation_map_layer_1 = {
            (IN, "n", "e"): CLOCKWISE,
            (IN, "e", "s"): CLOCKWISE,
            (IN, "s", "w"): CLOCKWISE,
            (IN, "w", "n"): CLOCKWISE,
            (IN, "n", "w"): COUNTER_CLOCKWISE,
            (IN, "w", "s"): COUNTER_CLOCKWISE,
            (IN, "s", "e"): COUNTER_CLOCKWISE,
            (IN, "e", "n"): COUNTER_CLOCKWISE,
            (OUT, "n", "e"): COUNTER_CLOCKWISE,
            (OUT, "e", "s"): COUNTER_CLOCKWISE,
            (OUT, "s", "w"): COUNTER_CLOCKWISE,
            (OUT, "w", "n"): COUNTER_CLOCKWISE,
            (OUT, "n", "w"): CLOCKWISE,
            (OUT, "w", "s"): CLOCKWISE,
            (OUT, "s", "e"): CLOCKWISE,
            (OUT, "e", "n"): CLOCKWISE,
        }

        float_orientation_map_layer_2 = {
            (CLOCKWISE, "n", "e"): OUT,
            (CLOCKWISE, "e", "s"): OUT,
            (CLOCKWISE, "s", "w"): OUT,
            (CLOCKWISE, "w", "n"): OUT,
            (CLOCKWISE, "n", "w"): IN,
            (CLOCKWISE, "w", "s"): IN,
            (CLOCKWISE, "s", "e"): IN,
            (CLOCKWISE, "e", "n"): IN,
            (COUNTER_CLOCKWISE, "n", "e"): IN,
            (COUNTER_CLOCKWISE, "e", "s"): IN,
            (COUNTER_CLOCKWISE, "s", "w"): IN,
            (COUNTER_CLOCKWISE, "w", "n"): IN,
            (COUNTER_CLOCKWISE, "n", "w"): OUT,
            (COUNTER_CLOCKWISE, "w", "s"): OUT,
            (COUNTER_CLOCKWISE, "s", "e"): OUT,
            (COUNTER_CLOCKWISE, "e", "n"): OUT,
        }

        if self.rotation_direction is not None:
            key = (self.turns, self.start_orientation)
            if self.motion_type in [PRO, STATIC]:
                end_orientation = pro_orientation_map.get(key)
            elif self.motion_type in [ANTI, DASH]:
                end_orientation = anti_orientation_map.get(key)
            return end_orientation

        elif self.rotation_direction is None:
            if self.motion_type == STATIC:
                return self.start_orientation
            elif self.motion_type == DASH:
                return OUT if self.start_orientation == IN else IN
            elif self.motion_type == FLOAT:
                if self.start_layer == 1:
                    key = (
                        self.start_orientation,
                        self.start_location,
                        self.end_location,
                    )
                    return float_orientation_map_layer_1.get(
                        key, self.start_orientation
                    )
                elif self.start_layer == 2:
                    key = (
                        self.start_orientation,
                        self.start_location,
                        self.end_location,
                    )
                    return float_orientation_map_layer_2.get(
                        key, self.start_orientation
                    )

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
            self.end_layer = 1 if self.start_layer == 1 else 2
            new_turns_int: int = int(new_turns_float)
            if new_turns_int != self.arrow.turns:
                self.update_turns(new_turns_int)
        else:
            self.end_layer = 2 if self.start_layer == 1 else 1
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
