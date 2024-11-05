from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QSpacerItem, QSizePolicy, QApplication, QFrame

if TYPE_CHECKING:
    from .sequence_widget import SequenceWidget


class GraphEditorPlaceholder(QFrame):
    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.setFixedHeight(0)  # Start with a height of 0

    def set_height(self, new_height):
        """Sets the height of the placeholder dynamically."""
        self.setFixedHeight(new_height)
        self.sequence_widget.updateGeometry()
        self.sequence_widget.button_panel.updateGeometry()  # Update layout to reflect the height change
        # QApplication.processEvents()  # Process events to update layout immediately

    def resize_graph_editor_placeholder(self):
        """Resizes the placeholder to match the graph editor height."""
        graph_editor_height = (
            self.sequence_widget.graph_editor.get_graph_editor_height()
        )
        self.set_height(graph_editor_height)
