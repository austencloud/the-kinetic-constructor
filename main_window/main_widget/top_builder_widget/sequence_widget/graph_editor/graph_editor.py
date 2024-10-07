from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout
from .adjustment_panel.beat_adjustment_panel import BeatAdjustmentPanel
from .pictograph_container.GE_pictograph_container import GraphEditorPictographContainer


if TYPE_CHECKING:
    from main_window.main_widget.top_builder_widget.sequence_widget.sequence_widget import (
        SequenceWidget,
    )


class GraphEditor(QFrame):
    def __init__(self, sequence_widget: "SequenceWidget") -> None:
        super().__init__()
        self.sequence_widget = sequence_widget
        self.main_widget = sequence_widget.main_widget
        self._setup_components()
        self._setup_layout()

    def _setup_components(self) -> None:
        self.pictograph_container = GraphEditorPictographContainer(self)
        self.adjustment_panel = BeatAdjustmentPanel(self)

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

    def clear_graph_editor(self) -> None:
        self.pictograph_container.GE_pictograph_view.set_to_blank_grid()
        self.adjustment_panel.update_adjustment_panel()

    def resize_graph_editor(self) -> None:
        self.setFixedHeight(int(self.sequence_widget.height() // 3.5))
        self.pictograph_container.resize_GE_pictograph_container()
        self.adjustment_panel.update_adjustment_panel()
        self.adjustment_panel.placeholder_widget.resize_adjustment_panel_placeholder_text()
        self.adjustment_panel.resize_beat_adjustment_panel()

    def resizeEvent(self, event) -> None:
        self.resize_graph_editor()
        super().resizeEvent(event)
