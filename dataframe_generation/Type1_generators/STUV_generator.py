from typing import Dict, List, Literal, Tuple
from data.Enums import Location, PropRotationDirection
from df_generator import DataFrameGenerator
from data.positions_map import positions_map
from data.constants import *


class STUV_Generator(DataFrameGenerator):
    def __init__(self) -> None:
        super().__init__(letters=["S", "T", "U", "V"])
        self.create_dataframes_for_STUV()

    def create_dataframes_for_STUV(self) -> None:
        for letter in self.letters:
            data = self.create_df(letter)
            self.save_dataframe(letter, data, "Type_1")

    def create_ST_dataframes(
        self,
        letter,
        red_start_loc,
        red_end_loc,
        red_motion_type,
        red_rot_dir,
        red_leading_bool,
    ):
        variations = []
        blue_motion_type = red_motion_type

        if red_leading_bool:
            blue_start_loc, blue_end_loc = self.determine_start_end_loc(
                red_start_loc, red_end_loc, red_rot_dir, red_leading_bool
            )
        elif not red_leading_bool:
            blue_start_loc, blue_end_loc = self.determine_start_end_loc(
                red_start_loc, red_end_loc, red_rot_dir, red_leading_bool
            )

        # Apply positions
        start_pos, end_pos = self.get_positions(
            blue_start_loc, blue_end_loc, red_start_loc, red_end_loc
        )

        variation = {
            "letter": letter,
            "start_position": start_pos,
            "end_position": end_pos,
            "blue_motion_type": blue_motion_type,
            "blue_rot_dir": red_rot_dir,
            "blue_start_location": blue_start_loc,
            "blue_end_location": blue_end_loc,
            "red_motion_type": red_motion_type,
            "red_rot_dir": red_rot_dir,
            "red_start_location": red_start_loc,
            "red_end_location": red_end_loc,
        }

        variations.append(variation)
        return variations

    def create_U_dataframes(self) -> List[Dict]:
        data = []
        red_pro_handpath_rot_dir = self.get_handpath_tuple_map_collection(PRO)

        for red_handpath_rot_dir in self.handpath_rot_dirs:
            # Blue leading with CCW_HANDPATH
            for red_start_loc, red_end_loc in red_pro_handpath_rot_dir[
                red_handpath_rot_dir
            ]:
                if red_handpath_rot_dir == CCW_HANDPATH:
                    blue_motion_type = PRO
                    red_motion_type = ANTI
                    red_prop_rot_dir = self.get_prop_rot_dir(
                        red_motion_type, red_handpath_rot_dir
                    )
                    blue_prop_rot_dir = self.get_prop_rot_dir(
                        blue_motion_type, red_handpath_rot_dir
                    )
                    blue_start_loc = red_end_loc
                    blue_end_loc = self.get_opposite_location(red_start_loc)
                    data.append(
                        self.create_variation_dict(
                            "U",
                            red_start_loc,
                            red_end_loc,
                            blue_start_loc,
                            blue_end_loc,
                            red_motion_type,
                            red_prop_rot_dir,
                            blue_motion_type,
                            blue_prop_rot_dir,
                        )
                    )
            # Blue leading with CW_HANDPATH
            for red_start_loc, red_end_loc in red_pro_handpath_rot_dir[
                red_handpath_rot_dir
            ]:
                if red_handpath_rot_dir == CW_HANDPATH:
                    blue_motion_type = PRO
                    red_motion_type = ANTI
                    red_prop_rot_dir = self.get_prop_rot_dir(
                        red_motion_type, red_handpath_rot_dir
                    )
                    blue_prop_rot_dir = self.get_prop_rot_dir(
                        blue_motion_type, red_handpath_rot_dir
                    )
                    blue_start_loc = red_end_loc
                    blue_end_loc = self.get_opposite_location(red_start_loc)
                    data.append(
                        self.create_variation_dict(
                            "U",
                            red_start_loc,
                            red_end_loc,
                            blue_start_loc,
                            blue_end_loc,
                            red_motion_type,
                            red_prop_rot_dir,
                            blue_motion_type,
                            blue_prop_rot_dir,
                        )
                    )
            # Red leading with CCW_HANDPATH
            for red_start_loc, red_end_loc in red_pro_handpath_rot_dir[
                red_handpath_rot_dir
            ]:
                if red_handpath_rot_dir == CCW_HANDPATH:
                    blue_motion_type = ANTI
                    red_motion_type = PRO
                    red_prop_rot_dir = self.get_prop_rot_dir(
                        red_motion_type, red_handpath_rot_dir
                    )
                    blue_prop_rot_dir = self.get_prop_rot_dir(
                        blue_motion_type, red_handpath_rot_dir
                    )
                    blue_start_loc = self.get_opposite_location(red_end_loc)
                    blue_end_loc = red_start_loc
                    data.append(
                        self.create_variation_dict(
                            "U",
                            red_start_loc,
                            red_end_loc,
                            blue_start_loc,
                            blue_end_loc,
                            red_motion_type,
                            red_prop_rot_dir,
                            blue_motion_type,
                            blue_prop_rot_dir,
                        )
                    )
            # Red leading with CW_HANDPATH
            for red_start_loc, red_end_loc in red_pro_handpath_rot_dir[
                red_handpath_rot_dir
            ]:
                if red_handpath_rot_dir == CW_HANDPATH:
                    blue_motion_type = ANTI
                    red_motion_type = PRO
                    red_prop_rot_dir = self.get_prop_rot_dir(
                        red_motion_type, red_handpath_rot_dir
                    )
                    blue_prop_rot_dir = self.get_prop_rot_dir(
                        blue_motion_type, red_handpath_rot_dir
                    )
                    blue_start_loc = self.get_opposite_location(red_end_loc)
                    blue_end_loc = red_start_loc
                    data.append(
                        self.create_variation_dict(
                            "U",
                            red_start_loc,
                            red_end_loc,
                            blue_start_loc,
                            blue_end_loc,
                            red_motion_type,
                            red_prop_rot_dir,
                            blue_motion_type,
                            blue_prop_rot_dir,
                        )
                    )

        return data

    def create_V_dataframes(self) -> List[Dict]:
        data = []
        red_pro_handpath_rot_dir = self.get_handpath_tuple_map_collection(PRO)

        for red_handpath_rot_dir in self.handpath_rot_dirs:
            # Blue leading with CCW_HANDPATH
            for red_start_loc, red_end_loc in red_pro_handpath_rot_dir[
                red_handpath_rot_dir
            ]:
                if red_handpath_rot_dir == CCW_HANDPATH:
                    blue_motion_type = ANTI
                    red_motion_type = PRO
                    red_prop_rot_dir = self.get_prop_rot_dir(
                        red_motion_type, red_handpath_rot_dir
                    )
                    blue_prop_rot_dir = self.get_prop_rot_dir(
                        blue_motion_type, red_handpath_rot_dir
                    )
                    blue_start_loc = red_end_loc
                    blue_end_loc = self.get_opposite_location(red_start_loc)
                    data.append(
                        self.create_variation_dict(
                            "V",
                            red_start_loc,
                            red_end_loc,
                            blue_start_loc,
                            blue_end_loc,
                            red_motion_type,
                            red_prop_rot_dir,
                            blue_motion_type,
                            blue_prop_rot_dir,
                        )
                    )

            # Blue leading with CW_HANDPATH
            for red_start_loc, red_end_loc in red_pro_handpath_rot_dir[
                red_handpath_rot_dir
            ]:
                if red_handpath_rot_dir == CW_HANDPATH:
                    blue_motion_type = ANTI
                    red_motion_type = PRO
                    red_prop_rot_dir = self.get_prop_rot_dir(
                        red_motion_type, red_handpath_rot_dir
                    )
                    blue_prop_rot_dir = self.get_prop_rot_dir(
                        blue_motion_type, red_handpath_rot_dir
                    )
                    blue_start_loc = red_end_loc
                    blue_end_loc = self.get_opposite_location(red_start_loc)
                    data.append(
                        self.create_variation_dict(
                            "V",
                            red_start_loc,
                            red_end_loc,
                            blue_start_loc,
                            blue_end_loc,
                            red_motion_type,
                            red_prop_rot_dir,
                            blue_motion_type,
                            blue_prop_rot_dir,
                        )
                    )
            # Red leading with CCW_HANDPATH
            for red_start_loc, red_end_loc in red_pro_handpath_rot_dir[
                red_handpath_rot_dir
            ]:
                if red_handpath_rot_dir == CCW_HANDPATH:
                    blue_motion_type = PRO
                    red_motion_type = ANTI
                    red_prop_rot_dir = self.get_prop_rot_dir(
                        red_motion_type, red_handpath_rot_dir
                    )
                    blue_prop_rot_dir = self.get_prop_rot_dir(
                        blue_motion_type, red_handpath_rot_dir
                    )
                    blue_start_loc = self.get_opposite_location(red_end_loc)
                    blue_end_loc = red_start_loc
                    data.append(
                        self.create_variation_dict(
                            "V",
                            red_start_loc,
                            red_end_loc,
                            blue_start_loc,
                            blue_end_loc,
                            red_motion_type,
                            red_prop_rot_dir,
                            blue_motion_type,
                            blue_prop_rot_dir,
                        )
                    )

            # Red leading with CW_HANDPATH
            for red_start_loc, red_end_loc in red_pro_handpath_rot_dir[
                red_handpath_rot_dir
            ]:
                if red_handpath_rot_dir == CW_HANDPATH:
                    blue_motion_type = PRO
                    red_motion_type = ANTI
                    red_prop_rot_dir = self.get_prop_rot_dir(
                        red_motion_type, red_handpath_rot_dir
                    )
                    blue_prop_rot_dir = self.get_prop_rot_dir(
                        blue_motion_type, red_handpath_rot_dir
                    )
                    blue_start_loc = self.get_opposite_location(red_end_loc)
                    blue_end_loc = red_start_loc
                    data.append(
                        self.create_variation_dict(
                            "V",
                            red_start_loc,
                            red_end_loc,
                            blue_start_loc,
                            blue_end_loc,
                            red_motion_type,
                            red_prop_rot_dir,
                            blue_motion_type,
                            blue_prop_rot_dir,
                        )
                    )

        return data

    def create_variation_dict(
        self,
        letter,
        red_start_loc,
        red_end_loc,
        blue_start_loc,
        blue_end_loc,
        red_motion_type,
        red_rot_dir,
        blue_motion_type,
        blue_rot_dir,
    ):
        start_pos, end_pos = self.get_positions(
            red_start_loc, red_end_loc, blue_start_loc, blue_end_loc
        )
        return {
            "letter": letter,
            "start_position": start_pos,
            "end_position": end_pos,
            "blue_motion_type": blue_motion_type,
            "blue_rot_dir": blue_rot_dir,
            "blue_start_location": blue_start_loc,
            "blue_end_location": blue_end_loc,
            "red_motion_type": red_motion_type,
            "red_rot_dir": red_rot_dir,
            "red_start_location": red_start_loc,
            "red_end_location": red_end_loc,
        }

    def get_positions(
        self, red_start_loc, red_end_loc, blue_start_loc, blue_end_loc
    ) -> Tuple[Location, Location]:
        start_key = (blue_start_loc, red_start_loc)
        end_key = (blue_end_loc, red_end_loc)
        start_pos = positions_map.get(start_key)
        end_pos = positions_map.get(end_key)
        return start_pos, end_pos

    def determine_start_end_loc(
        self, red_start_loc, red_end_loc, red_rot_dir, red_leading
    ):
        if red_rot_dir == CLOCKWISE:
            if red_leading:
                if red_start_loc == NORTH:
                    blue_start_loc = WEST
                elif red_start_loc == EAST:
                    blue_start_loc = NORTH
                elif red_start_loc == SOUTH:
                    blue_start_loc = EAST
                elif red_start_loc == WEST:
                    blue_start_loc = SOUTH
                blue_end_loc = red_start_loc

            elif not red_leading:
                if red_start_loc == NORTH:
                    blue_end_loc = SOUTH
                elif red_start_loc == EAST:
                    blue_end_loc = WEST
                elif red_start_loc == SOUTH:
                    blue_end_loc = NORTH
                elif red_start_loc == WEST:
                    blue_end_loc = EAST
                blue_start_loc = red_end_loc

        elif red_rot_dir == COUNTER_CLOCKWISE:
            if red_leading:
                if red_start_loc == NORTH:
                    blue_start_loc = EAST
                elif red_start_loc == WEST:
                    blue_start_loc = NORTH
                elif red_start_loc == SOUTH:
                    blue_start_loc = WEST
                elif red_start_loc == EAST:
                    blue_start_loc = SOUTH
                blue_end_loc = red_start_loc

            elif not red_leading:
                if red_start_loc == NORTH:
                    blue_end_loc = SOUTH
                elif red_start_loc == WEST:
                    blue_end_loc = EAST
                elif red_start_loc == SOUTH:
                    blue_end_loc = NORTH
                elif red_start_loc == EAST:
                    blue_end_loc = WEST
                blue_start_loc = red_end_loc

        return blue_start_loc, blue_end_loc

    def generate_variations_U(
        self,
        letter,
        red_start_loc,
        red_end_loc,
        red_rot_dir,
        red_leading,
    ):
        variations = []
        if red_leading:
            red_motion_type = PRO
            blue_motion_type = ANTI
            leading_rot_dir = red_rot_dir
        elif not red_leading:
            red_motion_type = ANTI
            blue_motion_type = PRO

        blue_rot_dir = COUNTER_CLOCKWISE if red_rot_dir == CLOCKWISE else CLOCKWISE

        if red_rot_dir == CLOCKWISE:
            if red_leading:
                if red_start_loc == NORTH:
                    blue_start_loc = WEST
                elif red_start_loc == EAST:
                    blue_start_loc = NORTH
                elif red_start_loc == SOUTH:
                    blue_start_loc = EAST
                elif red_start_loc == WEST:
                    blue_start_loc = SOUTH
                blue_end_loc = red_start_loc

            elif not red_leading:
                if red_start_loc == NORTH:
                    blue_end_loc = SOUTH
                elif red_start_loc == EAST:
                    blue_end_loc = WEST
                elif red_start_loc == SOUTH:
                    blue_end_loc = NORTH
                elif red_start_loc == WEST:
                    blue_end_loc = EAST
                blue_start_loc = red_end_loc

        elif red_rot_dir == COUNTER_CLOCKWISE:
            if red_leading:
                if red_start_loc == NORTH:
                    blue_start_loc = EAST
                elif red_start_loc == WEST:
                    blue_start_loc = NORTH
                elif red_start_loc == SOUTH:
                    blue_start_loc = WEST
                elif red_start_loc == EAST:
                    blue_start_loc = SOUTH
                blue_end_loc = red_start_loc

            elif not red_leading:
                if red_start_loc == NORTH:
                    blue_end_loc = SOUTH
                elif red_start_loc == WEST:
                    blue_end_loc = EAST
                elif red_start_loc == SOUTH:
                    blue_end_loc = NORTH
                elif red_start_loc == EAST:
                    blue_end_loc = WEST
                blue_start_loc = red_end_loc

        # Apply positions
        start_pos, end_pos = self.get_positions(
            blue_start_loc, blue_end_loc, red_start_loc, red_end_loc
        )
        # Create variations for red and blue leading
        variations.append(
            letter,
            start_pos,
            end_pos,
            blue_motion_type,
            blue_rot_dir,
            blue_start_loc,
            blue_end_loc,
            red_motion_type,
            red_rot_dir,
            red_start_loc,
            red_end_loc,
        )

        return variations

    def get_positions(
        self, blue_start_loc, blue_end_loc, red_start_loc, red_end_loc
    ) -> Tuple[Location, Location]:
        start_key = (blue_start_loc, red_start_loc)
        end_key = (blue_end_loc, red_end_loc)
        start_pos = positions_map.get(start_key)
        end_pos = positions_map.get(end_key)
        return start_pos, end_pos

    def create_df(self, letter) -> List[Dict]:
        data = []
        if letter in ["S", "T"]:
            red_motion_type = PRO if letter == "S" else ANTI
            for red_handpath_rot_dir in self.handpath_rot_dirs:
                red_prop_rot_dir = self.get_prop_rot_dir(
                    red_motion_type, red_handpath_rot_dir
                )

                for red_start_loc, red_end_loc in self.red_handpath_map:
                    data.extend(
                        self.create_ST_dataframes(
                            letter,
                            red_start_loc,
                            red_end_loc,
                            red_motion_type,
                            red_prop_rot_dir,
                            red_leading_bool=True,
                        )
                    )
                    data.extend(
                        self.create_ST_dataframes(
                            letter,
                            red_start_loc,
                            red_end_loc,
                            red_motion_type,
                            red_prop_rot_dir,
                            red_leading_bool=False,
                        )
                    )
        elif letter == "U":
            data = self.create_U_dataframes()
            self.save_dataframe(letter, data, "Type_1")
        elif letter == "V":
            data = self.create_V_dataframes()
            self.save_dataframe(letter, data, "Type_1")
        return data

    def determine_follower_start_location(
        self, leader_end_loc, follower_rot_dir
    ) -> Location:
        if follower_rot_dir == CLOCKWISE:
            if leader_end_loc == NORTH:
                return EAST
            elif leader_end_loc == WEST:
                return NORTH
            elif leader_end_loc == SOUTH:
                return WEST
            elif leader_end_loc == EAST:
                return SOUTH
        elif follower_rot_dir == COUNTER_CLOCKWISE:
            if leader_end_loc == NORTH:
                return WEST
            elif leader_end_loc == EAST:
                return NORTH
            elif leader_end_loc == SOUTH:
                return EAST
            elif leader_end_loc == WEST:
                return SOUTH


STUV_Generator()
