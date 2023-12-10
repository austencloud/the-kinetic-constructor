from PyQt6.QtWidgets import QGraphicsScene
from widgets.graph_editor.object_panel.objectbox_view import ObjectBoxView
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from widgets.graph_editor.graph_editor import GraphEditor


class ObjectBox(QGraphicsScene):
    def __init__(self, main_widget: "MainWidget", graph_editor: "GraphEditor") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.pictograph = graph_editor.pictograph
        self.setSceneRect(0, 0, 750, 750)
        self.view: ObjectBoxView = None
