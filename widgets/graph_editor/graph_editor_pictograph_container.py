from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout


if TYPE_CHECKING:
    from widgets.graph_editor.graph_editor import GraphEditor
    from widgets.graph_editor.graph_editor_pictograph import GraphEditorPictographView


class GraphEditorPictographContainer(QWidget):
    def __init__(
        self,
        graph_editor: "GraphEditor",
        GE_pictograph_view: "GraphEditorPictographView",
    ) -> None:
        super().__init__(graph_editor)
        self.graph_editor = graph_editor
        self.GE_pictograph_view = GE_pictograph_view

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(GE_pictograph_view)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def resize_GE_pictograph_container(self):
        self.GE_pictograph_view.resize_GE_pictograph_view()
        self.setMaximumHeight(self.GE_pictograph_view.height())
        self.setMaximumWidth(self.GE_pictograph_view.height())
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
