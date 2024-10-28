from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout




if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.graph_editor.graph_editor import GraphEditor


class GraphEditorLayoutManager:
    def __init__(self, graph_editor: "GraphEditor") -> None:
        self.graph_editor = graph_editor
        self.sequence_widget = graph_editor.sequence_widget

    def setup_layout(self) -> None:
        self.graph_editor.pictograph_layout = self._setup_pictograph_layout()
        self.graph_editor.adjustment_panel_layout = (
            self._setup_adjustment_panel_layout()
        )

        layout: QHBoxLayout = QHBoxLayout(self.graph_editor)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(self.graph_editor.pictograph_layout)
        layout.addLayout(self.graph_editor.adjustment_panel_layout)

    def _setup_pictograph_layout(self) -> None:
        pictograph_layout = QVBoxLayout()
        pictograph_layout.addWidget(self.graph_editor.pictograph_container)
        pictograph_layout.setContentsMargins(0, 0, 0, 0)
        pictograph_layout.setSpacing(0)
        pictograph_layout.setStretch(1, 1)
        return pictograph_layout

    def _setup_adjustment_panel_layout(self) -> None:
        adjustment_panel_layout = QVBoxLayout()
        adjustment_panel_layout.addWidget(self.graph_editor.adjustment_panel)
        adjustment_panel_layout.setContentsMargins(0, 0, 0, 0)
        adjustment_panel_layout.setSpacing(0)
        return adjustment_panel_layout



