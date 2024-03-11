from typing import TYPE_CHECKING

from PyQt6.QtGui import (
    QStandardItemModel,
    QStandardItem,
)

if TYPE_CHECKING:
    from widgets.dictionary.dictionary import Dictionary


class DictionarySortByLengthManager:
    def __init__(self, dictionary: "Dictionary") -> None:
        self.dictionary = dictionary

    def sort_sequences_by_length(self) -> None:
        sequences = [
            (
                self.compute_display_length(item.text()),
                item.text().replace(".json", ""),
                item,
            )
            for item in self.extract_items(self.dictionary.model)
        ]
        sequences.sort(key=lambda x: x[0])
        self.dictionary.model.clear()
        for length, name, item in sequences:
            self.dictionary.model.appendRow(item)

    @staticmethod
    def compute_display_length(name: str) -> int:
        count = 0
        skip_next = False
        for i, char in enumerate(name):
            if skip_next:
                skip_next = False
                continue
            if char == "-" and i + 1 < len(name):
                count += 1
                skip_next = True
            else:
                count += 1

    @staticmethod
    def extract_items(model: QStandardItemModel) -> list[QStandardItem]:
        items = []
        for row in range(model.rowCount()):
            items.append(model.item(row))
        return items

    def filter_sequences_by_length(self):
        # Implement the logic to filter sequences based on the updated visibility settings
        # This could involve iterating through the items in your tree model and hiding/showing based on length
        pass