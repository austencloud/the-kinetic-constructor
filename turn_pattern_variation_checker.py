import json
import os
from PIL import Image


class TurnPatternVariationChecker:
    def __init__(self, directory) -> None:
        self.directory = directory

    def check_for_turn_pattern_variation(self, sequence) -> bool:
        for image_name in os.listdir(self.directory):
            if self.are_turns_patterns_identical(
                sequence, os.path.join(self.directory, image_name)
            ):
                return True
        return False

    def are_turns_patterns_identical(self, sequence, image_path) -> bool:
        with Image.open(image_path) as img:
            metadata = img.info.get("metadata")
            if metadata:
                return json.loads(metadata) == sequence
        return False
