from PyQt6.QtWidgets import QGraphicsScene
from typing import TYPE_CHECKING

from widgets.graph_editor_tab.object_panel.base_objectbox.base_objectbox_view import BaseObjectBoxView

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor_tab.graph_editor_frame import GraphEditorFrame


class BaseObjectBox(QGraphicsScene):
    def __init__(
        self, main_widget: "MainWidget", graph_editor: "GraphEditorFrame"
    ) -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.pictograph = graph_editor.main_pictograph
        self.setSceneRect(0, 0, 950, 950)
        self.view: BaseObjectBoxView = None
