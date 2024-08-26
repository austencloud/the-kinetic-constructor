from typing import TYPE_CHECKING
from data.constants import *
from objects.motion.motion import Motion

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph


class BaseTurnsTupleGenerator:
    def _normalize_turns(self, motion: Motion) -> int:
        return (
            int(motion.turns) if motion.turns in {0.0, 1.0, 2.0, 3.0} else motion.turns
        )

    def set_pictograph(self, pictograph: "BasePictograph"):
        self.p = pictograph

        self.blue_motion = self.p.motions.get(BLUE)
        self.red_motion = self.p.motions.get(RED)

    def generate_turns_tuple(self, pictograph) -> str:
        pass  # implemented in subclasses


class Type1HybridTurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph) -> str:
        super().set_pictograph(pictograph)
        pro_motion = (
            self.blue_motion if self.blue_motion.motion_type == PRO else self.red_motion
        )
        anti_motion = (
            self.blue_motion
            if self.blue_motion.motion_type == ANTI
            else self.red_motion
        )
        return f"({pro_motion.turns}, {anti_motion.turns})"


class Type2TurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph) -> str:
        super().set_pictograph(pictograph)
        shift = (
            self.red_motion if self.red_motion.check.is_shift() else self.blue_motion
        )
        static = (
            self.red_motion if self.red_motion.check.is_static() else self.blue_motion
        )
        if static.turns != 0 and static.prop_rot_dir != NO_ROT:
            direction = "s" if static.prop_rot_dir == shift.prop_rot_dir else "o"
            return f"({direction}, {self._normalize_turns(shift)}, {self._normalize_turns(static)})"
        else:
            return f"({self._normalize_turns(shift)}, {self._normalize_turns(static)})"


class Type3TurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph) -> str:
        super().set_pictograph(pictograph)
        shift = self.p.get.shift()
        dash = self.p.get.dash()
        direction = "s" if dash.prop_rot_dir == shift.prop_rot_dir else "o"
        if dash.turns > 0 and shift.turns > 0:
            return f"({direction}, {self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
        elif dash.turns > 0:
            return f"({direction}, {self._normalize_turns(shift)}, {self._normalize_turns(dash)})"
        else:
            return f"({self._normalize_turns(shift)}, {self._normalize_turns(dash)})"


class Type4TurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph) -> str:
        super().set_pictograph(pictograph)
        dash = self.p.get.dash()
        static = self.p.get.static()
        if dash.turns == 0 and static.turns == 0:
            return f"({self._normalize_turns(dash)}, {self._normalize_turns(static)})"
        elif dash.turns == 0 or static.turns == 0:
            turning_motion = dash if dash.turns != 0 else static
            return f"({turning_motion.prop_rot_dir}, {self._normalize_turns(dash)}, {self._normalize_turns(static)})"
        else:
            direction = "s" if dash.prop_rot_dir == static.prop_rot_dir else "o"
            return f"({direction}, {self._normalize_turns(dash)}, {self._normalize_turns(static)})"


class Type56TurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph) -> str:
        super().set_pictograph(pictograph)
        if self.blue_motion.turns == 0 and self.red_motion.turns == 0:
            return f"({self._normalize_turns(self.blue_motion)}, {self._normalize_turns(self.red_motion)})"
        elif self.blue_motion.turns == 0 or self.red_motion.turns == 0:
            turning_motion = (
                self.blue_motion if self.blue_motion.turns != 0 else self.red_motion
            )
            return f"({turning_motion.prop_rot_dir}, {self._normalize_turns(self.blue_motion)}, {self._normalize_turns(self.red_motion)})"
        else:
            direction = (
                "s"
                if self.blue_motion.prop_rot_dir == self.red_motion.prop_rot_dir
                else "o"
            )
            return f"({direction}, {self._normalize_turns(self.blue_motion)}, {self._normalize_turns(self.red_motion)})"


class ColorTurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph) -> str:
        super().set_pictograph(pictograph)
        return f"({self._normalize_turns(self.blue_motion)}, {self._normalize_turns(self.red_motion)})"


class LeadStateTurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph) -> str:
        super().set_pictograph(pictograph)
        leading_motion = self.p.get.leading_motion()
        trailing_motion = self.p.get.trailing_motion()
        if leading_motion:
            return f"({leading_motion.turns}, {trailing_motion.turns})"
        else:
            return f"({self._normalize_turns(self.blue_motion)}, {self._normalize_turns(self.red_motion)})"


class LambdaTurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph) -> str:
        super().set_pictograph(pictograph)
        dash = self.p.get.dash()
        static = self.p.get.static()
        dash_direction_map, static_direction_map = self._get_direction_maps()

        if dash.turns == 0 and static.turns > 0:
            open_close_state = static_direction_map.get(
                (dash.end_loc, static.end_loc, static.prop_rot_dir), ""
            )
            return f"({self._normalize_turns(dash)}, {self._normalize_turns(static)}, {open_close_state})"
        elif static.turns == 0 and dash.turns > 0:
            open_close_state = dash_direction_map.get(
                (dash.end_loc, static.end_loc, dash.prop_rot_dir), ""
            )
            return f"({self._normalize_turns(dash)}, {self._normalize_turns(static)}, {open_close_state})"
        elif static.turns > 0 and dash.turns > 0:
            static_open_close_state = static_direction_map.get(
                (dash.end_loc, static.end_loc, static.prop_rot_dir), ""
            )
            dash_open_close_state = dash_direction_map.get(
                (dash.end_loc, static.end_loc, dash.prop_rot_dir), ""
            )
            vtg_dir = "s" if static.prop_rot_dir == dash.prop_rot_dir else "o"
            return f"({vtg_dir}, {self._normalize_turns(dash)}, {self._normalize_turns(static)}, {dash_open_close_state}, {static_open_close_state})"
        else:
            return f"({self._normalize_turns(dash)}, {self._normalize_turns(static)})"

    def _get_direction_maps(self):
        dash_direction_map = {
            (EAST, NORTH, CLOCKWISE): OPENING,
            (EAST, NORTH, COUNTER_CLOCKWISE): CLOSING,
            (EAST, SOUTH, CLOCKWISE): CLOSING,
            (EAST, SOUTH, COUNTER_CLOCKWISE): OPENING,
            (WEST, NORTH, CLOCKWISE): CLOSING,
            (WEST, NORTH, COUNTER_CLOCKWISE): OPENING,
            (WEST, SOUTH, CLOCKWISE): OPENING,
            (WEST, SOUTH, COUNTER_CLOCKWISE): CLOSING,
            (NORTH, EAST, CLOCKWISE): CLOSING,
            (NORTH, EAST, COUNTER_CLOCKWISE): OPENING,
            (NORTH, WEST, CLOCKWISE): OPENING,
            (NORTH, WEST, COUNTER_CLOCKWISE): CLOSING,
            (SOUTH, EAST, CLOCKWISE): OPENING,
            (SOUTH, EAST, COUNTER_CLOCKWISE): CLOSING,
            (SOUTH, WEST, CLOCKWISE): CLOSING,
            (SOUTH, WEST, COUNTER_CLOCKWISE): OPENING,
        }
        static_direction_map = {
            (EAST, NORTH, CLOCKWISE): CLOSING,
            (EAST, NORTH, COUNTER_CLOCKWISE): OPENING,
            (EAST, SOUTH, CLOCKWISE): OPENING,
            (EAST, SOUTH, COUNTER_CLOCKWISE): CLOSING,
            (WEST, NORTH, CLOCKWISE): OPENING,
            (WEST, NORTH, COUNTER_CLOCKWISE): CLOSING,
            (WEST, SOUTH, CLOCKWISE): CLOSING,
            (WEST, SOUTH, COUNTER_CLOCKWISE): OPENING,
            (NORTH, EAST, CLOCKWISE): OPENING,
            (NORTH, EAST, COUNTER_CLOCKWISE): CLOSING,
            (NORTH, WEST, CLOCKWISE): CLOSING,
            (NORTH, WEST, COUNTER_CLOCKWISE): OPENING,
            (SOUTH, EAST, CLOCKWISE): CLOSING,
            (SOUTH, EAST, COUNTER_CLOCKWISE): OPENING,
            (SOUTH, WEST, CLOCKWISE): OPENING,
            (SOUTH, WEST, COUNTER_CLOCKWISE): CLOSING,
        }
        return dash_direction_map, static_direction_map


class LambdaDashTurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph) -> str:
        super().set_pictograph(pictograph)
        blue_dash = self.p.blue_motion
        red_dash = self.p.red_motion
        blue_dash_map, red_dash_map = self._get_direction_maps()

        if blue_dash.turns == 0 and red_dash.turns > 0:
            red_dash_state = red_dash_map.get(
                (blue_dash.end_loc, red_dash.end_loc, red_dash.prop_rot_dir), ""
            )
            return f"({self._normalize_turns(blue_dash)}, {self._normalize_turns(red_dash)}, {red_dash_state})"
        elif red_dash.turns == 0 and blue_dash.turns > 0:
            blue_dash_state = blue_dash_map.get(
                (blue_dash.end_loc, red_dash.end_loc, blue_dash.prop_rot_dir), ""
            )
            return f"({self._normalize_turns(blue_dash)}, {self._normalize_turns(red_dash)}, {blue_dash_state})"
        elif red_dash.turns > 0 and blue_dash.turns > 0:
            red_dash_state = red_dash_map.get(
                (blue_dash.end_loc, red_dash.end_loc, red_dash.prop_rot_dir), ""
            )
            blue_dash_state = blue_dash_map.get(
                (blue_dash.end_loc, red_dash.end_loc, blue_dash.prop_rot_dir), ""
            )
            vtg_dir = "s" if red_dash.prop_rot_dir == blue_dash.prop_rot_dir else "o"
            return f"({vtg_dir}, {self._normalize_turns(blue_dash)}, {self._normalize_turns(red_dash)}, {blue_dash_state}, {red_dash_state})"
        else:
            return f"({self._normalize_turns(blue_dash)}, {self._normalize_turns(red_dash)})"

    def _get_direction_maps(self):

        blue_dash_direction_map = {
            (EAST, NORTH, CLOCKWISE): OPENING,
            (EAST, NORTH, COUNTER_CLOCKWISE): CLOSING,
            (EAST, SOUTH, CLOCKWISE): CLOSING,
            (EAST, SOUTH, COUNTER_CLOCKWISE): OPENING,
            (WEST, NORTH, CLOCKWISE): CLOSING,
            (WEST, NORTH, COUNTER_CLOCKWISE): OPENING,
            (WEST, SOUTH, CLOCKWISE): OPENING,
            (WEST, SOUTH, COUNTER_CLOCKWISE): CLOSING,
            (NORTH, EAST, CLOCKWISE): CLOSING,
            (NORTH, EAST, COUNTER_CLOCKWISE): OPENING,
            (NORTH, WEST, CLOCKWISE): OPENING,
            (NORTH, WEST, COUNTER_CLOCKWISE): CLOSING,
            (SOUTH, EAST, CLOCKWISE): OPENING,
            (SOUTH, EAST, COUNTER_CLOCKWISE): CLOSING,
            (SOUTH, WEST, CLOCKWISE): CLOSING,
            (SOUTH, WEST, COUNTER_CLOCKWISE): OPENING,
        }
        red_dash_direction_map = {
            (EAST, NORTH, CLOCKWISE): CLOSING,
            (EAST, NORTH, COUNTER_CLOCKWISE): OPENING,
            (EAST, SOUTH, CLOCKWISE): OPENING,
            (EAST, SOUTH, COUNTER_CLOCKWISE): CLOSING,
            (WEST, NORTH, CLOCKWISE): OPENING,
            (WEST, NORTH, COUNTER_CLOCKWISE): CLOSING,
            (WEST, SOUTH, CLOCKWISE): CLOSING,
            (WEST, SOUTH, COUNTER_CLOCKWISE): OPENING,
            (NORTH, EAST, CLOCKWISE): OPENING,
            (NORTH, EAST, COUNTER_CLOCKWISE): CLOSING,
            (NORTH, WEST, CLOCKWISE): CLOSING,
            (NORTH, WEST, COUNTER_CLOCKWISE): OPENING,
            (SOUTH, EAST, CLOCKWISE): CLOSING,
            (SOUTH, EAST, COUNTER_CLOCKWISE): OPENING,
            (SOUTH, WEST, CLOCKWISE): OPENING,
            (SOUTH, WEST, COUNTER_CLOCKWISE): CLOSING,
        }
        return blue_dash_direction_map, red_dash_direction_map


