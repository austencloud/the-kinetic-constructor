# sequence_dictionary_browser.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QListWidget
from PyQt6.QtCore import Qt, QMimeData, QByteArray
from PyQt6.QtGui import QDrag
import json

if TYPE_CHECKING:
    pass


class DraggableSequence(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)

    def startDrag(self, supportedActions):
        item = self.currentItem()
        if item:
            sequence = item.data(Qt.ItemDataRole.UserRole)
            mime_data = QMimeData()
            mime_data.setData(
                "application/x-sequence",
                QByteArray(json.dumps(sequence).encode("utf-8")),
            )
            drag = QDrag(self)
            drag.setMimeData(mime_data)
            drag.exec(Qt.DropAction.CopyAction)
