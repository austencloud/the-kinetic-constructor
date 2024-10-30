from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout, QStackedWidget, QStackedLayout


if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.graph_editor.graph_editor import (
        GraphEditor,
    )


class GraphEditorLayoutManager:
    def __init__(self, graph_editor: "GraphEditor") -> None:
        self.graph_editor = graph_editor
        self.sequence_widget = graph_editor.sequence_widget

    def setup_layout(self) -> None:
        self._setup_main_layout()
        self.graph_editor.pictograph_layout = self._setup_pictograph_layout()
        self.graph_editor.adjustment_panel_layout = (
            self._setup_adjustment_panel_layout()
        )
        self._setup_stacks()

        self.graph_editor.main_layout.addLayout(self.graph_editor.left_stack)
        self.graph_editor.main_layout.addLayout(self.graph_editor.pictograph_layout)
        self.graph_editor.main_layout.addLayout(self.graph_editor.right_stack)

    def _setup_main_layout(self):
        self.graph_editor.main_layout = QHBoxLayout(self.graph_editor)
        self.graph_editor.main_layout.setSpacing(0)
        self.graph_editor.main_layout.setContentsMargins(0, 0, 0, 0)

    def _setup_stacks(self):
        self.graph_editor.left_stack = QStackedLayout()
        self.graph_editor.left_stack.addWidget(
            self.graph_editor.adjustment_panel.blue_ori_picker
        )
        self.graph_editor.left_stack.addWidget(
            self.graph_editor.adjustment_panel.blue_turns_box
        )

        self.graph_editor.right_stack = QStackedLayout()
        self.graph_editor.right_stack.addWidget(
            self.graph_editor.adjustment_panel.red_ori_picker
        )
        self.graph_editor.right_stack.addWidget(
            self.graph_editor.adjustment_panel.red_turns_box
        )

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
