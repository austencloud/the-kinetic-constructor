import os
import json
from datetime import datetime
import sys
from PyQt6.QtWidgets import QInputDialog, QMessageBox
from PyQt6.QtGui import QImage
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.dictionary.dictionary_widget import DictionaryWidget


class DictionaryVariationManager:
    def __init__(self, dictionary: "DictionaryWidget") -> None:
        self.dictionary = dictionary
        if getattr(sys, "frozen", False):
            # Running in a PyInstaller bundle
            self.base_dictionary_folder = os.path.join(
                os.getenv("LOCALAPPDATA"), "The Kinetic Alphabet", "dictionary"
            )
        else:
            # Running in a development environment
            self.base_dictionary_folder = os.path.join(os.getcwd(), "dictionary")

    def create_variation(self, sequence_data: dict, base_pattern: str) -> None:
        pattern_folder = os.path.join(self.base_dictionary_folder, base_pattern)
        os.makedirs(pattern_folder, exist_ok=True)

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        variation_name = f"{base_pattern}_{timestamp}.json"
        variation_filepath = os.path.join(pattern_folder, variation_name)

        with open(variation_filepath, "w", encoding="utf-8") as file:
            json.dump(sequence_data, file, indent=4, ensure_ascii=False)

    def rename_variation(self, base_pattern: str, current_variation_name: str) -> None:
        pattern_folder = os.path.join(self.base_dictionary_folder, base_pattern)
        current_filepath = os.path.join(
            pattern_folder, f"{current_variation_name}.json"
        )

        new_variation_name, ok = QInputDialog.getText(
            self.dictionary,
            "Rename Variation",
            "Enter new variation name:",
            text=current_variation_name[:-5],
        )

        if ok and new_variation_name and new_variation_name != current_variation_name:
            new_filepath = os.path.join(pattern_folder, f"{new_variation_name}.json")
            if not os.path.exists(new_filepath):
                os.rename(current_filepath, new_filepath)
            else:
                QMessageBox.warning(
                    self.dictionary,
                    "Rename Error",
                    "A variation with this name already exists.",
                )

    def delete_variation(self, base_pattern: str, variation_name: str) -> None:
        filepath = os.path.join(
            self.base_dictionary_folder, base_pattern, f"{variation_name}.json"
        )

        confirm = QMessageBox.question(
            self.dictionary,
            "Delete Variation",
            f"Are you sure you want to delete the variation '{variation_name}'?",
        )

        if confirm == QMessageBox.StandardButton.Yes:
            os.remove(filepath)

    def select_structural_variation(self, variation_name: str):
        base_pattern = variation_name.split("_")[0]
        sequence_file_path = os.path.join(
            self.base_dictionary_folder, base_pattern, f"{variation_name}.json"
        )

        if os.path.exists(sequence_file_path):
            self.dictionary.sequence_populator.load_sequence_from_file(
                sequence_file_path
            )
        else:
            QMessageBox.warning(
                self.dictionary,
                "Variation Not Found",
                f"The variation '{variation_name}' could not be found.",
            )

    def _get_next_version_filename(self, base_path, base_name, extension):
        version = 1
        while True:
            versioned_filename = f"{base_name}_v{version}{extension}"
            if not os.path.exists(os.path.join(base_path, versioned_filename)):
                return versioned_filename
            version += 1

    def save_structural_variation(
        self, sequence_data: dict, base_pattern: str, thumbnail_path: str
    ) -> None:
        # Ensure the pattern folder for JSON exists
        pattern_folder_json = os.path.join(self.base_dictionary_folder, base_pattern)
        os.makedirs(pattern_folder_json, exist_ok=True)

        pattern_folder_thumb = os.path.join(thumbnail_path, base_pattern)
        os.makedirs(pattern_folder_thumb, exist_ok=True)

        # Find the next version for JSON
        existing_json = self._get_existing_variations(pattern_folder_json, base_pattern)
        json_filename = self._get_next_version_filename(
            pattern_folder_json, base_pattern, ".json"
        )

        # Find the next version for thumbnail
        thumbnail_filename = self._get_next_version_filename(
            pattern_folder_thumb, base_pattern, ".png"
        )

        # Save JSON
        variation_json_path = os.path.join(pattern_folder_json, json_filename)
        with open(variation_json_path, "w", encoding="utf-8") as file:
            json.dump(sequence_data, file, indent=4, ensure_ascii=False)

        # Save Thumbnail
        variation_thumb_path = os.path.join(pattern_folder_thumb, thumbnail_filename)
        thumbnail_image = QImage(
            thumbnail_path
        )  # Assuming thumbnail_path is the path to the image in memory
        thumbnail_image.save(variation_thumb_path, "PNG")

        return variation_json_path, variation_thumb_path

    def _get_existing_variations(self, pattern_folder: str, base_pattern: str) -> list:
        # List all files in the pattern folder that start with the base pattern
        return [
            filename
            for filename in os.listdir(pattern_folder)
            if filename.startswith(base_pattern) and filename.endswith(".json")
        ]

    def _get_next_version_number(self, existing_variations: list) -> int:
        # Extract version numbers from the existing files
        version_numbers = [
            int(filename.split("_v")[-1].split(".json")[0])
            for filename in existing_variations
            if "_v" in filename
        ]
        if not version_numbers:
            return 1
        return max(version_numbers) + 1

    def get_variation_filepath(self, base_pattern: str, variation_name: str) -> str:
        if getattr(sys, "frozen", False):
            return os.path.join(
                os.getenv("LOCALAPPDATA"),
                "The Kinetic Alphabet",
                "dictionary",
                base_pattern,
                f"{variation_name}.json",
            )
        else:
            return os.path.join(
                os.getcwd(), "dictionary", base_pattern, f"{variation_name}.json"
            )
