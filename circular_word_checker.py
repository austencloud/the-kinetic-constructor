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

        return self.is_circular, self.is_permutable

    def get_properties(self):
        return {"is_circular": self.is_circular, "is_permutable": self.is_permutable}
