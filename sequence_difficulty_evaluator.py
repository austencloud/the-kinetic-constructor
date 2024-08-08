from typing import List, Dict


class SequenceDifficultyEvaluator:
    def __init__(self):
        self.RADIAL_ORIENTATIONS = {"in", "out"}

    def evaluate_difficulty(self, sequence: List[Dict]) -> int:
        for entry in sequence[1:]:  # Skip the first entry with metadata
            if self._has_non_radial_orientation(entry):
                return 3  # Level 3: Contains non-radial orientations
            if self._has_turns(entry):
                return 2  # Level 2: Contains turns
        return 1  # Level 1: No turns, only radial orientations

    def _has_turns(self, entry: Dict) -> bool:
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
