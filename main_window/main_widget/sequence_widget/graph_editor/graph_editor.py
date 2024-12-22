from typing import TYPE_CHECKING
from PyQt6.QtWidgets import (
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QSizePolicy,
    QStackedLayout,
)
from PyQt6.QtCore import Qt

from main_window.main_widget.sequence_widget.graph_editor.arrow_selection_manager import (
    ArrowSelectionManager,
)

from .graph_editor_layout_manager import GraphEditorLayoutManager
from .graph_editor_state_manager import GraphEditorStateManager
from .adjustment_panel.beat_adjustment_panel import BeatAdjustmentPanel
from .pictograph_container.GE_pictograph_container import GraphEditorPictographContainer

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class GraphEditor(QFrame):
    main_layout: QHBoxLayout
    pictograph_layout: QVBoxLayout
    adjustment_panel_layout: QVBoxLayout
    left_stack: QStackedLayout
    right_stack: QStackedLayout

    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.main_widget = sequence_widget.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setMinimumHeight(0)  # Allow to shrink to zero height
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self._setup_components()
        self.layout_manager.setup_layout()
        self.hide()

    def _setup_components(self) -> None:
        self.arrow_selection_manager = ArrowSelectionManager(self)
        self.pictograph_container = GraphEditorPictographContainer(self)
        self.adjustment_panel = BeatAdjustmentPanel(self)
        self.layout_manager = GraphEditorLayoutManager(self)
        self.state = GraphEditorStateManager(self)

        self.pictograph_container.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.pictograph_container.setMinimumHeight(0)

        self.adjustment_panel.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )
        self.adjustment_panel.setMinimumHeight(0)

    def resize_graph_editor(self) -> None:
        graph_editor_height = self.get_graph_editor_height()
        width = self.sequence_widget.width()

        self.setFixedSize(width, graph_editor_height)

        if self.sequence_widget.graph_editor.isVisible():
            self.sequence_widget.layout_manager.graph_editor_placeholder.resize_graph_editor_placeholder()

        self.adjustment_panel.update_adjustment_panel()
        self.raise_()

    def get_graph_editor_height(self):
        return int(self.sequence_widget.height() // 3.5)
