from PyQt6.QtCore import QDir
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING
from widgets.library.custom_file_system_model import CustomFileSystemModel
from widgets.library.custom_sort_proxy_model import CustomSortProxyModel

from PyQt6.QtWidgets import (
    QTreeView,
    QVBoxLayout,
    QHeaderView,
)

if TYPE_CHECKING:
    from widgets.library.library import Library


class LibraryWordsTree:
    def __init__(self, library: "Library") -> None:
        self.library = library
        self.model = CustomFileSystemModel()
        self.proxy_model = CustomSortProxyModel()
        self.tree_view = QTreeView()

    def setup_ui(self, layout: QVBoxLayout) -> None:
        self.model.setRootPath(QDir.currentPath() + "/library")
        self.proxy_model.setSourceModel(self.model)
        self.tree_view.setModel(self.proxy_model)
        library_index = self.model.index(QDir.currentPath() + "/library")
        proxy_library_index = self.proxy_model.mapFromSource(library_index)
        self.tree_view.setRootIndex(proxy_library_index)
        self.tree_view.doubleClicked.connect(self.library.on_double_clicked)
        self.tree_view.setHeaderHidden(False)
        self.tree_view.header().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self._set_font_size()

        layout.addWidget(self.tree_view)

    def _set_font_size(self) -> None:
        font_size = int(self.library.width() * 0.02)
        font = QFont("Arial", font_size)
        self.tree_view.setFont(font)
        self.tree_view.setUniformRowHeights(True)
        self.tree_view.setStyleSheet("QTreeView::item { height: 40px; }")

    def resize_library_words_tree(self):
        self._set_font_size()
