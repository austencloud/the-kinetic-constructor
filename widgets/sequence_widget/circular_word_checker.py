class CircularWordChecker:
    def __init__(self, sequence):
        self.sequence = sequence
        self.is_circular = False
        self.is_permutable = False

    def check_properties(self):
        if not self.sequence:
            return False, False

        start_position: str = self.sequence[0]["end_pos"]  # Use the exact start position from the first dict
        current_position = start_position
        letter_sequence = []
        rotational_permutations = True

        for entry in self.sequence:
            if "letter" in entry:
                letter_sequence.append(entry["letter"])
            if "end_pos" in entry:
                current_position = entry["end_pos"]

        # Check for exact match (Circular)
        self.is_circular = (current_position == start_position)

        # Check if the last position matches a variation of the start position (Permutable)
        base_position = start_position.rstrip('0123456789')  # Strip numeric suffix
        current_base_position = current_position.rstrip('0123456789')
        self.is_permutable = (current_base_position == base_position)

        # Check for rotational permutations
        unique_letters = set(letter_sequence)
        for letter in unique_letters:
            occurrences = [i for i, x in enumerate(letter_sequence) if x == letter]
            if len(occurrences) > 1:
                first_occurrence = occurrences[0]
                for i in range(1, len(occurrences)):
                    prev = self.sequence[occurrences[i - 1]]
                    curr = self.sequence[occurrences[i]]
                    if not self._is_rotational_permutation(prev, curr):
                        rotational_permutations = False
                        break

        self.is_permutable = self.is_permutable and rotational_permutations

        return self.is_circular, self.is_permutable

    def _is_rotational_permutation(self, prev, curr):
        # Check if the properties are consistent and only position is changing
        return (
            prev["blue_attributes"]["motion_type"] == curr["blue_attributes"]["motion_type"] and
            prev["blue_attributes"]["prop_rot_dir"] == curr["blue_attributes"]["prop_rot_dir"] and
            prev["red_attributes"]["motion_type"] == curr["red_attributes"]["motion_type"] and
            prev["red_attributes"]["prop_rot_dir"] == curr["red_attributes"]["prop_rot_dir"]
        )

    def get_properties(self):
        return {"is_circular": self.is_circular, "is_permutable": self.is_permutable}
