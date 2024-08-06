from typing import TYPE_CHECKING
from PIL import Image
from PyQt6.QtWidgets import QMessageBox
import json

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class MetaDataExtractor:
    def __init__(self, main_widget: "MainWidget"):
        self.main_widget = main_widget

    def extract_metadata_from_file(self, file_path):
        # Check if a file exists at the path we're passing as "file_path"
        if not file_path:
            return None

        try:
            with Image.open(file_path) as img:
                metadata = img.info.get("metadata")
                if metadata:
                    return json.loads(metadata)
                else:
                    QMessageBox.warning(
                        self.main_widget,
                        "Error",
                        "No sequence metadata found in the thumbnail.",
                    )
        except Exception as e:
            QMessageBox.critical(
                self.main_widget,
                "Error",
                f"Error loading sequence from thumbnail: {e}",
            )
        return None

    def get_sequence_length(self, file_path):
        metadata = self.extract_metadata_from_file(file_path)
        if metadata and "sequence" in metadata:
            return len(metadata["sequence"]) - 2
        return 0  # Default to 0 if no valid sequence length is found
