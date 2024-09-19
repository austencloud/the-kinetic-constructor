from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.add_to_dictionary_manager.add_to_dictionary_manager import AddToDictionaryManager

class TurnPatternConverter:
    def __init__(self, add_to_dictionary_manager: "AddToDictionaryManager"):
        self.add_to_dictionary_manager = add_to_dictionary_manager

    def sequence_to_pattern(self, sequence: list[dict]) -> str:
        """
        Convert sequence data to a more readable turn pattern string, including tuples for differing turns.
        Format turns in a beat using just the numbers separated by a comma, and different beats using an underscore.
        """
        pattern_parts = []
        for item in sequence:
            if "sequence_start_position" in item or "prop_type" in item:
                continue  # Skip the item with the starting position key

            blue_attributes = item["blue_attributes"]
            red_attributes = item["red_attributes"]
            blue_turns = blue_attributes.get("turns", 0)
            red_turns = red_attributes.get("turns", 0)

            pattern_part = (
                f"{blue_turns},{red_turns}" if blue_turns or red_turns else "0"
            )
            pattern_parts.append(pattern_part)

        return "_".join(pattern_parts)

    def pattern_to_sequence(self, pattern: str) -> list[dict]:
        """
        Convert a more readable pattern string back to a sequence format (abstract representation).
        Handles parts split by underscores, with turns in each part split by a comma.
        """
        sequence = []
        parts = pattern.split("_")
        for part in parts:
            if "," in part:
                blue_turns, red_turns = map(float, part.split(","))
            else:
                blue_turns, red_turns = float(part), 0
            sequence.append({"blue_turns": blue_turns, "red_turns": red_turns})
        return sequence
