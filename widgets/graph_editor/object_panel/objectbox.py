from PyQt6.QtWidgets import QGraphicsScene, QGraphicsSceneMouseEvent
from widgets.graph_editor.object_panel.objectbox_drag import ObjectBoxDrag
from widgets.graph_editor.object_panel.objectbox_view import ObjectBoxView
from PyQt6.QtCore import Qt
from objects.graphical_object import GraphicalObject
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
        self.view: ObjectBoxView = None
        
    def mousePressEvent(self, event) -> None:
        scene_pos = event.scenePos()
        event_pos = self.view.mapFromScene(scene_pos)

        closest_object = None
        min_distance = float("inf")
        for object in self.items():
            if isinstance(object, GraphicalObject):
                object_center = object.sceneBoundingRect().center()
                distance = (scene_pos - object_center).manhattanLength()
                if distance < min_distance:
                    closest_object = object
                    min_distance = distance
        
        if closest_object:
            self.target_object = closest_object
            if not self.objectbox_drag:
                pictograph = self.main_widget.graph_editor.pictograph
                self.objectbox_drag = ObjectBoxDrag(self.main_window, pictograph, self)
            if event.button() == Qt.MouseButton.LeftButton:
                self.objectbox_drag.match_target_object(self.target_object)
                self.objectbox_drag.handle_mouse_press(event_pos)
                self.objectbox_drag.start_drag(event_pos)
        else:
            self.target_object = None
            event.ignore()