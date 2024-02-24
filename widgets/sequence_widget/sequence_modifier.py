from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
from widgets.base_tab_widget import BaseTabWidget
from widgets.animator.animator import Animator
from widgets.graph_editor.graph_editor import GraphEditor
from widgets.library.library import Library

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class SequenceModifier(BaseTabWidget):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget.main_widget)
        self.main_widget = sequence_widget.main_widget
        self.sequence_widget = sequence_widget
        self.graph_editor = GraphEditor(self)
        self.animator = Animator(self)
        self.prop_changer = QWidget(self)
        self.library = Library(self)
        self.addTab(self.graph_editor, "Graph Editor")
        self.addTab(self.animator, "Animator")
        self.addTab(self.prop_changer, "Prop Changer")
        self.addTab(self.library, "Library")
        self.currentChanged.connect(self.resize_sequence_modifier)

    def resize_sequence_modifier(self):
        self.setMaximumWidth(self.sequence_widget.beat_frame.width())
        self.graph_editor.resize_graph_editor()
        self.animator.resize_animator()
