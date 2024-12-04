class SequenceMirror:
    def __init__(self):
        self.vertical_mirror_positions = {
            "alpha1": "alpha1",
            "alpha3": "alpha7",
            "alpha5": "alpha5",
            "alpha7": "alpha3",
            "beta1": "beta1",
            "beta3": "beta7",
            "beta5": "beta5",
            "beta7": "beta3",
            "gamma1": "gamma9",
            "gamma3": "gamma15",
            "gamma5": "gamma13",
            "gamma7": "gamma11",
            "gamma9": "gamma1",
            "gamma11": "gamma7",
            "gamma13": "gamma5",
            "gamma15": "gamma3",
        }

        self.vertical_mirror_locations = {"s": "s", "e": "w", "w": "e", "n": "n"}

    def reverse_prop_rot_dir(self, prop_rot_dir):
        if prop_rot_dir == "cw":
            return "ccw"
        elif prop_rot_dir == "ccw":
            return "cw"
        else:
            return prop_rot_dir

    def mirror_sequence(self, sequence_json):
        # Implement the mirroring logic here
        mirrored_sequence = []

        # Copy the metadata (first dictionary)
        metadata = sequence_json[0].copy()
        mirrored_sequence.append(metadata)

        # Copy the start position beat (second dictionary)
        start_pos_beat = sequence_json[1].copy()
        # Mirror the start positions
        start_pos_beat["end_pos"] = self.vertical_mirror_positions.get(
            start_pos_beat["end_pos"], start_pos_beat["end_pos"]
        )
        start_pos_beat["blue_attributes"]["end_loc"] = (
            self.vertical_mirror_locations.get(
                start_pos_beat["blue_attributes"]["end_loc"],
                start_pos_beat["blue_attributes"]["end_loc"],
            )
        )
        start_pos_beat["red_attributes"]["end_loc"] = (
            self.vertical_mirror_locations.get(
                start_pos_beat["red_attributes"]["end_loc"],
                start_pos_beat["red_attributes"]["end_loc"],
            )
        )
        # Reverse prop_rot_dir for start position beat
        start_pos_beat["blue_attributes"]["prop_rot_dir"] = self.reverse_prop_rot_dir(
            start_pos_beat["blue_attributes"]["prop_rot_dir"]
        )
        start_pos_beat["red_attributes"]["prop_rot_dir"] = self.reverse_prop_rot_dir(
            start_pos_beat["red_attributes"]["prop_rot_dir"]
        )
        mirrored_sequence.append(start_pos_beat)

        # Mirror each beat in the sequence
        for beat in sequence_json[2:]:
            mirrored_beat = beat.copy()
            # Mirror end positions
            mirrored_beat["start_pos"] = self.vertical_mirror_positions.get(
                mirrored_beat["start_pos"], mirrored_beat["start_pos"]
            )
            mirrored_beat["end_pos"] = self.vertical_mirror_positions.get(
                mirrored_beat["end_pos"], mirrored_beat["end_pos"]
            )
            # Mirror locations
            mirrored_beat["blue_attributes"]["start_loc"] = (
                self.vertical_mirror_locations.get(
                    mirrored_beat["blue_attributes"]["start_loc"],
                    mirrored_beat["blue_attributes"]["start_loc"],
                )
            )
            mirrored_beat["blue_attributes"]["end_loc"] = (
                self.vertical_mirror_locations.get(
                    mirrored_beat["blue_attributes"]["end_loc"],
                    mirrored_beat["blue_attributes"]["end_loc"],
                )
            )
            mirrored_beat["red_attributes"]["start_loc"] = (
                self.vertical_mirror_locations.get(
                    mirrored_beat["red_attributes"]["start_loc"],
                    mirrored_beat["red_attributes"]["start_loc"],
                )
            )
            mirrored_beat["red_attributes"]["end_loc"] = (
                self.vertical_mirror_locations.get(
                    mirrored_beat["red_attributes"]["end_loc"],
                    mirrored_beat["red_attributes"]["end_loc"],
                )
            )
            # Reverse prop_rot_dir for blue_attributes
            mirrored_beat["blue_attributes"]["prop_rot_dir"] = (
                self.reverse_prop_rot_dir(
                    mirrored_beat["blue_attributes"]["prop_rot_dir"]
                )
            )
            # Reverse prop_rot_dir for red_attributes
            mirrored_beat["red_attributes"]["prop_rot_dir"] = self.reverse_prop_rot_dir(
                mirrored_beat["red_attributes"]["prop_rot_dir"]
            )
            # Add the mirrored beat to the sequence
            mirrored_sequence.append(mirrored_beat)

        return mirrored_sequence
