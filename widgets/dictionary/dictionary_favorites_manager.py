import os
from PyQt6.QtCore import Qt
import json
from typing import TYPE_CHECKING

from PyQt6.QtWidgets import (
    QTreeView,
    QVBoxLayout,
    QHeaderView,
)
from PyQt6.QtGui import (
    QStandardItemModel,
    QStandardItem,
)

if TYPE_CHECKING:
    from widgets.dictionary.dictionary import Dictionary


class DictionaryFavoritesTree:
    def __init__(self, dictionary: "Dictionary") -> None:
        self.dictionary = dictionary
        self.favorites_model = QStandardItemModel()
        self.favorites_view = QTreeView()
        self.favorites_file = "favorites.json"

    def setup_ui(self, layout: QVBoxLayout) -> None:
        self.favorites_view.setModel(self.favorites_model)
        self.favorites_view.setHeaderHidden(False)
        self.favorites_view.header().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.favorites_view.doubleClicked.connect(
            self.dictionary.on_favorite_double_clicked
        )
        self.favorites_view.setAcceptDrops(True)
        self.favorites_view.setDragEnabled(True)
        self.favorites_view.setDragDropMode(QTreeView.DragDropMode.DropOnly)
        self.favorites_view.setSelectionMode(QTreeView.SelectionMode.ExtendedSelection)
        self.favorites_view.setSelectionBehavior(QTreeView.SelectionBehavior.SelectRows)
        self.favorites_view.setDropIndicatorShown(True)
        self.favorites_view.setRootIsDecorated(False)
        self.favorites_view.header().sectionClicked.connect(
            self.dictionary.sort_favorites
        )
        layout.addWidget(self.favorites_view)

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
