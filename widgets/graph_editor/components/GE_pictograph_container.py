from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout


if TYPE_CHECKING:
    from widgets.graph_editor.graph_editor import GraphEditor
    from widgets.graph_editor.components.GE_pictograph import GE_PictographView


class GE_PictographContainer(QWidget):
    def __init__(
        self,
        graph_editor: "GraphEditor",
        GE_pictograph_view: "GE_PictographView",
    ) -> None:
        super().__init__(graph_editor)
        self.graph_editor = graph_editor
        self.GE_pictograph_view = GE_pictograph_view

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(GE_pictograph_view)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("border: 1px solid black;")

    def resize_GE_pictograph_container(self):
        self.setMaximumHeight(self.graph_editor.height())
        self.setMaximumWidth(self.graph_editor.height())
        self.GE_pictograph_view.resize_GE_pictograph_view()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
