from typing import TYPE_CHECKING
from PIL import Image
from PyQt6.QtWidgets import QMessageBox
import json
if TYPE_CHECKING:
    from widgets.dictionary_widget.thumbnail_box.thumbnail_box import ThumbnailBox


class MetaDataExtractor:
    def __init__(self, thumbanil_box: "ThumbnailBox"):
        self.thumbanil_box = thumbanil_box

    def extract_metadata_from_file(self, file_path):
        try:
            with Image.open(file_path) as img:
                metadata = img.info.get("metadata")
                if metadata:
                    return json.loads(metadata)
                else:
                    QMessageBox.warning(
                        self.thumbanil_box.main_widget,
                        "Error",
                        "No sequence metadata found in the thumbnail.",
                    )
        except Exception as e:
            QMessageBox.critical(
                self.thumbanil_box.main_widget,
                "Error",
                f"Error loading sequence from thumbnail: {e}",
            )
