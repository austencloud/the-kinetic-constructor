from PyQt6.QtWidgets import QGraphicsView, QFrame
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.graph_editor_tab.graph_editor_object_panel.base_objectbox.base_objectbox import (
        BaseObjectBox,
    )
    from widgets.graph_editor_tab.graph_editor_frame import GraphEditorFrame


class BaseObjectBoxView(QGraphicsView):
    def __init__(
        self, BaseObjectBox: "BaseObjectBox", graph_editor: "GraphEditorFrame"
    ) -> None:
        super().__init__()
        self.graph_editor = graph_editor
        self.setScene(BaseObjectBox)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.BaseObjectBox = BaseObjectBox

        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Plain)
        self.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

    def resizeEvent(self, event) -> None:
        # super().resizeEvent(event)
        self.setMinimumWidth(int(self.graph_editor.main_pictograph.view.height() / 2))
        self.setMaximumWidth(int(self.graph_editor.main_pictograph.view.height() / 2))

        self.setMinimumHeight(int(self.graph_editor.main_pictograph.view.height() / 2))
        self.setMaximumHeight(int(self.graph_editor.main_pictograph.view.height() / 2))

        if self.scene():
            self.fitInView(self.sceneRect(), Qt.AspectRatioMode.KeepAspectRatio)
