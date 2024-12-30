from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QSizePolicy, QFrame


if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.graph_editor.graph_editor import GraphEditor


class GraphEditorPlaceholder(QFrame):
    """This frame allows the sequence widget's items to reposition when toggling the graph editor's visibility."""

    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__(graph_editor)
        self.sequence_widget = graph_editor.sequence_widget
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(0) 

    def set_height(self, new_height):
        """Sets the height of the placeholder dynamically."""
        self.setFixedHeight(new_height)
        self.sequence_widget.updateGeometry()
        self.sequence_widget.button_panel.updateGeometry() 

    def resize_graph_editor_placeholder(self):
        """Resizes the placeholder to match the graph editor height."""
        graph_editor_height = (
            self.sequence_widget.graph_editor.get_graph_editor_height()
        )
        self.set_height(graph_editor_height)
