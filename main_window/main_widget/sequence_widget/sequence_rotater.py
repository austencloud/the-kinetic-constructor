from data.positions_map import positions_map

class SequenceRotator:
    def __init__(self):
        self.rotation_mapping_90 = {
            "n": "e",
            "ne": "se",
            "e": "s",
            "se": "sw",
            "s": "w",
            "sw": "nw",
            "w": "n",
            "nw": "ne"
        }

    def rotate_sequence(self, sequence_json):
        rotated_sequence = []

        metadata = sequence_json[0].copy()
        rotated_sequence.append(metadata)

        start_pos_beat = sequence_json[1].copy()
        self._rotate_beat(start_pos_beat)
        rotated_sequence.append(start_pos_beat)

        for beat in sequence_json[2:]:
            rotated_beat = beat.copy()
            self._rotate_beat(rotated_beat)
            rotated_sequence.append(rotated_beat)

        return rotated_sequence

    def _rotate_beat(self, beat):
        for color in ["blue_attributes", "red_attributes"]:
            if color in beat:
                attributes = beat[color]
                if "start_loc" in attributes:
                    attributes["start_loc"] = self._rotate_location(
                        attributes["start_loc"], 1)
                if "end_loc" in attributes:
                    attributes["end_loc"] = self._rotate_location(
                        attributes["end_loc"], 1)

        if "blue_attributes" in beat and "red_attributes" in beat:
            blue_attrs = beat["blue_attributes"]
            red_attrs = beat["red_attributes"]

            if "start_loc" in blue_attrs and "start_loc" in red_attrs:
                beat["start_pos"] = self.get_position_name(
                    blue_attrs["start_loc"], red_attrs["start_loc"]
                )

            if "end_loc" in blue_attrs and "end_loc" in red_attrs:
                beat["end_pos"] = self.get_position_name(
                    blue_attrs["end_loc"], red_attrs["end_loc"]
                )

    def _rotate_location(self, location, rotation_steps):
        if location not in self.rotation_mapping_90:
            return "Unknown location:" + location 
        for _ in range(rotation_steps % 4):
            location = self.rotation_mapping_90[location]
        return location

    def get_position_name(self, left_loc, right_loc):
        return positions_map.get((left_loc, right_loc), "unknown")
