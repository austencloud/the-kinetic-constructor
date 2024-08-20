import os
import json
from PIL import Image, PngImagePlugin
from sequence_difficulty_evaluator import SequenceLevelEvaluator
from widgets.path_helpers.path_helpers import get_user_editable_resource_path

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
        self.sequence_level_evaluator = SequenceLevelEvaluator()
        self.dictionary_path = dictionary_path
        self.default_author = default_author

    def update_all_metadata(self):
        # Traverse through all files in the dictionary path
        for root, dirs, files in os.walk(self.dictionary_path):
            for file_name in files:
                if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    file_path = os.path.join(root, file_name)
                    self.update_metadata_for_file(file_path)

    def update_metadata_for_file(self, file_path):
        # Extract existing metadata from the image
        metadata = self.metadata_extractor.extract_metadata_from_file(file_path)

        sequence = metadata.get("sequence", [])
        # Update the metadata dictionary with author and level
        sequence_metadata = {
            "author": self.default_author,
            "level": self.sequence_level_evaluator.get_sequence_level(sequence),
            "prop_type": metadata.get("prop_type", "unknown"),
            "is_circular": metadata.get("is_circular", False),
            "is_permutable": metadata.get("is_permutable", False),
            "is_rotational_permutation": metadata.get("is_rotational_permutation", False),
            "is_mirrored_permutation": metadata.get("is_mirrored_permutation", False),
            "is_colorswapped_permutation": metadata.get("is_colorswapped_permutation", False),
        }

        # Prepend the sequence metadata to the sequence
        sequence.insert(0, sequence_metadata)
        metadata["sequence"] = sequence

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
