import os
import json
from datetime import datetime
from PIL import Image, PngImagePlugin

from widgets.path_helpers.path_helpers import get_images_and_data_path


def update_metadata(directory):
    for root, _, files in os.walk(directory):
        if "__pycache__" in root:
            continue
        for file in files:
            if file.endswith((".png", ".jpg", ".jpeg")):
                file_path = os.path.join(root, file)
                image = Image.open(file_path)
                info = image.info
                metadata = info.get("metadata")

                if metadata:
                    metadata_dict = json.loads(metadata)
                else:
                    metadata_dict = {}

                if "date_added" not in metadata_dict:
                    metadata_dict["date_added"] = datetime.now().isoformat()
                    new_metadata = json.dumps(metadata_dict)

                    info = PngImagePlugin.PngInfo()
                    info.add_text("metadata", new_metadata)

                    image.save(file_path, "PNG", pnginfo=info)
                    print(f"Updated metadata for {file_path}")


# Run the script on your dictionary directory
dictionary_dir = get_images_and_data_path("dictionary")
update_metadata(dictionary_dir)
print("Metadata update complete.")