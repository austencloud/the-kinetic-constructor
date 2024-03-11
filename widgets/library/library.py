import os
import json
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QMessageBox, QTreeView, QHBoxLayout
from PyQt6.QtCore import QModelIndex, Qt
from PyQt6.QtGui import QStandardItem, QDragEnterEvent, QDropEvent
from Enums.letters import Letter, LetterConditions
from .library_favorites_manager import LibraryFavoritesManager
from .library_search_sort_bar import LibrarySearchSortBar
from .library_sequence_length_manager import LibrarySequenceLengthManager
from .library_sequence_loader import LibrarySequenceLoader

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class Library(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget

        self.setup_ui()

    def _init_references(self):
        self.json_handler = self.main_widget.json_manager.current_sequence_json_handler
        self.start_pos_view = self.main_widget.sequence_widget.beat_frame.start_pos_view
        self.start_pos_manager = (
            self.main_widget.main_tab_widget.sequence_builder.start_pos_picker.start_pos_manager
        )
        self.sequence_widget = self.main_widget.sequence_widget
        self.sequence_builder = self.main_widget.main_tab_widget.sequence_builder

    def setup_ui(self) -> None:
        main_layout = QVBoxLayout(self)
        tree_layout = QHBoxLayout()
        self.search_sort_bar = LibrarySearchSortBar(self)
        self.favorites_manager = LibraryFavoritesManager(self)
        self.sequence_loading = LibrarySequenceLoader(self)
        self.sequence_length_management = LibrarySequenceLengthManager(self)
        self.search_sort_bar.setup_ui(main_layout)
        self.sequence_loading.setup_ui(main_layout)
        self.favorites_manager.setup_ui(tree_layout)
        self.setup_preview_area(tree_layout)
        self.setLayout(main_layout)

    def filter_sequences(self, text: str) -> None:
        search_text = text.lower()
        for i in range(self.sequence_loading.model.rowCount()):
            item = self.sequence_loading.model.item(i)
            file_name = item.text().lower()
            item.setHidden(search_text not in file_name)

    def sort_sequences(self, criteria: str) -> None:
        if criteria == "Name":
            self.sequence_loading.proxy_model.sort(0)
            self.sequence_loading.proxy_model.lengthSortingEnabled = False
        elif criteria == "Length":
            self.sequence_loading.proxy_model.lengthSortingEnabled = True
            self.sequence_loading.proxy_model.invalidate()

    def sort_sequences_by_start_position(self) -> None:
        sequences = []
        for item in self.sequence_loading.extract_items(self.sequence_loading.model):
            file_name = item.text().replace(".json", "")
            start_letter_enum = self.get_starting_position_from_sequence_name(file_name)
            sequences.append((start_letter_enum, file_name, item))
        sequences.sort(key=lambda x: (x[0].name, x[1]))
        self.sequence_loading.model.clear()
        for _, name, item in sequences:
            self.sequence_loading.model.appendRow(item)

    @staticmethod
    def get_starting_position_from_sequence_name(name: str) -> Letter:
        for letter in Letter:
            if (
                name.startswith(letter.value)
                and letter
                in LetterConditions.ALPHA_STARTING.value
                + LetterConditions.BETA_STARTING.value
                + LetterConditions.GAMMA_STARTING.value
            ):
                return letter
        return Letter.A

    def setup_preview_area(self, layout: QVBoxLayout) -> None:
        self.preview_area = QWidget()
        self.preview_area.setStyleSheet("background-color: gray;")
        layout.addWidget(self.preview_area)

    def on_double_clicked(self, index: QModelIndex) -> None:
        file_path = self.sequence_loading.model.filePath(index)
        if file_path.endswith(".json"):
            self.load_sequence_from_file(file_path)
        else:
            QMessageBox.information(
                self, "Information", "Selected file is not a JSON sequence file."
            )

    def on_favorite_double_clicked(self, index: QModelIndex) -> None:
        item = self.favorites_manager.favorites_model.itemFromIndex(index)
        file_path = item.data(Qt.ItemDataRole.UserRole)
        self.load_sequence_from_file(file_path)

    def load_sequence_from_file(self, file_path: str) -> None:
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                sequence_data: list[dict[str, str]] = json.load(file)
            self.populate_sequence(sequence_data)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load sequence: {str(e)}")

    def populate_sequence(self, sequence_data: list[dict[str, str]]) -> None:
        if not self.json_handler:
            self._init_references()
        if not sequence_data:
            return
        self.sequence_widget.button_frame.clear_sequence(
            show_indicator=False, should_reset_to_start_pos_picker=False
        )
        start_pos_beat = self.start_pos_manager._convert_current_sequence_json_entry_to_start_pos_pictograph(
            sequence_data
        )
        self.json_handler.set_start_position_data(start_pos_beat)
        self.start_pos_view.set_start_pos_beat(start_pos_beat)
        for pictograph_dict in sequence_data:
            if pictograph_dict.get("sequence_start_position"):
                continue
            self.sequence_widget.populate_sequence(pictograph_dict)
        last_beat = self.sequence_widget.beat_frame.get_last_filled_beat().beat
        self.sequence_builder.current_pictograph = last_beat
        if self.sequence_builder.start_pos_picker.isVisible():
            self.sequence_builder.transition_to_sequence_building()
        self.sequence_builder.option_picker.scroll_area._add_and_display_relevant_pictographs(
            self.sequence_builder.option_picker.option_manager.get_next_options()
        )

    def dragEnterEvent(self, event: "QDragEnterEvent") -> None:
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: "QDropEvent") -> None:
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith(".json"):
                self.add_to_favorites(file_path)

    def add_to_favorites(self, file_path: str) -> None:
        file_name = os.path.basename(file_path)
        item = QStandardItem(file_name)
        item.setData(file_path, Qt.ItemDataRole.UserRole)
        self.favorites_manager.favorites_model.appendRow(item)
        self.favorites_manager.save_favorites()

    def sort_favorites(self, column: int) -> None:
        # Toggle sorting order between ascending and descending
        currentOrder = self.favorites_manager.favorites_model.sortOrder()
        newOrder = (
            Qt.SortOrder.DescendingOrder
            if currentOrder == Qt.SortOrder.AscendingOrder
            else Qt.SortOrder.AscendingOrder
        )
        self.favorites_manager.favorites_model.sort(column, newOrder)
