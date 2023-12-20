from PyQt6.QtWidgets import QGraphicsScene
from widgets.graph_editor_tab.object_panel.objectbox_view import ObjectBoxView
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor_tab.graph_editor import GraphEditor


class ObjectBox(QGraphicsScene):
    def __init__(self, main_widget: "MainWidget", graph_editor: "GraphEditor") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.pictograph = graph_editor.main_pictograph
        self.setSceneRect(0, 0, 750, 750)
        self.view: ObjectBoxView = None
