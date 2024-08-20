import os
import json
from PIL import Image, PngImagePlugin

class MetadataCleaner:
    def __init__(self, dictionary_path):
        self.dictionary_path = dictionary_path

    def clean_all_metadata(self):
        # Traverse through all files in the dictionary path
        for root, dirs, files in os.walk(self.dictionary_path):
            for file_name in files:
                if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
                    file_path = os.path.join(root, file_name)
                    self.clean_metadata_for_file(file_path)

    def clean_metadata_for_file(self, file_path):
        # Extract existing metadata from the image
        metadata = self.extract_metadata_from_file(file_path)

        if metadata and "sequence" in metadata:
            sequence = metadata["sequence"]

            if isinstance(sequence, list) and len(sequence) > 1:
                # Look for and remove any unwanted properties dictionaries in the sequence
                sequence = [
                    item for item in sequence 
                    if not self._is_unwanted_properties_dict(item)
                ]

                # Update the metadata with the cleaned sequence
                metadata["sequence"] = sequence

                # Save the cleaned metadata back to the image
                self.save_metadata_to_image(file_path, metadata)
                print(f"Cleaned metadata for {file_path}")
            else:
                print(f"Skipped: {file_path} (Invalid or insufficient sequence data)")
        else:
            print(f"Skipped: {file_path} (Invalid metadata structure)")

    def _is_unwanted_properties_dict(self, item):
        """
        Determines if the given item is an unwanted properties dictionary.
        An unwanted properties dictionary typically contains only metadata-related keys.
        """
        return (
            isinstance(item, dict) and
            "prop_type" in item and
            "is_circular" in item and
            "is_permutable" in item
        )

    def extract_metadata_from_file(self, file_path):
        try:
            with Image.open(file_path) as img:
                metadata = img.info.get("metadata")
                if metadata:
                    return json.loads(metadata)
        except Exception as e:
            print(f"Error loading metadata from {file_path}: {e}")
        return None

    def save_metadata_to_image(self, file_path, metadata):
        try:
            with Image.open(file_path) as img:
                # Prepare the metadata to be saved
                meta = PngImagePlugin.PngInfo()
                meta.add_text("metadata", json.dumps(metadata))

                img.save(file_path, "PNG", pnginfo=meta)
            print(f"Saved cleaned metadata for {file_path}")
        except Exception as e:
            print(f"Failed to save metadata to {file_path}: {e}")

if __name__ == "__main__":
    dictionary_path = "F:\\CODE\\tka-sequence-constructor\\dictionary"
    cleaner = MetadataCleaner(dictionary_path)
    cleaner.clean_all_metadata()
