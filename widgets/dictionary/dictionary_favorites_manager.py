import os
import json
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtWidgets import QTreeView, QVBoxLayout, QHeaderView
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from widgets.turn_pattern_converter import TurnPatternConverter
if TYPE_CHECKING:
    from widgets.dictionary.dictionary import Dictionary

class DictionaryTurnPatternTree:
    def __init__(self, dictionary: "Dictionary") -> None:
        self.dictionary = dictionary
        self.turn_pattern_model = QStandardItemModel()
        self.turn_pattern_view = QTreeView()
        self.setup_ui(dictionary.layout)

    def setup_ui(self, layout: QVBoxLayout) -> None:
        self.turn_pattern_view.setModel(self.turn_pattern_model)
        self.turn_pattern_view.setHeaderHidden(True)
        self.turn_pattern_view.doubleClicked.connect(self.on_turn_pattern_double_clicked)
        layout.addWidget(self.turn_pattern_view)

    def display_turn_patterns_for_variation(self, base_pattern: str, structural_variation: str) -> None:
        self.turn_pattern_model.clear()  # Clear the existing list

        # Load the turn pattern files for the given structural variation
        pattern_folder = os.path.join(self.dictionary.variation_manager.base_dictionary_folder, base_pattern)
        structural_variation_path = os.path.join(pattern_folder, f"{structural_variation}.json")

        # Read the file to get turn patterns
        if os.path.exists(structural_variation_path):
            with open(structural_variation_path, "r") as file:
                sequence_data = json.load(file)
                # Extract turn patterns from the sequence data
                for turn_pattern in sequence_data.get("turn_patterns", []):
                    item = QStandardItem(turn_pattern["name"])
                    item.setData(turn_pattern, Qt.ItemDataRole.UserRole)  # Store the full turn pattern data
                    self.turn_pattern_model.appendRow(item)


    def on_turn_pattern_double_clicked(self, index: QModelIndex) -> None:
        item = self.turn_pattern_model.itemFromIndex(index)
        turn_pattern_str = item.text()  # Assuming the turn pattern string is directly the item text.
        # Convert the turn pattern string to a sequence format
        sequence = TurnPatternConverter.pattern_to_sequence(turn_pattern_str)

        # Now, apply this sequence to the current sequence in the sequence widget.
        # This requires a method in your sequence widget or its json handler that can take this sequence data and update the sequence widget accordingly.
        # For demonstration, let's say there's a method in the sequence widget's json handler called `update_sequence_with_pattern`.
        self.dictionary.sequence_widget.current_sequence_json_handler.update_sequence_with_pattern(sequence)
        
        # Optionally, show a notification or update the UI to reflect the change.
        self.dictionary.indicator_label.show_indicator("Turn pattern applied to the current sequence.")