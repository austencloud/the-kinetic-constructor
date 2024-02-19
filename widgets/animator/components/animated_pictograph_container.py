from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout

from widgets.animator.components.animated_pictograph import AnimatedPictographView



if TYPE_CHECKING:
    from widgets.graph_editor.graph_editor import GraphEditor
    from widgets.graph_editor.components.GE_pictograph import GE_PictographView


class AnimatedPictographContainer(QWidget):
    def __init__(
        self,
        graph_editor: "GraphEditor",
        animated_pictograph_view: "AnimatedPictographView",
    ) -> None:
        super().__init__(graph_editor)
        self.graph_editor = graph_editor
        self.animated_pictograph_view = animated_pictograph_view

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(animated_pictograph_view)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet("border: 1px solid black;")

    def resize_animated_pictograph_container(self):
        self.setMaximumHeight(self.graph_editor.height())
        self.setMaximumWidth(self.graph_editor.height())
        self.animated_pictograph_view.resize_animated_pictograph_view()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
