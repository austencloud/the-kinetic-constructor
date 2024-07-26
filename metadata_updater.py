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

    def update_metadata(self, directory):
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
                        metadata_list = json.loads(metadata)
                        if isinstance(metadata_list, list):
                            metadata_dict = {"sequence": metadata_list}

                    if "date_added" not in metadata_dict:
                        metadata_dict["date_added"] = datetime.now().isoformat()
                        new_metadata = json.dumps(metadata_dict)

                        info = PngImagePlugin.PngInfo()
                        info.add_text("metadata", new_metadata)

                        image.save(file_path, "PNG", pnginfo=info)
                        print(f"Updated metadata for {file_path}")
