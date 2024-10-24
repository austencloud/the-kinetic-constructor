# sequence_dictionary_browser.py
from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtCore import Qt, QMimeData, QByteArray
from PyQt6.QtGui import QDrag
import json

if TYPE_CHECKING:
    from .choreography_tab_widget import ChoreographyTabWidget
    from main_window.main_widget.sequence_widget.beat_frame.beat import BeatView


class DraggableSequenceListWidget(QListWidget):
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

