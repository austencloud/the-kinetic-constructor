from typing import TYPE_CHECKING

from PyQt6.QtGui import (
    QStandardItemModel,
    QStandardItem,
)
if TYPE_CHECKING:
    from widgets.library.library import Library


class LibrarySequenceLengthManager:
    def __init__(self, library: "Library") -> None:
        self.library = library

    def sort_sequences_by_length(self) -> None:
        sequences = [
            (
                self.compute_display_length(item.text()),
                item.text().replace(".json", ""),
                item,
            )
            for item in self.extract_items(self.library.model)
        ]
        sequences.sort(key=lambda x: x[0])
        self.library.model.clear()
        for length, name, item in sequences:
            self.library.model.appendRow(item)

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
