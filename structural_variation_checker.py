import os
import json


class StructuralVariationChecker:
    def __init__(self, dictionary_directory):
        self.dictionary_directory = dictionary_directory

    def check_for_structural_variation(self, current_sequence, base_word):
        # Path where variations are stored
        base_path = os.path.join(self.dictionary_directory, base_word)
        if not os.path.exists(base_path):
            os.makedirs(base_path, exist_ok=True)

        # Iterate through existing files to check for identical structural variations
        for filename in os.listdir(base_path):
            if filename.endswith(".json"):
                with open(os.path.join(base_path, filename), "r") as file:
                    try:
                        existing_sequence = json.load(file)
                        if self.are_structural_variations_identical(
                            current_sequence, existing_sequence
                        ):
                            return (
                                True,
                                filename,
                            )  # Returns True and the existing filename if match is found
                    except json.JSONDecodeError:
                        continue  # In case of a bad file, just skip it

        # No match found 
        return False, "1"

    def are_structural_variations_identical(self, seq1, seq2):
        def structural_variation_matches(b1, b2):
            ignored_keys = ["turns", "end_ori", "start_ori"]
            for key in b1.keys():
                if key not in ignored_keys and b1[key] != b2[key]:
                    return False
            return True

        if len(seq1) != len(seq2):
            return False

        for beat1, beat2 in zip(seq1, seq2):
            for color in ["blue_attributes", "red_attributes"]:
                if color in beat1 and color in beat2:
                    if not structural_variation_matches(beat1[color], beat2[color]):
                        return False
        return True