class GammaTurnsTupleGenerator(BaseTurnsTupleGenerator):
    def generate_turns_tuple(self, pictograph) -> str:
        super().set_pictograph(pictograph)
        blue_static = self.p.blue_motion
        red_static = self.p.red_motion
        blue_static_map, red_static_map = self._get_direction_maps()

        if blue_static.turns == 0 and red_static.turns > 0:
            red_static_state = red_static_map.get(
                (blue_static.end_loc, red_static.end_loc, red_static.prop_rot_dir), ""
            )
            return f"({self._normalize_turns(blue_static)}, {self._normalize_turns(red_static)}, {red_static_state})"
        elif red_static.turns == 0 and blue_static.turns > 0:
            blue_static_state = blue_static_map.get(
                (blue_static.end_loc, red_static.end_loc, blue_static.prop_rot_dir), ""
            )
            return f"({self._normalize_turns(blue_static)}, {self._normalize_turns(red_static)}, {blue_static_state})"
        elif red_static.turns > 0 and blue_static.turns > 0:
            red_static_state = red_static_map.get(
                (blue_static.end_loc, red_static.end_loc, red_static.prop_rot_dir), ""
            )
            blue_static_state = blue_static_map.get(
                (blue_static.end_loc, red_static.end_loc, blue_static.prop_rot_dir), ""
            )
            vtg_dir = (
                "s" if red_static.prop_rot_dir == blue_static.prop_rot_dir else "o"
            )
            return f"({vtg_dir}, {self._normalize_turns(blue_static)}, {self._normalize_turns(red_static)}, {blue_static_state}, {red_static_state})"
        else:
            return f"({self._normalize_turns(blue_static)}, {self._normalize_turns(red_static)})"

    def _get_direction_maps(self):
        blue_static_direction_map = {
            (EAST, NORTH, CLOCKWISE): OPENING,
            (EAST, NORTH, COUNTER_CLOCKWISE): CLOSING,
            (EAST, SOUTH, CLOCKWISE): CLOSING,
            (EAST, SOUTH, COUNTER_CLOCKWISE): OPENING,
            (WEST, NORTH, CLOCKWISE): CLOSING,
            (WEST, NORTH, COUNTER_CLOCKWISE): OPENING,
            (WEST, SOUTH, CLOCKWISE): OPENING,
            (WEST, SOUTH, COUNTER_CLOCKWISE): CLOSING,
            (NORTH, EAST, CLOCKWISE): CLOSING,
            (NORTH, EAST, COUNTER_CLOCKWISE): OPENING,
            (NORTH, WEST, CLOCKWISE): OPENING,
            (NORTH, WEST, COUNTER_CLOCKWISE): CLOSING,
            (SOUTH, EAST, CLOCKWISE): OPENING,
            (SOUTH, EAST, COUNTER_CLOCKWISE): CLOSING,
            (SOUTH, WEST, CLOCKWISE): CLOSING,
            (SOUTH, WEST, COUNTER_CLOCKWISE): OPENING,
        }
        red_static_direction_map = {
            (EAST, NORTH, CLOCKWISE): CLOSING,
            (EAST, NORTH, COUNTER_CLOCKWISE): OPENING,
            (EAST, SOUTH, CLOCKWISE): OPENING,
            (EAST, SOUTH, COUNTER_CLOCKWISE): CLOSING,
            (WEST, NORTH, CLOCKWISE): OPENING,
            (WEST, NORTH, COUNTER_CLOCKWISE): CLOSING,
            (WEST, SOUTH, CLOCKWISE): CLOSING,
            (WEST, SOUTH, COUNTER_CLOCKWISE): OPENING,
            (NORTH, EAST, CLOCKWISE): OPENING,
            (NORTH, EAST, COUNTER_CLOCKWISE): CLOSING,
            (NORTH, WEST, CLOCKWISE): CLOSING,
            (NORTH, WEST, COUNTER_CLOCKWISE): OPENING,
            (SOUTH, EAST, CLOCKWISE): CLOSING,
            (SOUTH, EAST, COUNTER_CLOCKWISE): OPENING,
            (SOUTH, WEST, CLOCKWISE): OPENING,
            (SOUTH, WEST, COUNTER_CLOCKWISE): CLOSING,
        }
        return blue_static_direction_map, red_static_direction_map
