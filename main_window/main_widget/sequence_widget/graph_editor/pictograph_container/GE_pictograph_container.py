from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from ..GE_pictograph_view import GE_PictographView, GE_BlankPictograph

if TYPE_CHECKING:
    from base_widgets.base_pictograph.base_pictograph import BasePictograph
    from ..graph_editor import GraphEditor

# pictograph_container.py


class GraphEditorPictographContainer(QWidget):
    def __init__(self, graph_editor: "GraphEditor") -> None:
        super().__init__(graph_editor)
        self.graph_editor = graph_editor

        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.setMinimumHeight(0)
        self.setup_pictograph()

        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.addWidget(self.GE_pictograph_view)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # self.layout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)

    def setup_pictograph(self):
        self.GE_pictograph = GE_BlankPictograph(self)
        self.GE_pictograph_view = GE_PictographView(self, self.GE_pictograph)

    def update_GE_pictograph(self, pictograph: "BasePictograph") -> None:
        self.GE_pictograph_view.set_scene(pictograph)
        self.GE_pictograph = pictograph

    def resize_GE_pictograph_container(self):
        size = self.graph_editor.height()
        self.setFixedWidth(size)
        self.setFixedHeight(size)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.GE_pictograph_view.resize_GE_pictograph_view()
