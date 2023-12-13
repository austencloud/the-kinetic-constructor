from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtGui import QResizeEvent

if TYPE_CHECKING:
    from widgets.graph_editor.graph_editor import GraphEditor
    from widgets.graph_editor.pictograph.pictograph_view import PictographView


class PictographWidget(QWidget):
    def __init__(
        self, graph_editor: "GraphEditor", view: "PictographView", aspect_ratio
    ) -> None:
        super().__init__(graph_editor)
        self.aspect_ratio = aspect_ratio
        self.graph_editor = graph_editor
        self.view = view
        
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(view)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def resize_pictograph_widget(self) -> None:
        new_width = int(self.graph_editor.height() * 75 / 90)
        self.setMaximumHeight(self.graph_editor.height())
        self.setMinimumWidth(new_width)
        self.setMaximumWidth(new_width)
        self.view.configure_button_size_and_position(int(self.width() / 10))
        self.view_scale = min(
            self.width() / self.graph_editor.pictograph.sceneRect().width(),
            self.height() / self.graph_editor.pictograph.sceneRect().height(),
        )
        self.view.resetTransform()
        self.view.scale(
            self.view_scale,
            self.view_scale,
        )
