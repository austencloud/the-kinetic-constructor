from typing import TYPE_CHECKING
from PyQt6.QtGui import QResizeEvent

from widgets.graph_editor.graph_editor import GraphEditor

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QSizePolicy



class GraphEditorWidget(QFrame):
    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.main_layout = QHBoxLayout(self)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.graph_editor = GraphEditor(self.main_widget, self)

        self.main_layout.addWidget(self.graph_editor)
        # Ensure the graph editor does not expand in height beyond what's necessary
        self.graph_editor.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.graph_editor.setMaximumHeight(self.graph_editor.preferred_height())


        self.setLayout(self.main_layout)

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.graph_editor.resize_graph_editor()
