from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout

if TYPE_CHECKING:
    from widgets.graph_editor_tab.graph_editor_frame import GraphEditorFrame
    from widgets.graph_editor_tab.graph_editor_pictograph_view import (
        GraphEditorPictographView,
    )


class GraphEditorPictographWidget(QWidget):
    def __init__(
        self,
        graph_editor: "GraphEditorFrame",
        main_pictograph_view: "GraphEditorPictographView",
    ) -> None:
        super().__init__(graph_editor)
        self.graph_editor = graph_editor
        self.main_pictograph_view = main_pictograph_view

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(main_pictograph_view)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def showEvent(self, event) -> None:
        super().showEvent(event)
        self.setMinimumWidth(self.main_pictograph_view.width())
        self.setMaximumWidth(self.main_pictograph_view.width())

        self.setMinimumHeight(self.main_pictograph_view.height())
        self.setMaximumHeight(self.main_pictograph_view.height())
