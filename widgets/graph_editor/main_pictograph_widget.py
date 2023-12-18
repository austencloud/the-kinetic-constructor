from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout

if TYPE_CHECKING:
    from widgets.graph_editor.graph_editor import GraphEditor
    from widgets.graph_editor.main_pictograph_view import MainPictographView


class MainPictographWidget(QWidget):
    def __init__(
        self, graph_editor: "GraphEditor", main_pictograph_view: "MainPictographView", aspect_ratio
    ) -> None:
        super().__init__(graph_editor)
        self.aspect_ratio = aspect_ratio
        self.graph_editor = graph_editor
        self.main_pictograph_view = main_pictograph_view

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(main_pictograph_view)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def resizeEvent(self, event) -> None:

        self.view_scale = min(
            self.width() / self.graph_editor.main_pictograph.sceneRect().width(),
            self.height() / self.graph_editor.main_pictograph.sceneRect().height(),
        )
        self.main_pictograph_view.resetTransform()
        self.main_pictograph_view.scale(
            self.view_scale,
            self.view_scale,
        )
        self.main_pictograph_view.configure_button_size_and_position(int(self.width() / 10))

    def calculate_preferred_height(self) -> int:
        return int(self.main_pictograph_view.height() * self.aspect_ratio)  
