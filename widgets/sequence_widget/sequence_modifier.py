from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QTabWidget, QSizePolicy
from styles.get_tab_stylesheet import get_tab_stylesheet
from widgets.graph_editor.graph_editor import GraphEditor

if TYPE_CHECKING:
    from widgets.sequence_widget.sequence_widget import SequenceWidget


class SequenceModifier(QTabWidget):
    def __init__(self, sequence_widget: "SequenceWidget"):
        super().__init__(sequence_widget)
        self.main_widget = sequence_widget.main_widget
        self.sequence_widget = sequence_widget
        self.graph_editor = GraphEditor(self)
        self.addTab(self.graph_editor, "Graph Editor")
        self.setStyleSheet(get_tab_stylesheet())
        size_policy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.setSizePolicy(size_policy)

    def resize_sequence_modifier(self) -> None:
        if self.sequence_widget.beat_frame.selection_manager.selected_beat:
            self.graph_editor.adjustment_panel.hide_placeholder_widget()
        else:
            self.graph_editor.adjustment_panel.show_placeholder_widget()

        self.graph_editor.resize_graph_editor()
        self.graph_editor.adjustment_panel.update_adjustment_panel()
