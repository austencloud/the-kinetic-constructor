from email.mime import base
import os
from PyQt6.QtCore import QDir, Qt, QModelIndex, QEvent
from PyQt6.QtGui import QFont

from typing import TYPE_CHECKING
from widgets.dictionary.dictionary_file_system_model import DictionaryFileSystemModel
from widgets.dictionary.dictionary_sort_proxy_model import (
    DictionarySortProxyModel,
)
from PyQt6.QtWidgets import (
    QTreeView,
    QVBoxLayout,
    QHeaderView,
    QMessageBox,
    QTreeWidget,
)

if TYPE_CHECKING:
    from widgets.dictionary.dictionary import Dictionary


class DictionaryWordsTree(QTreeView):
    def __init__(self, dictionary: "Dictionary") -> None:
        super().__init__(dictionary)
        self.dictionary = dictionary
        self.model = DictionaryFileSystemModel()
        self.proxy_model = DictionarySortProxyModel(dictionary)

    def setup_ui(self, layout: QVBoxLayout) -> None:
        self.model.setRootPath(QDir.currentPath() + "/dictionary")
        self.proxy_model.setSourceModel(self.model)
        self.setModel(self.proxy_model)
        self.proxy_model.lengthSortingEnabled = True
        self.proxy_model.setSortRole(Qt.ItemDataRole.UserRole)
        self.proxy_model.sort(0, Qt.SortOrder.AscendingOrder)

        dictionary_index = self.model.index(QDir.currentPath() + "/dictionary")
        proxy_dictionary_index = self.proxy_model.mapFromSource(dictionary_index)
        self.setRootIndex(proxy_dictionary_index)
        self.doubleClicked.connect(self.on_double_clicked)
        self.setHeaderHidden(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self._set_font_size()

        self.installEventFilter(self)
        layout.addWidget(self)
        self.update_sort_order_from_settings()

    def eventFilter(self, obj, event) -> bool:
        if obj == self and event.type() == QEvent.Type.KeyPress:
            key_event = event
            if key_event.key() == Qt.Key.Key_Delete:
                self.delete_selected_section()
                return True
        return False

    def delete_selected_section(self) -> None:
        selected_indexes = self.selectedIndexes()
        if len(selected_indexes) > 0:
            selected_index = selected_indexes[0]
            source_index = self.proxy_model.mapToSource(selected_index)
            file_path = self.model.filePath(source_index)
            base_pattern = self.model.fileName(source_index)
            if self.model.isDir(source_index):
                if (
                    QMessageBox.question(
                        self,
                        "Confirmation",
                        f"Are you sure you want to delete all variations of {base_pattern}?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    )
                    == QMessageBox.StandardButton.Yes
                ):
                    if self.model.remove(source_index):
                        pass
                    else:
                        QMessageBox.warning(
                            self, "Warning", "Failed to delete directory."
                        )
            elif file_path.endswith(".json"):
                base_pattern = self.model.fileName(source_index)
                if (
                    QMessageBox.question(
                        self,
                        "Confirmation",
                        f"Are you sure you want to delete this variation?\n{base_pattern}",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    )
                    == QMessageBox.StandardButton.Yes
                ):
                    if self.model.remove(source_index):
                        # dont' do anyhting, just continue
                        pass
                    else:
                        QMessageBox.warning(
                            self, "Warning", "Failed to delete JSON file."
                        )
            else:
                QMessageBox.warning(
                    self,
                    "Warning",
                    "Selected file is not a JSON sequence file.",
                )

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
        self.setFont(font)
        self.setUniformRowHeights(True)
        self.setStyleSheet("QTreeView::item { height: 40px; }")

    def on_double_clicked(self, index: QModelIndex) -> None:
        source_index = self.proxy_model.mapToSource(index)
        file_path = self.model.filePath(source_index)

        if self.model.isDir(source_index):
            if self.isExpanded(index):
                self.collapse(index)
            else:
                self.expand(index)
                # Load the turn patterns for the selected structural variation.
                base_pattern = self.model.fileName(source_index)
                self.dictionary.turn_variation_tree.display_turn_patterns_for_variation(base_pattern, base_pattern)
        elif file_path.endswith(".json"):
            self.dictionary.sequence_populator.load_sequence_from_file(file_path)
            # Assuming the filename without the extension is the structural variation name.
            structural_variation_name = os.path.splitext(self.model.fileName(source_index))[0]
            base_pattern = structural_variation_name.split('_')[0]
            # Display the turn patterns related to the selected structural variation.
            self.dictionary.turn_variation_tree.display_turn_patterns_for_variation(base_pattern, structural_variation_name)
        else:
            QMessageBox.information(
                self,
                "Information",
                "Selected file is not a JSON sequence file.",
            )

    def resize_dictionary_words_tree(self):
        self._set_font_size()
