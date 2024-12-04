from data.constants import *


class SequenceColorSwapper:

    def swap_colors(self, sequence_json: list[dict]) -> list[dict]:
        self.positions_map: dict[tuple[str], str] = {
            (SOUTH, NORTH): ALPHA1,
            (SOUTHWEST, NORTHEAST): ALPHA2,
            (WEST, EAST): ALPHA3,
            (NORTHWEST, SOUTHEAST): ALPHA4,
            (NORTH, SOUTH): ALPHA5,
            (NORTHEAST, SOUTHWEST): ALPHA6,
            (EAST, WEST): ALPHA7,
            (SOUTHEAST, NORTHWEST): ALPHA8,
            (NORTH, NORTH): BETA1,
            (NORTHEAST, NORTHEAST): BETA2,
            (EAST, EAST): BETA3,
            (SOUTHEAST, SOUTHEAST): BETA4,
            (SOUTH, SOUTH): BETA5,
            (SOUTHWEST, SOUTHWEST): BETA6,
            (WEST, WEST): BETA7,
            (NORTHWEST, NORTHWEST): BETA8,
            (WEST, NORTH): GAMMA1,
            (NORTHWEST, NORTHEAST): GAMMA2,
            (NORTH, EAST): GAMMA3,
            (NORTHEAST, SOUTHEAST): GAMMA4,
            (EAST, SOUTH): GAMMA5,
            (SOUTHEAST, SOUTHWEST): GAMMA6,
            (SOUTH, WEST): GAMMA7,
            (SOUTHWEST, NORTHWEST): GAMMA8,
            (EAST, NORTH): GAMMA9,
            (SOUTHEAST, NORTHEAST): GAMMA10,
            (SOUTH, EAST): GAMMA11,
            (SOUTHWEST, SOUTHEAST): GAMMA12,
            (WEST, SOUTH): GAMMA13,
            (NORTHWEST, SOUTHWEST): GAMMA14,
            (NORTH, WEST): GAMMA15,
            (NORTHEAST, NORTHWEST): GAMMA16,
        }

        swapped_sequence = []

        # Copy the metadata (first dictionary)
        metadata = sequence_json[0].copy()
        swapped_sequence.append(metadata)

        # Swap colors in the start position beat (second dictionary)
        if len(sequence_json) > 1:
            start_pos_beat = sequence_json[1].copy()
            # Swap blue and red attributes
            start_pos_beat["blue_attributes"], start_pos_beat["red_attributes"] = (
                start_pos_beat["red_attributes"],
                start_pos_beat["blue_attributes"],
            )
            # Recalculate 'end_pos' based on swapped attributes
            left_loc = start_pos_beat["blue_attributes"]["end_loc"]
            right_loc = start_pos_beat["red_attributes"]["end_loc"]
            start_pos_beat["end_pos"] = self.get_position_name(left_loc, right_loc)
            swapped_sequence.append(start_pos_beat)
        else:
            return sequence_json  # Return the original sequence if no start position

        # Swap colors in each beat
        for beat in sequence_json[2:]:
            swapped_beat = beat.copy()
            # Swap blue and red attributes
            swapped_beat["blue_attributes"], swapped_beat["red_attributes"] = (
                swapped_beat["red_attributes"],
                swapped_beat["blue_attributes"],
            )
            # Recalculate 'start_pos' and 'end_pos' based on swapped attributes
            # Recalculate 'start_pos'
            left_start_loc = swapped_beat["blue_attributes"]["start_loc"]
            right_start_loc = swapped_beat["red_attributes"]["start_loc"]
            swapped_beat["start_pos"] = self.get_position_name(
                left_start_loc, right_start_loc
            )
            # Recalculate 'end_pos'
            left_end_loc = swapped_beat["blue_attributes"]["end_loc"]
            right_end_loc = swapped_beat["red_attributes"]["end_loc"]
            swapped_beat["end_pos"] = self.get_position_name(
                left_end_loc, right_end_loc
            )
            swapped_sequence.append(swapped_beat)

        return swapped_sequence

    def get_position_name(self, left_loc: str, right_loc: str) -> str:
        # Use the positions_map to get the position name
        position_name = self.positions_map.get((left_loc, right_loc), "unknown")
        return position_name
