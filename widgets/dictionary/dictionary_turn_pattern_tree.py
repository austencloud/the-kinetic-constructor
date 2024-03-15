import os
import json
from typing import TYPE_CHECKING
from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtWidgets import QTreeView, QVBoxLayout, QHeaderView
from PyQt6.QtGui import QStandardItemModel, QStandardItem

from widgets.turn_pattern_converter import TurnPatternConverter

if TYPE_CHECKING:
    from widgets.dictionary.dictionary import Dictionary


class DictionaryTurnPatternTree(QTreeView):
    def __init__(self, dictionary: "Dictionary") -> None:
        super().__init__(dictionary)
        self.dictionary = dictionary
        self.turn_pattern_model = QStandardItemModel()
        self.setup_ui(dictionary.layout)

    def setup_ui(self, layout: QVBoxLayout) -> None:
        self.setModel(self.turn_pattern_model)
        self.setHeaderHidden(True)
        self.doubleClicked.connect(self.on_turn_pattern_double_clicked)
        layout.addWidget(self)

    def display_turn_patterns_for_variation(
        self, base_pattern: str, structural_variation: str
    ) -> None:
        self.turn_pattern_model.clear()  # Clear the existing list

        self.pattern_folder = os.path.join(
            self.dictionary.variation_manager.base_dictionary_folder, base_pattern
        )
        self.structural_variation_path = os.path.join(
            self.pattern_folder, f"{structural_variation}.json"
        )

        if os.path.exists(self.structural_variation_path):
            with open(self.structural_variation_path, "r") as file:
                sequence_data = json.load(file)
                turn_pattern = TurnPatternConverter.sequence_to_pattern(sequence_data)
                item = QStandardItem(turn_pattern)
                item.setData(turn_pattern, Qt.ItemDataRole.UserRole)
                self.turn_pattern_model.appendRow(item)

    def on_turn_pattern_double_clicked(self, index: QModelIndex) -> None:
        if os.path.exists(self.structural_variation_path):
            with open(self.structural_variation_path, "r") as file:
                sequence_data = json.load(file)
                self.dictionary.sequence_populator.populate_sequence(sequence_data)
        
