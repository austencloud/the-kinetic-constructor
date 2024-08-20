import os
import json
from PIL import Image, PngImagePlugin
from sequence_difficulty_evaluator import SequenceLevelEvaluator
from widgets.path_helpers.path_helpers import get_user_editable_resource_path

import os
import json
from PIL import Image, PngImagePlugin


"""This class is created so that we can update the metadata of all of the images that currently exist within the dictionary, 
without having to rely on the main widget. 
It's going to need to be updated once I update the sequence properties checker 
in order to make it so that it can detect whether a sequence is a mirrored permutation or a color swaped permutation."""


class SequencePropertiesCheckerStandalone:
    def __init__(self, sequence):
        self.sequence = sequence[1:] if sequence else []

        self.ends_at_start_pos = False
        self.is_permutable = False
        self.is_strictly_rotational_permutation = False
        self.is_strictly_mirrored_permutation = False
        self.is_strictly_colorswapped_permutation = False
        self.is_mirror_and_color_swapped_permutation = False
        self.is_rotational_colorswapped_permutation = False

    def check_properties(self):
        if not self.sequence:
            return {
                "author": "Austen Cloud",
                "level": 0,
                "is_circular": False,
                "is_permutable": False,
                "is_strictly_rotational_permutation": False,
                "is_strictly_mirrored_permutation": False,
                "is_strictly_colorswapped_permutation": False,
                "is_mirror_and_color_swapped_permutation": False,
                "is_rotational_colorswapped_permutation": False,
            }

        self.ends_at_start_pos = self._check_ends_at_start_pos()
        self.is_permutable = self._check_is_permutable()
        self.is_strictly_rotational_permutation = (
            self._check_is_rotational_permutation()
        )
        self.is_strictly_mirrored_permutation = self._check_is_mirrored_permutation()
        self.is_strictly_colorswapped_permutation = (
            self._check_is_colorswapped_permutation()
        )
        self.is_mirror_and_color_swapped_permutation = (
            self.check_is_mirrored_and_color_swapped_permutation()
        )
        self.is_rotational_colorswapped_permutation = (
            self.check_is_rotational_and_colorswapped_permutation()
        )

        # Assuming you have a method or a way to calculate level
        level = self._calculate_sequence_level()

        return {
            "author": "Austen Cloud",
            "level": level,
            "is_circular": self.ends_at_start_pos,
            "is_permutable": self.is_permutable,
            "is_strictly_rotational_permutation": self.is_strictly_rotational_permutation,
            "is_strictly_mirrored_permutation": self.is_strictly_mirrored_permutation,
            "is_strictly_colorswapped_permutation": self.is_strictly_colorswapped_permutation,
            "is_mirror_and_color_swapped_permutation": self.is_mirror_and_color_swapped_permutation,
            "is_rotational_colorswapped_permutation": self.is_rotational_colorswapped_permutation,
        }

    def _check_ends_at_start_pos(self) -> bool:
        start_position = self.sequence[0]["end_pos"]  # Assuming the first position
        current_position = self.sequence[-1]["end_pos"]  # Assuming the last position
        return current_position == start_position

    def _check_is_permutable(self) -> bool:
        start_position = self.sequence[0]["end_pos"].rstrip("0123456789")
        current_position = self.sequence[-1]["end_pos"].rstrip("0123456789")
        return current_position == start_position

    def _check_is_rotational_permutation(self) -> bool:
        letter_sequence = [
            entry["letter"] for entry in self.sequence if "letter" in entry
        ]
        unique_letters = set(letter_sequence)
        for letter in unique_letters:
            occurrences = [i for i, x in enumerate(letter_sequence) if x == letter]
            if len(occurrences) > 1:
                for i in range(1, len(occurrences)):
                    prev = self.sequence[occurrences[i - 1]]
                    curr = self.sequence[occurrences[i]]
                    if not self._is_rotational_permutation(prev, curr):
                        return False
        return True

    def _is_rotational_permutation(self, prev, curr) -> bool:
        return (
            prev["blue_attributes"]["motion_type"]
            == curr["blue_attributes"]["motion_type"]
            and prev["blue_attributes"]["prop_rot_dir"]
            == curr["blue_attributes"]["prop_rot_dir"]
            and prev["red_attributes"]["motion_type"]
            == curr["red_attributes"]["motion_type"]
            and prev["red_attributes"]["prop_rot_dir"]
            == curr["red_attributes"]["prop_rot_dir"]
        )

    def _check_is_mirrored_permutation(self) -> bool:
        # Add logic to determine if the sequence is a mirrored permutation
        return False  # Placeholder, needs actual logic

    def _check_is_colorswapped_permutation(self) -> bool:
        # Add logic to determine if the sequence is a color-swapped permutation
        return False  # Placeholder, needs actual logic

    def _calculate_sequence_level(self) -> int:
        # Here we can integrate your level evaluator logic or hardcode levels based on the sequence complexity
        # This function should replace the direct call to `main_widget.sequence_level_evaluator`
        has_non_radial_orientation = any(
            self._has_non_radial_orientation(entry) for entry in self.sequence
        )
        has_turns = any(self._has_turns(entry) for entry in self.sequence)

        if has_non_radial_orientation:
            return 3  # Level 3: Contains non-radial orientations
        elif has_turns:
            return 2  # Level 2: Contains turns
        else:
            return 1  # Level 1: No turns, only radial orientations

    def _has_turns(self, entry) -> bool:
        return (
            entry["blue_attributes"]["turns"] > 0
            or entry["red_attributes"]["turns"] > 0
        )

    def _has_non_radial_orientation(self, entry) -> bool:
        radial_orientations = {"in", "out"}
        blue_start_ori = entry["blue_attributes"]["start_ori"]
        blue_end_ori = entry["blue_attributes"]["end_ori"]
        red_start_ori = entry["red_attributes"]["start_ori"]
        red_end_ori = entry["red_attributes"]["end_ori"]
        return (
            blue_start_ori not in radial_orientations
            or blue_end_ori not in radial_orientations
            or red_start_ori not in radial_orientations
            or red_end_ori not in radial_orientations
        )


