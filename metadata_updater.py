import os
import json
from PIL import Image, PngImagePlugin, UnidentifiedImageError
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class MetaDataUpdater:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget

    def update_metadata_for_images(self, directory):
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith((".png", ".jpg", ".jpeg")):
                    file_path = os.path.join(root, file)
                    self.update_metadata(file_path)

    def update_metadata(self, file_path):
        if os.path.getsize(file_path) == 0:
            print(f"Skipping empty file: {file_path}")
            return

        try:
            with Image.open(file_path) as img:
                metadata = img.info.get("metadata")
                if metadata:
                    metadata_dict = self.fix_metadata_structure(json.loads(metadata))
                    self.save_updated_metadata(file_path, img, metadata_dict)
                else:
                    print(f"No metadata found in {file_path}")
        except UnidentifiedImageError:
            print(f"Unidentified image file: {file_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    def fix_metadata_structure(self, metadata):
        # Initialize new metadata structure
        new_metadata = {
            "sequence": [],
            "date_added": None
        }

        # Extract and restructure metadata
        if isinstance(metadata, dict):
            # Handle nested "metadata_dict" key
            if "metadata_dict" in metadata:
                metadata = metadata["metadata_dict"]

            # Handle nested "sequence" and "date_added"
            if "sequence" in metadata and isinstance(metadata["sequence"], dict):
                sequence_list = metadata["sequence"].get("metadata_list", [])
                new_metadata["sequence"] = sequence_list

                # Extract date_added from the sequence
                date_added = metadata["sequence"].get("date_added")
                if date_added:
                    new_metadata["date_added"] = date_added

            # Top-level date_added handling
            if "date_added" in metadata:
                new_metadata["date_added"] = metadata["date_added"]

            # Fix missing date_added
            if not new_metadata["date_added"]:
                new_metadata["date_added"] = datetime.now().isoformat()

        return new_metadata

    def save_updated_metadata(self, file_path, img, metadata_dict):
        metadata_json = json.dumps(metadata_dict)
        info = PngImagePlugin.PngInfo()
        info.add_text("metadata", metadata_json)

        # Save the image with updated metadata
        img.save(file_path, "PNG", pnginfo=info)