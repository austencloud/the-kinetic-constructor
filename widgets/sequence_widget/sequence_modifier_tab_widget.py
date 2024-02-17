from PyQt6.QtWidgets import QTabWidget
from typing import TYPE_CHECKING

from widgets.base_tab_widget import BaseTabWidget
from widgets.graph_editor_tab.graph_editor_frame import GraphEditor

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class SequenceModifierTabWidget(BaseTabWidget):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget.main_widget)
        self.sequence_widget = sequence_widget
        self.graph_editor = GraphEditor(sequence_widget.main_widget)
        self.addTab(self.graph_editor, "Graph Editor")
