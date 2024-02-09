from typing import Union, TYPE_CHECKING
from PyQt6.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt

from widgets.pictograph.pictograph import Pictograph

if TYPE_CHECKING:
    from widgets.codex.codex import Codex
    from widgets.sequence_builder.sequence_builder import SequenceBuilder


class BasePictographScrollArea(QScrollArea):
    def __init__(self, parent: Union["SequenceBuilder", "Codex"]) -> None:
        super().__init__(parent)
        self.container = QWidget()
        self.main_widget = parent.main_widget
        self.container_layout = None
        self.setWidgetResizable(True)
        self.setup_ui()

    def setup_ui(self):
        self.container.setStyleSheet("background-color: #f2f2f2;")
        self.setWidget(self.container)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def set_layout(self, layout_type: str):
        self.clear_layout()

        if layout_type == "VBox":
            self.container_layout: QVBoxLayout = QVBoxLayout(self.container)
        elif layout_type == "HBox":
            self.container_layout: QHBoxLayout = QHBoxLayout(self.container)
        else:
            raise ValueError("Invalid layout type specified.")

        self.container_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container.setLayout(self.container_layout)

    def clear_layout(self):
        if self.container_layout:
            while self.container_layout.count():
                child = self.container_layout.takeAt(0)
                if child.widget():
                    child.widget().hide()

    def add_widget_to_layout(self, widget: QWidget, position: int = None):
        if position is not None: # item is a section
            self.container_layout.insertWidget(position, widget)
        else:  # item is a start pos pictograph
            self.container_layout.addWidget(widget)
