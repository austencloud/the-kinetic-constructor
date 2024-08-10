from typing import List, Dict


class SequenceDifficultyEvaluator:
    def __init__(self):
        self.RADIAL_ORIENTATIONS = {"in", "out"}

    def evaluate_difficulty(self, sequence: list[dict]) -> int:
        if len(sequence) < 3:
            return ""
        has_non_radial_orientation = False
        has_turns = False

        for entry in sequence[1:]:  # Skip the first entry with metadata
            if self._has_non_radial_orientation(entry):
                has_non_radial_orientation = True
            if self._has_turns(entry):
                has_turns = True

        if has_non_radial_orientation:
            return 3  # Level 3: Contains non-radial orientations
        elif has_turns:
            return 2  # Level 2: Contains turns
        else:
            return 1  # Level 1: No turns, only radial orientations

    def _has_turns(self, entry: dict) -> bool:
        return (
            entry["blue_attributes"]["turns"] > 0
            or entry["red_attributes"]["turns"] > 0
        )

    def _has_non_radial_orientation(self, entry: Dict) -> bool:
        blue_start_ori = entry["blue_attributes"]["start_ori"]
        blue_end_ori = entry["blue_attributes"]["end_ori"]
        red_start_ori = entry["red_attributes"]["start_ori"]
        red_end_ori = entry["red_attributes"]["end_ori"]
        return (
            blue_start_ori not in self.RADIAL_ORIENTATIONS
            or blue_end_ori not in self.RADIAL_ORIENTATIONS
            or red_start_ori not in self.RADIAL_ORIENTATIONS
            or red_end_ori not in self.RADIAL_ORIENTATIONS
        )