class StandaloneMetaDataExtractor:
    def extract_metadata_from_file(self, file_path):
        if not file_path:
            return None

        try:
            with Image.open(file_path) as img:
                metadata = img.info.get("metadata")
                if metadata:
                    return json.loads(metadata)
        except Exception as e:
            print(f"Error loading sequence from thumbnail: {e}")
        return None


class MetadataUpdater:
    def __init__(self, dictionary_path, default_author="Austen Cloud"):
        self.metadata_extractor = StandaloneMetaDataExtractor()
        self.dictionary_path = dictionary_path
        self.default_author = default_author

    def update_all_metadata(self):
        # Traverse through all files in the dictionary path
        for root, dirs, files in os.walk(self.dictionary_path):
            for file_name in files:
                if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
                    file_path = os.path.join(root, file_name)
                    self.update_metadata_for_file(file_path)

    def update_metadata_for_file(self, file_path):
        # Extract existing metadata from the image
        metadata = self.metadata_extractor.extract_metadata_from_file(file_path)

        if metadata:
            sequence = metadata.get("sequence", [])
            # Use the SequencePropertiesCheckerStandalone to determine sequence properties
            sequence_checker = SequencePropertiesCheckerStandalone(sequence)
            sequence_properties = sequence_checker.check_properties()

            # Update the metadata with the sequence properties
            sequence_metadata = {
                "author": self.default_author,
                "level": sequence_properties["level"],
                "prop_type": metadata.get("prop_type", "unknown"),
                "is_circular": sequence_properties["is_circular"],
                "is_permutable": sequence_properties["is_permutable"],
                "is_strictly_rotational_permutation": sequence_properties[
                    "is_strictly_rotational_permutation"
                ],
                "is_strictly_mirrored_permutation": sequence_properties[
                    "is_strictly_mirrored_permutation"
                ],
                "is_strictly_colorswapped_permutation": sequence_properties[
                    "is_strictly_colorswapped_permutation"
                ],
                "is_mirror_and_color_swapped_permutation": sequence_properties[
                    "is_mirror_and_color_swapped_permutation"
                ],
                "is_rotational_colorswapped_permutation": sequence_properties[
                    "is_rotational_colorswapped_permutation"
                ],
            }

            # Prepend the sequence metadata to the sequence
            sequence.insert(0, sequence_metadata)
            metadata["sequence"] = sequence
        else:
            # If no metadata exists, create a new one
            metadata = {
                "sequence": [
                    {
                        "author": self.default_author,
                        "level": 0,
                        "prop_type": "unknown",
                        "is_circular": False,
                        "is_permutable": False,
                        "is_strictly_rotational_permutation": False,
                        "is_strictly_mirrored_permutation": False,
                        "is_strictly_colorswapped_permutation": False,
                        "is_mirror_and_color_swapped_permutation": False,
                        "is_rotational_colorswapped_permutation": False,
                    }
                ]
            }

        # Save the updated metadata back to the image
        self.save_metadata_to_image(file_path, metadata)

    def save_metadata_to_image(self, file_path, metadata):
        try:
            with Image.open(file_path) as img:
                # Prepare the metadata to be saved
                meta = PngImagePlugin.PngInfo()
                meta.add_text("metadata", json.dumps(metadata))

                img.save(file_path, "PNG", pnginfo=meta)
            print(f"Saved metadata to {file_path}")
        except Exception as e:
            print(f"Failed to save metadata to {file_path}: {e}")


# To execute the metadata update process
if __name__ == "__main__":
    dictionary_path = "F:\\CODE\\tka-sequence-constructor\\dictionary"
    updater = MetadataUpdater(dictionary_path)
    updater.update_all_metadata()
