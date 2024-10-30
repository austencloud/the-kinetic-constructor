from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint, QPropertyAnimation, QEasingCurve, QRect
from .graph_editor_layout_manager import GraphEditorLayoutManager
from .graph_editor_state_manager import GraphEditorStateManager
from .graph_editor_toggle_tab import GraphEditorToggleTab
from .graph_editor_animator import GraphEditorAnimator
from .adjustment_panel.beat_adjustment_panel import BeatAdjustmentPanel
from .pictograph_container.GE_pictograph_container import GraphEditorPictographContainer

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


# graph_editor.py

from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSizePolicy

if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class GraphEditor(QFrame):
    pictograph_layout: QVBoxLayout
    adjustment_panel_layout: QVBoxLayout

    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__(sequence_widget)
        self.sequence_widget = sequence_widget
        self.main_widget = sequence_widget.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager

        # Set size policies
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.setMinimumHeight(0)  # Allow to shrink to zero height
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self._setup_components()
        self.layout_manager.setup_layout()
        self.hide()

    def _setup_components(self) -> None:
        self.pictograph_container = GraphEditorPictographContainer(self)
        self.adjustment_panel = BeatAdjustmentPanel(self)
        # self.toggle_tab = GraphEditorToggleTab(self)
        self.layout_manager = GraphEditorLayoutManager(self)
        self.state = GraphEditorStateManager(self)
        # self.sequence_widget.toggle_tab.toggled.connect(self.toggle_graph_editor)

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
        self.setFixedSize(self.sequence_widget.width(), graph_editor_height)

        if self.sequence_widget.graph_editor.isVisible():
            self.sequence_widget.layout_manager.graph_editor_placeholder.resize_graph_editor_placeholder()

        self.pictograph_container.resize_GE_pictograph_container()
        self.adjustment_panel.update_adjustment_panel()
        self.adjustment_panel.resize_beat_adjustment_panel()
        self.raise_()

    def get_graph_editor_height(self):
        return int(self.sequence_widget.height() // 3.5)

    def resizeEvent(self, event):
        self.resize_graph_editor()
        super().resizeEvent(event)
