import os
from typing import TYPE_CHECKING
from PIL import Image
from PyQt6.QtWidgets import QMessageBox
import json

from utilities.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


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

    def get_sequence_author(self, file_path):
        metadata = self.extract_metadata_from_file(file_path)
        if metadata and "sequence" in metadata:
            return metadata["sequence"][0]["author"]
        return

    def get_sequence_level(self, file_path):
        metadata = self.extract_metadata_from_file(file_path)
        if metadata and "sequence" in metadata:
            return metadata["sequence"][0]["level"]
        return

    def get_sequence_length(self, file_path):
        metadata = self.extract_metadata_from_file(file_path)
        if metadata and "sequence" in metadata:
            return len(metadata["sequence"]) - 2
        return 0  # Default to 0 if no valid sequence length is found

    def get_sequence_start_position(self, file_path):
        metadata = self.extract_metadata_from_file(file_path)
        if metadata and "sequence" in metadata:
            return metadata["sequence"][1]["sequence_start_position"]
        return

    def get_metadata_and_thumbnail_dict(self) -> list[dict[str, str]]:
        """Collect all sequences and their metadata along with the associated thumbnail paths."""
        dictionary_dir = get_images_and_data_path("dictionary")
        metadata_and_thumbnail_dict = []

        for word in os.listdir(dictionary_dir):
            word_dir = os.path.join(dictionary_dir, word)
            if os.path.isdir(word_dir) and "__pycache__" not in word:
                thumbnails = self.main_widget.thumbnail_finder.find_thumbnails(word_dir)
                for thumbnail in thumbnails:
                    metadata = self.extract_metadata_from_file(thumbnail)
                    if metadata:
                        metadata_and_thumbnail_dict.append(
                            {"metadata": metadata, "thumbnail": thumbnail}
                        )

        return metadata_and_thumbnail_dict
