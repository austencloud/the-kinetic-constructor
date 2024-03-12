from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget
from widgets.base_tab_widget import BaseTabWidget
from widgets.animator.animator import Animator
from widgets.graph_editor.graph_editor import GraphEditor

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
        self.addTab(self.graph_editor, "Graph Editor")
        self.addTab(self.animator, "Animator")
        self.addTab(self.prop_changer, "Prop Changer")
        self.currentChanged.connect(self.resize_sequence_modifier)

    def resize_sequence_modifier(self) -> None:
        current_widget = self.currentWidget()
        if current_widget == self.graph_editor:
            if self.sequence_widget.beat_frame.selection_manager.selected_beat:
                self.graph_editor.adjustment_panel.hide_placeholder_widget()
            else:
                self.graph_editor.adjustment_panel.show_placeholder_widget()
            self.graph_editor.resize_graph_editor()
        elif current_widget == self.animator:
            self.animator.resize_animator()
