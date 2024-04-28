import os


class StructuralVariationChecker:
    def __init__(self, dictionary_directory):
        self.dictionary_directory = dictionary_directory

    def check_for_structural_variation(self, sequence, get_base_word):
        base_word = get_base_word(sequence)
        version_number = 1
        while os.path.exists(
            os.path.join(self.dictionary_directory, f"{base_word}_v{version_number}")
        ):
            version_number += 1
        exists = os.path.exists(
            os.path.join(
                self.dictionary_directory, f"{base_word}_v{version_number - 1}"
            )
        )
        return exists, str(version_number)

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
