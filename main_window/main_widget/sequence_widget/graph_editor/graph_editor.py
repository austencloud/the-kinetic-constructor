from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout

from main_window.main_widget.sequence_widget.graph_editor.graph_editor_toggle_tab import (
    GraphEditorToggleTab,
)
from main_window.main_widget.sequence_widget.graph_editor_animator import (
    GraphEditorAnimator,
)

from .adjustment_panel.beat_adjustment_panel import BeatAdjustmentPanel
from .pictograph_container.GE_pictograph_container import GraphEditorPictographContainer


if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.sequence_widget import SequenceWidget


class GraphEditor(QFrame):
    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__()
        self.sequence_widget = sequence_widget
        self.main_widget = sequence_widget.main_widget
        self.settings_manager = self.main_widget.main_window.settings_manager
        self.is_graph_editor_visible = self.settings_manager.settings.value(
            "graph_editor_visible", True, type=bool
        )
        self._setup_components()
        self._setup_layout()

    def _setup_components(self) -> None:
        self.pictograph_container = GraphEditorPictographContainer(self)
        self.adjustment_panel = BeatAdjustmentPanel(self)
        self.toggle_tab = GraphEditorToggleTab(self)
        self.toggle_tab.toggled.connect(self.toggle_graph_editor)
        self.animator = GraphEditorAnimator(self)

    def _setup_layout(self) -> None:
        self.pictograph_layout = self._setup_pictograph_layout()
        self.adjustment_panel_layout = self._setup_adjustment_panel_layout()

        layout: QHBoxLayout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(self.pictograph_layout)
        layout.addLayout(self.adjustment_panel_layout)

    def _setup_pictograph_layout(self) -> None:
        pictograph_layout = QVBoxLayout()
        pictograph_layout.addWidget(self.pictograph_container)
        pictograph_layout.setContentsMargins(0, 0, 0, 0)
        pictograph_layout.setSpacing(0)
        pictograph_layout.setStretch(1, 1)
        return pictograph_layout

    def _setup_adjustment_panel_layout(self) -> None:
        adjustment_panel_layout = QVBoxLayout()
        adjustment_panel_layout.addWidget(self.adjustment_panel)
        adjustment_panel_layout.setContentsMargins(0, 0, 0, 0)
        adjustment_panel_layout.setSpacing(0)
        return adjustment_panel_layout

    def toggle_graph_editor(self):
        """Animate the opening or closing of the GraphEditor and toggle tab."""
        self.animator.animate_toggle()

    def update_graph_editor_visibility(self):
        """Set the initial state of the GraphEditor based on saved settings."""
        if self.is_graph_editor_visible:
            self.setMaximumHeight(self.main_widget.height() // 4)
        else:
            self.setMaximumHeight(0)
            self.toggle_tab.move(
                self.toggle_tab.pos().x(), self.height() - self.toggle_tab.height()
            )

    def save_graph_editor_state(self):
        """Save the visibility state of the GraphEditor."""
        self.settings_manager.settings.setValue(
            "graph_editor_visible", self.is_graph_editor_visible
        )

    def clear_graph_editor(self) -> None:
        self.pictograph_container.GE_pictograph_view.set_to_blank_grid()
        self.adjustment_panel.update_adjustment_panel()

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
