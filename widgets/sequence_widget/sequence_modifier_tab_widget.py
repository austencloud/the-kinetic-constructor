from typing import TYPE_CHECKING

from widgets.base_tab_widget import BaseTabWidget
from widgets.graph_editor.graph_editor import GraphEditor

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class SequenceModifier(BaseTabWidget):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget.main_widget)
        self.main_widget = sequence_widget.main_widget
        self.sequence_widget = sequence_widget
        self.graph_editor = GraphEditor(self)
        self.addTab(self.graph_editor, "Graph Editor")

    def resize_sequence_modifier(self):
        self.setMaximumHeight(self.sequence_widget.width() // 2)
        self.graph_editor.resize_graph_editor()
