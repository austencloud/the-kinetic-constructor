class TurnPatternConverter:
    @staticmethod
    def sequence_to_pattern(sequence: list[dict]) -> str:
        """
        Convert sequence data to a more readable turn pattern string, including tuples for differing turns.
        """
        pattern_parts = []
        for item in sequence:
            if (
                "blue_turns" in item or "red_turns" in item
            ):  # Ensure there are turn values
                blue_turns = item.get("blue_turns", 0)
                red_turns = item.get("red_turns", 0)

                # Determine how to format each part based on the presence and value of turns
                if blue_turns and red_turns:
                    # If both turns are present and not equal, format as a tuple
                    pattern_part = (
                        f"L{blue_turns},R{red_turns}"
                        if blue_turns != red_turns
                        else f"L{blue_turns}_R{red_turns}"
                    )
                elif blue_turns:
                    # Only blue turns are present
                    pattern_part = f"L{blue_turns}"
                elif red_turns:
                    # Only red turns are present
                    pattern_part = f"R{red_turns}"
                # if both turns are present and they are equal, return a single value
                elif blue_turns == red_turns:
                    pattern_part = f"{blue_turns}"
                else:
                    print(
                        "That's not right, turns aren't equal and neither is present."
                    )

                pattern_parts.append(pattern_part)
        return "_".join(pattern_parts)

    @staticmethod
    def pattern_to_sequence(pattern: str) -> list[dict]:
        """
        Convert a more readable pattern string back to a sequence format (abstract representation).
        This needs to handle the tuple format correctly.
        """
        sequence = []
        parts = pattern.split("_")
        for part in parts:
            blue_turns, red_turns = 0, 0
            if "L" in part:
                # Extract blue turns, handling tuple format
                blue_part = part[
                    part.index("L") + 1 : part.index(",") if "," in part else None
                ]
                blue_turns = float(blue_part) if blue_part else 0
            if "R" in part:
                # Extract red turns, handling tuple format
                red_part = (
                    part[part.index("R") + 1 :]
                    if "R" in part
                    else part[part.index(",") + 1 :]
                )
                red_turns = float(red_part) if red_part else 0
            sequence.append((blue_turns, red_turns))
        return sequence
