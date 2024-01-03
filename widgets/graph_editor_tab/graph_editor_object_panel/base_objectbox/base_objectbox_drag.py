from PyQt6.QtWidgets import QWidget
from typing import TYPE_CHECKING, Optional, Union

from objects.graphical_object import GraphicalObject
from utilities.TypeChecking.TypeChecking import RotationAngles
from widgets.graph_editor_tab.graph_editor_object_panel.base_objectbox.base_objectbox import (
    BaseObjectBox,
)

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget

    from objects.pictograph.pictograph import Pictograph
    from widgets.graph_editor_tab.graph_editor_object_panel.arrowbox.arrowbox_drag import (
        ArrowBoxDrag,
    )
    from widgets.graph_editor_tab.graph_editor_object_panel.propbox.propbox_drag import (
        PropBoxDrag,
    )

from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, QPointF, QPoint
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer


class BaseObjectBoxDrag(QWidget):
    def __init__(
        self,
        main_widget: "MainWidget",
        pictograph: "Pictograph",
        BaseObjectBox: "BaseObjectBox",
    ) -> None:
        super().__init__(main_widget)
        self.setParent(main_widget)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.reset_drag_state()
        self.setup_dependencies(main_widget, pictograph, BaseObjectBox)

    def setup_dependencies(
        self,
        main_widget: "MainWidget",
        pictograph: "Pictograph",
        BaseObjectBox: "BaseObjectBox",
    ) -> None:
        self.preview = QLabel(self)
        self.transform = QTransform()
        self.BaseObjectBox = BaseObjectBox
        self.pictograph = pictograph
        self.main_widget = main_widget
        self.has_entered_pictograph_once = False
        self.current_rotation_angle = 0
        self.svg_file = None
        self.static_arrow = None

    def create_pixmap(
        self, target_object: GraphicalObject, drag_angle: RotationAngles
    ) -> None:
        new_svg_data = target_object.set_svg_color(self.color)
        renderer = QSvgRenderer()
        renderer.load(new_svg_data)

        scaled_size = (
            renderer.defaultSize()
            * self.main_widget.graph_editor_tab.graph_editor.main_pictograph.view_scale
        )
        original_pixmap = QPixmap(scaled_size)
        self.setMinimumSize(scaled_size)
        self.preview.setMinimumSize(scaled_size)
        original_pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(original_pixmap)
        renderer.render(painter)
        painter.end()

        rotate_transform = QTransform().rotate(drag_angle)
        rotated_pixmap = original_pixmap.transformed(rotate_transform)
        self.setMinimumSize(rotated_pixmap.size())
        self.preview.resize(rotated_pixmap.size())
        self.preview.setPixmap(rotated_pixmap)
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)

        return rotated_pixmap

    def reset_drag_state(self) -> None:
        self.dragging = False
        self.drag_preview = None
        self.current_rotation_angle = 0

    def match_target_object(
        self: Union["ArrowBoxDrag", "PropBoxDrag"],
        target_object: GraphicalObject,
        drag_angle: Optional[RotationAngles],
    ) -> None:
        self.target_object = target_object
        self.color = target_object.color
        self.svg_file = target_object.svg_file
        pixmap = self.create_pixmap(target_object, drag_angle)
        self.preview.setPixmap(pixmap)
        self.object_center = (
            self.target_object.boundingRect().center()
            * self.main_widget.graph_editor_tab.graph_editor.main_pictograph.view_scale
        )

    def move_to_cursor(self, event_pos: QPoint) -> None:
        local_pos = self.BaseObjectBox.view.mapTo(self.main_widget, event_pos)
        self.center = QPointF((self.preview.width() / 2), self.preview.height() / 2)
        self.move(local_pos - self.center.toPoint())

    def remove_same_color_objects(self) -> None:
        for prop in self.pictograph.props.values():
            if prop.color == self.color:
                if prop in self.pictograph.items():
                    self.pictograph.removeItem(prop)
        for arrow in self.pictograph.arrows.values():
            if arrow.color == self.color:
                if arrow in self.pictograph.items():
                    self.pictograph.removeItem(arrow)
        for motion in self.pictograph.motions.values():
            if motion.color == self.color:
                motion.clear_attributes()

    def start_drag(self, event_pos: "QPoint") -> None:
        self.move_to_cursor(event_pos)
        self.show()
