import os
import json
from datetime import datetime
from PyQt6.QtWidgets import QInputDialog, QMessageBox
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.dictionary.dictionary import Dictionary


class DictionaryVariationManager:
    def __init__(self, dictionary: "Dictionary") -> None:
        self.dictionary = dictionary
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

    def save_structural_variation(self, sequence_data: dict, base_pattern: str) -> None:
        """
        Saves or updates a structural variation for a given base pattern.
        This might involve creating a new variation file or updating an existing one.
        The exact implementation can vary based on application needs.
        """
        pattern_folder = os.path.join(self.base_dictionary_folder, base_pattern)
        os.makedirs(pattern_folder, exist_ok=True)

        year = datetime.now().strftime("%y")
        month = datetime.now().strftime("%m").lstrip("0")
        day = datetime.now().strftime("%d").lstrip("0")
        
        timestamp = datetime.now().strftime(f"{month}-{day}-{year}")
        variation_name = f"{base_pattern}_{timestamp}.json"
        variation_filepath = os.path.join(pattern_folder, variation_name)

        with open(variation_filepath, "w", encoding="utf-8") as file:
            json.dump(sequence_data, file, indent=4, ensure_ascii=False)
