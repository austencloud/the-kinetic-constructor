from typing import TYPE_CHECKING

from PyQt6.QtGui import (
    QStandardItemModel,
    QStandardItem,
)

if TYPE_CHECKING:
    from widgets.dictionary.dictionary import Dictionary


class DictionarySortByLengthHandler:
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
    def extract_items(model: QStandardItemModel) -> list[QStandardItem]:
        items = []
        for row in range(model.rowCount()):
            items.append(model.item(row))
        return items

    def filter_sequences_by_length(self):
        visibility_settings = (
            self.dictionary.main_widget.main_window.settings_manager.get_word_length_visibility()
        )
        model = self.dictionary.words_tree.model

        for i in range(model.rowCount()):
            item = model.item(i)
            if item:  # Safety check
                sequence_name = item.text()
                sequence_length = self.compute_display_length(sequence_name)
                should_be_visible = visibility_settings.get(sequence_length, False)
                item.setHidden(not should_be_visible)
