from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from main_window.main_widget.sequence_widget.graph_editor.graph_editor import (
        GraphEditor,
    )


class GraphEditorStateManager:
    def __init__(self, graph_editor: "GraphEditor") -> None:
        self.graph_editor = graph_editor
        self.is_graph_editor_visible = (
            self.graph_editor.settings_manager.settings.value(
                "graph_editor_visible", True, type=bool
            )
        )

    def update_graph_editor_visibility(self):
        """Set the initial state of the GraphEditor based on saved settings."""
        if self.is_graph_editor_visible:
            self.graph_editor.setMaximumHeight(
                self.graph_editor.main_widget.height() // 4
            )
        else:
            self.graph_editor.setMaximumHeight(0)
            self.graph_editor.toggle_tab.move(
                self.graph_editor.toggle_tab.pos().x(),
                self.graph_editor.height() - self.graph_editor.toggle_tab.height(),
            )

    def save_graph_editor_state(self):
        """Save the visibility state of the GraphEditor."""
        self.graph_editor.settings_manager.settings.setValue(
            "graph_editor_visible", self.is_graph_editor_visible
        )

    def reset_graph_editor(self) -> None:
        self.graph_editor.pictograph_container.GE_pictograph_view.set_to_blank_grid()
        self.graph_editor.adjustment_panel.update_adjustment_panel()
