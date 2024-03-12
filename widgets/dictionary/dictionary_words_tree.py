from PyQt6.QtCore import QDir, Qt, QModelIndex
from PyQt6.QtGui import QFont

from typing import TYPE_CHECKING
from widgets.dictionary.dictionary_file_system_model import DictionaryFileSystemModel
from widgets.dictionary.dictionary_sort_proxy_model import (
    DictionarySortProxyModel,
)
from PyQt6.QtWidgets import QTreeView, QVBoxLayout, QHeaderView, QMessageBox

if TYPE_CHECKING:
    from widgets.dictionary.dictionary import Dictionary


class DictionaryWordsTree:
    def __init__(self, dictionary: "Dictionary") -> None:
        self.dictionary = dictionary
        self.model = DictionaryFileSystemModel()
        self.proxy_model = DictionarySortProxyModel(dictionary)
        self.tree_view = QTreeView()

    def setup_ui(self, layout: QVBoxLayout) -> None:
        self.model.setRootPath(QDir.currentPath() + "/dictionary")
        self.proxy_model.setSourceModel(self.model)
        self.tree_view.setModel(self.proxy_model)
        self.proxy_model.lengthSortingEnabled = True
        self.proxy_model.setSortRole(Qt.ItemDataRole.UserRole)
        self.proxy_model.sort(0, Qt.SortOrder.AscendingOrder)

        dictionary_index = self.model.index(QDir.currentPath() + "/dictionary")
        proxy_dictionary_index = self.proxy_model.mapFromSource(dictionary_index)
        self.tree_view.setRootIndex(proxy_dictionary_index)
        self.tree_view.doubleClicked.connect(self.on_double_clicked)
        self.tree_view.setHeaderHidden(False)
        self.tree_view.header().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self._set_font_size()

        layout.addWidget(self.tree_view)
        self.update_sort_order_from_settings()

    def update_sort_order_from_settings(self) -> None:
        sort_criteria = (
            self.dictionary.main_widget.main_window.settings_manager.get_setting(
                "sort_criteria", "Length"
            )
        )

        self.proxy_model.lengthSortingEnabled = sort_criteria == "Length"
        self.proxy_model.invalidate()
        self.proxy_model.sort(0, Qt.SortOrder.AscendingOrder)

    def _set_font_size(self) -> None:
        font_size = int(self.dictionary.width() * 0.02)
        font = QFont("Arial", font_size)
        self.tree_view.setFont(font)
        self.tree_view.setUniformRowHeights(True)
        self.tree_view.setStyleSheet("QTreeView::item { height: 40px; }")

    def on_double_clicked(self, index: QModelIndex) -> None:
        source_index = self.proxy_model.mapToSource(index)
        file_path = self.model.filePath(source_index)

        if file_path.endswith(".json"):
            self.dictionary.sequence_populator.load_sequence_from_file(file_path)
        else:
            QMessageBox.information(
                self, "Information", "Selected file is not a JSON sequence file."
            )

    def resize_dictionary_words_tree(self):
        self._set_font_size()
