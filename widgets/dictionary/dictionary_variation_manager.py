import os
import json
from datetime import datetime
from PyQt6.QtWidgets import QInputDialog, QMessageBox, QTreeWidgetItem
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, List
if TYPE_CHECKING:
    from widgets.dictionary.dictionary import Dictionary


class DictionaryVariationManager:
    def __init__(self, dictionary: "Dictionary") -> None:
        self.dictionary = dictionary
        self.base_dictionary_folder = os.path.join(os.getcwd(), "dictionary")

    def create_variation(self, sequence_data: dict, base_pattern: str) -> None:
        # Ensure the base dictionary folder exists
        os.makedirs(self.base_dictionary_folder, exist_ok=True)

        # Create or ensure the base pattern folder exists
        pattern_folder = os.path.join(self.base_dictionary_folder, base_pattern)
        os.makedirs(pattern_folder, exist_ok=True)

        # Generate a timestamped filename for the new variation
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        variation_name = f"{base_pattern}_{timestamp}"
        variation_filename = f"{variation_name}.json"

        # Save the sequence data as a new variation file
        variation_filepath = os.path.join(pattern_folder, variation_filename)
        with open(variation_filepath, "w", encoding="utf-8") as file:
            json.dump(sequence_data, file, indent=4, ensure_ascii=False)

        # Add the new variation to the UI
        self.add_variation_to_ui(base_pattern, variation_name)

        # Optionally, select and highlight the new variation in the UI
        # self.select_variation_in_ui(variation_name)

    def rename_variation(self, base_pattern: str, current_variation_name: str) -> None:
        pattern_folder = os.path.join(self.base_dictionary_folder, base_pattern)
        current_filepath = os.path.join(
            pattern_folder, f"{current_variation_name}.json"
        )

        # Get the new name from the user
        new_variation_name, ok = QInputDialog.getText(
            self.dictionary, "Rename Variation", "Enter new variation name:"
        )

        if ok and new_variation_name:
            new_filepath = os.path.join(pattern_folder, f"{new_variation_name}.json")
            if not os.path.exists(new_filepath):
                os.rename(current_filepath, new_filepath)
                # Update the UI with the new variation name
                self.update_variation_name_in_ui(
                    current_variation_name, new_variation_name
                )
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

        # Confirm with the user before deletion
        confirm = QMessageBox.question(
            self.dictionary,
            "Delete Variation",
            f"Are you sure you want to delete the variation '{variation_name}'?",
        )

        if confirm == QMessageBox.StandardButton.Yes:
            os.remove(filepath)
            # Remove the variation from the UI

    def add_variation_to_ui(self, base_pattern: str, variation_name: str) -> None:
        # Find the base pattern item in the tree
        base_pattern_item = self.find_base_pattern_item(base_pattern)
        if not base_pattern_item:
            # If the base pattern item doesn't exist, create it
            base_pattern_item = QTreeWidgetItem(self.dictionary.words_tree.tree_view)
            base_pattern_item.setText(0, base_pattern)
            # Add the base pattern item to the top-level dictionary
            self.dictionary.words_tree.tree_view.addTopLevelItem(base_pattern_item)

        # Create a new item for the variation
        variation_item = QTreeWidgetItem(base_pattern_item)
        variation_item.setText(0, variation_name)
        # Store the variation file path as item data
        variation_item.setData(
            0,
            Qt.ItemDataRole.UserRole,
            os.path.join(
                self.base_dictionary_folder, base_pattern, f"{variation_name}.json"
            ),
        )

        # Expand the base pattern item to show the new variation
        base_pattern_item.setExpanded(True)


    def find_base_pattern_item(self, base_pattern: str) -> QTreeWidgetItem:
        # Iterate over the items in the tree to find the base pattern item
        for i in range(self.dictionary.words_tree.topLevelItemCount()):
            item = self.dictionary.words_tree.topLevelItem(i)
            if item.text(0) == base_pattern:
                return item
        return None

    def update_variation_name_in_ui(
        self, current_variation_name: str, new_variation_name: str
    ) -> None:
        # Find the item in the tree
        base_pattern_item = self.find_base_pattern_item(
            current_variation_name.split("_")[0]
        )
        if base_pattern_item:
            for i in range(base_pattern_item.childCount()):
                child = base_pattern_item.child(i)
                if child.text(0) == current_variation_name:
                    # Update the text of the item
                    child.setText(0, new_variation_name)
                    # Update the stored file path data
                    new_file_path = child.data(0, Qt.ItemDataRole.UserRole).replace(
                        current_variation_name, new_variation_name
                    )
                    child.setData(0, Qt.ItemDataRole.UserRole, new_file_path)
                    return
                
    def save_structural_variation(self, sequence_data: dict, base_pattern: str):
        # Ensure the base dictionary folder exists
        os.makedirs(self.base_dictionary_folder, exist_ok=True)

        # Create or ensure the base pattern folder exists
        pattern_folder = os.path.join(self.base_dictionary_folder, base_pattern)
        os.makedirs(pattern_folder, exist_ok=True)

        # Generate a timestamped filename for the new variation
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        variation_name = f"{base_pattern}_{timestamp}"
        variation_filename = f"{variation_name}.json"

        # Save the sequence data as a new variation file
        variation_filepath = os.path.join(pattern_folder, variation_filename)
        with open(variation_filepath, "w", encoding='utf-8') as file:
            json.dump(sequence_data, file, indent=4, ensure_ascii=False)

        # Add the new variation to the UI
        self.add_variation_to_ui(base_pattern, variation_name)

    def display_structural_variations(self, base_pattern: str):
        # Find or create the base pattern item in the tree
        base_pattern_item = self.find_base_pattern_item(base_pattern)
        if not base_pattern_item:
            base_pattern_item = QTreeWidgetItem(self.dictionary.words_tree.tree_view)
            base_pattern_item.setText(0, base_pattern)
            self.dictionary.words_tree.tree_view.addTopLevelItem(base_pattern_item)

        # Clear previous variations under this base pattern
        base_pattern_item.takeChildren()

        # List all structural variations from the folder and add them to the UI
        pattern_folder = os.path.join(self.base_dictionary_folder, base_pattern)
        for variation_filename in os.listdir(pattern_folder):
            if variation_filename.endswith('.json'):
                variation_name = variation_filename[:-5]  # Remove '.json'
                self.add_variation_to_ui(base_pattern, variation_name)

        base_pattern_item.setExpanded(True)

    def select_structural_variation(self, variation_name: str):
        base_pattern = variation_name.split('_')[0]
        # Load the selected structural variation into the sequence widget
        sequence_file_path = os.path.join(self.base_dictionary_folder, base_pattern, f"{variation_name}.json")
        self.dictionary.sequence_populator.load_sequence_from_file(sequence_file_path)

        # Display turn patterns for the selected structural variation
        