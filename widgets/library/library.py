import os
from PyQt6.QtWidgets import (
    QTreeView,
    QVBoxLayout,
    QWidget,
    QMessageBox,
    QLineEdit,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QHeaderView,
)
from PyQt6.QtGui import (
    QFileSystemModel,
    QStandardItemModel,
    QStandardItem,
    QDragEnterEvent,
    QDropEvent,
)
from PyQt6.QtCore import QDir, QModelIndex, Qt, QItemSelectionModel
import json
from typing import TYPE_CHECKING

from widgets.library.custom_file_system_model import CustomFileSystemModel

if TYPE_CHECKING:
    from widgets.main_widget.main_widget import MainWidget


class Library(QWidget):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__(main_widget)
        self.main_widget = main_widget
        self.favorites_file = "favorites.json"
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        self.setup_search_bar(layout)
        self.setup_tree_views(layout)
        self.setup_preview_area(layout)
        self.setLayout(layout)

    def setup_search_bar(self, layout: QVBoxLayout) -> None:
        search_layout = QHBoxLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search sequences...")
        self.search_bar.textChanged.connect(self.filter_sequences)
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_bar)

        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Name", "Start Position", "Difficulty"])
        self.sort_combo.currentTextChanged.connect(self.sort_sequences)
        search_layout.addWidget(QLabel("Sort by:"))
        search_layout.addWidget(self.sort_combo)

        layout.addLayout(search_layout)

    def setup_tree_views(self, layout: QVBoxLayout) -> None:
        tree_layout = QHBoxLayout()

        # Favorites view setup
        self.favorites_model = QStandardItemModel()
        self.favorites_view = QTreeView()
        self.favorites_view.setModel(self.favorites_model)
        self.favorites_view.setHeaderHidden(False)
        self.favorites_view.header().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.favorites_view.doubleClicked.connect(self.on_favorite_double_clicked)
        self.favorites_view.setAcceptDrops(True)
        self.favorites_view.setDragEnabled(True)
        self.favorites_view.setDragDropMode(QTreeView.DragDropMode.DropOnly)
        self.favorites_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)
        self.favorites_view.setSelectionBehavior(QTreeView.SelectionBehavior.SelectRows)
        self.favorites_view.setDropIndicatorShown(True)
        self.favorites_view.setRootIsDecorated(False)
        self.favorites_view.header().sectionClicked.connect(self.sort_favorites)

        # File system view setup
        self.model = CustomFileSystemModel()
        self.model.setRootPath(QDir.currentPath() + "/library")
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.model)
        self.tree_view.setRootIndex(self.model.index(QDir.currentPath() + "/library"))
        self.tree_view.doubleClicked.connect(self.on_double_clicked)
        self.tree_view.setHeaderHidden(False)
        self.tree_view.header().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        tree_layout.addWidget(self.tree_view)
        tree_layout.addWidget(self.favorites_view)

        layout.addLayout(tree_layout)

    def sort_favorites(self, column: int) -> None:
        # Toggle sorting order between ascending and descending
        currentOrder = self.favorites_model.sortOrder()
        newOrder = (
            Qt.SortOrder.DescendingOrder
            if currentOrder == Qt.SortOrder.AscendingOrder
            else Qt.SortOrder.AscendingOrder
        )
        self.favorites_model.sort(column, newOrder)

    def setup_preview_area(self, layout: QVBoxLayout) -> None:
        self.preview_area = QWidget()
        self.preview_area.setStyleSheet("background-color: gray;")
        layout.addWidget(self.preview_area)

    def on_double_clicked(self, index: QModelIndex) -> None:
        file_path = self.model.filePath(index)
        if file_path.endswith(".json"):
            self.load_sequence_from_file(file_path)
        else:
            QMessageBox.information(
                self, "Information", "Selected file is not a JSON sequence file."
            )

    def on_favorite_double_clicked(self, index: QModelIndex) -> None:
        item = self.favorites_model.itemFromIndex(index)
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
        if not sequence_data:
            return
        json_handler = self.main_widget.json_manager.current_sequence_json_handler
        start_pos_view = self.main_widget.sequence_widget.beat_frame.start_pos_view
        start_pos_manager = (
            self.main_widget.main_tab_widget.sequence_builder.start_pos_picker.start_pos_manager
        )
        sequence_widget = self.main_widget.sequence_widget
        sequence_widget.button_frame.clear_sequence(
            show_indicator=False, should_reset_to_start_pos_picker=False
        )

        start_pos_beat = start_pos_manager._convert_current_sequence_json_entry_to_start_pos_pictograph(
            sequence_data
        )
        json_handler.set_start_position_data(start_pos_beat)
        start_pos_view.set_start_pos_beat(start_pos_beat)

        for pictograph_dict in sequence_data:
            if pictograph_dict.get("sequence_start_position"):
                continue
            sequence_widget.populate_sequence(pictograph_dict)

        sequence_builder = self.main_widget.main_tab_widget.sequence_builder
        last_beat = sequence_widget.beat_frame.get_last_filled_beat().beat
        sequence_builder.current_pictograph = last_beat

        if sequence_builder.start_pos_picker.isVisible():
            sequence_builder.transition_to_sequence_building()

        sequence_builder.option_picker.scroll_area._add_and_display_relevant_pictographs(
            sequence_builder.option_picker.option_manager.get_next_options()
        )

    def filter_sequences(self, text: str) -> None:
        # Implement the filtering logic based on the search text
        # You can use the QFileSystemModel's setNameFilters() and setNameFilterDisables() methods
        # to filter the displayed files based on the search criteria
        pass

    def sort_sequences(self, criteria: str) -> None:
        # Implement the sorting logic based on the selected criteria
        # You can use the QFileSystemModel's sort() method to sort the displayed files
        pass

    def load_favorites(self) -> None:
        if os.path.exists(self.favorites_file):
            with open(self.favorites_file, "r") as file:
                favorites = json.load(file)
                for favorite in favorites:
                    item = QStandardItem(favorite["name"])
                    item.setData(favorite["path"], Qt.ItemDataRole.UserRole)
                    self.favorites_model.appendRow(item)

    def save_favorites(self) -> None:
        favorites = []
        for row in range(self.favorites_model.rowCount()):
            item = self.favorites_model.item(row)
            favorite = {
                "name": item.text(),
                "path": item.data(Qt.ItemDataRole.UserRole),
            }
            favorites.append(favorite)
        with open(self.favorites_file, "w") as file:
            json.dump(favorites, file)

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
        self.favorites_model.appendRow(item)
        self.save_favorites()
