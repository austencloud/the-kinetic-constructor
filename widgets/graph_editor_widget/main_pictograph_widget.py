from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout

if TYPE_CHECKING:
    from widgets.graph_editor_widget.graph_editor import GraphEditor
    from widgets.graph_editor_widget.main_pictograph_view import MainPictographView


class MainPictographWidget(QWidget):
    def __init__(
        self,
        graph_editor: "GraphEditor",
        main_pictograph_view: "MainPictographView",
    ) -> None:
        super().__init__(graph_editor)
        self.graph_editor = graph_editor
        self.main_pictograph_view = main_pictograph_view

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(main_pictograph_view)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def showEvent(self, event) -> None:
        self.setMinimumWidth(self.main_pictograph_view.width())
        self.setMaximumWidth(self.main_pictograph_view.width())

        self.setMinimumHeight(self.main_pictograph_view.height())
        self.setMaximumHeight(self.main_pictograph_view.height())
