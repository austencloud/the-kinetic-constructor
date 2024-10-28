from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from .graph_editor_layout_manager import GraphEditorLayoutManager
from .graph_editor_state_manager import GraphEditorStateManager
from .graph_editor_toggle_tab import GraphEditorToggleTab
from .graph_editor_animator import GraphEditorAnimator
from .adjustment_panel.beat_adjustment_panel import BeatAdjustmentPanel
from .pictograph_container.GE_pictograph_container import GraphEditorPictographContainer

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class GraphEditor(QFrame):
    pictograph_layout: QVBoxLayout
    adjustment_panel_layout: QVBoxLayout

    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__()
        self.sequence_widget = sequence_widget
        self.main_widget = sequence_widget.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager
        self._setup_components()
        self.layout_manager.setup_layout()

    def _setup_components(self) -> None:
        self.pictograph_container = GraphEditorPictographContainer(self)
        self.adjustment_panel = BeatAdjustmentPanel(self)
        self.toggle_tab = GraphEditorToggleTab(self)
        self.layout_manager = GraphEditorLayoutManager(self)
        self.state = GraphEditorStateManager(self)
        self.animator = GraphEditorAnimator(self)
        self.toggle_tab.toggled.connect(self.animator.animate_toggle)

    def resize_graph_editor(self) -> None:
        if not self.animator.is_animating:
            self.setFixedHeight(int(self.sequence_widget.height() // 3.5))
        self.setMaximumWidth(self.sequence_widget.width())
        self.pictograph_container.resize_GE_pictograph_container()
        self.adjustment_panel.update_adjustment_panel()
        self.adjustment_panel.placeholder_widget.resize_adjustment_panel_placeholder_text()
        self.adjustment_panel.resize_beat_adjustment_panel()

    def resizeEvent(self, event):
        self.resize_graph_editor()
        super().resizeEvent(event)


