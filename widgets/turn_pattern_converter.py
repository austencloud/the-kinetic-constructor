class TurnPatternConverter:
    @staticmethod
    def sequence_to_pattern(sequence: list[dict]) -> str:
        # Convert sequence data to a turn pattern string
        pattern_parts = []
        for item in sequence:
            # if it's the first item, ignore it
            if item == sequence[0]:
                continue
            blue_turns = item.get("blue_turns", 0)
            red_turns = item.get("red_turns", 0)
            pattern_parts.append(f"{blue_turns},{red_turns}")
        return "_".join(pattern_parts)

    @staticmethod
    def pattern_to_sequence(pattern: str) -> list[dict]:
        # Convert a pattern string to an abstract representation (list of tuples)
        parts = pattern.split("_")
        sequence = [tuple(map(int, part.split(","))) for part in parts]
        return sequence
