import os
import json
from PIL import Image, PngImagePlugin

class PropTypeUpdater:
    def __init__(self, dictionary_path):
        self.dictionary_path = dictionary_path

    def update_all_prop_types(self):
        # Traverse through all files in the dictionary path
        for root, dirs, files in os.walk(self.dictionary_path):
            for file_name in files:
                if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
                    file_path = os.path.join(root, file_name)
                    self.update_prop_type_for_file(file_path)

    def update_prop_type_for_file(self, file_path):
        # Extract existing metadata from the image
        metadata = self.extract_metadata_from_file(file_path)

        if metadata and "sequence" in metadata:
            sequence = metadata["sequence"]

            if isinstance(sequence, list) and len(sequence) > 0:
                # Check the first item in the sequence
                first_item = sequence[0]
                
                if first_item.get("prop_type") == "unknown":
                    # Update prop_type to "staff"
                    first_item["prop_type"] = "staff"

                    # Save the updated metadata back to the image
                    self.save_metadata_to_image(file_path, metadata)
                    print(f"Updated prop_type to 'staff' for {file_path}")
                else:
                    print(f"Skipped: {file_path} (prop_type is not 'unknown')")
            else:
                print(f"Skipped: {file_path} (Invalid or insufficient sequence data)")
        else:
            print(f"Skipped: {file_path} (Invalid metadata structure)")

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
            print(f"Saved updated metadata for {file_path}")
        except Exception as e:
            print(f"Failed to save metadata to {file_path}: {e}")

if __name__ == "__main__":
    dictionary_path = "F:\\CODE\\tka-sequence-constructor\\dictionary"
    updater = PropTypeUpdater(dictionary_path)
    updater.update_all_prop_types()
