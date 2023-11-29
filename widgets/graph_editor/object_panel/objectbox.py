from PyQt6.QtWidgets import QGraphicsScene
from widgets.graph_editor.object_panel.objectbox_view import ObjectBoxView
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.pictograph.pictograph import Pictograph


class ObjectBox(QGraphicsScene):
    def __init__(self, main_widget: "MainWidget", pictograph: "Pictograph") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.pictograph = pictograph
        self.setSceneRect(0, 0, 750, 750)
        self.setBackgroundBrush(Qt.GlobalColor.white)
        self.view = ObjectBoxView(self)
