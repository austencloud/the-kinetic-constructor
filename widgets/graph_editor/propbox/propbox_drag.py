from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, QPoint, QPointF
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer

from objects.props.prop import Prop
from objects.arrow import BlankArrow
from utilities.TypeChecking.TypeChecking import (
    MotionAttributesDicts,
    Color,
)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from widgets.graph_editor.propbox.propbox import PropBox

class PropBoxDrag(QWidget):
    def __init__(self, main_widget: MainWidget, pictograph: Pictograph, propbox: PropBox) -> None:
        super().__init__(main_widget)
        self.pictograph = pictograph
        self.propbox = propbox
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Initialize QLabel to show the ghost image of the prop
        self.preview = QLabel(self)
        self.transform = QTransform()
        self.dragging_prop: Prop = None

    def start_drag(self, prop: Prop, cursor_pos: QPoint) -> None:
        self.dragging_prop = prop

        # Create pixmap from the prop's SVG
        pixmap = self._create_pixmap_from_svg(prop.svg_file)
        self.preview.setPixmap(pixmap)
        self.preview.show()

        # Position the widget at cursor position
        self._update_position(cursor_pos)

    def _create_pixmap_from_svg(self, svg_file: str) -> QPixmap:
        renderer = QSvgRenderer(svg_file)
        pixmap_size = renderer.defaultSize()
        pixmap = QPixmap(pixmap_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return pixmap

    def _update_position(self, cursor_pos: QPoint) -> None:
        # Convert cursor position to global and adjust the position of the preview
        global_pos = self.propbox.view.mapToGlobal(cursor_pos)
        self.move(global_pos - self.preview.rect().center())

    def mouseMoveEvent(self, event) -> None:
        if self.dragging_prop:
            self._update_position(event.pos())

    def mouseReleaseEvent(self, event) -> None:
        if self.dragging_prop:
            self._drop_prop(event.pos())
            self.dragging_prop = None
            self.preview.hide()

    def _drop_prop(self, cursor_pos: QPoint):
        # Convert cursor position to scene position
        global_pos = self.propbox.view.mapToGlobal(cursor_pos)
        scene_pos = self.pictograph.view.mapFromGlobal(global_pos)

        # Determine valid drop location and create blank arrow
        valid_location = self._get_valid_location(scene_pos)
        if valid_location:
            self._create_blank_arrow_at_location(valid_location)

    def _get_valid_location(self, scene_pos: QPointF) -> QPointF:
        # Implement logic to determine a valid location based on scene position
        # For now, let's just return the scene position
        return scene_pos

    def _create_blank_arrow_at_location(self, location: QPointF) -> None:
        # Define attributes for a blank arrow
        blank_arrow_attributes: MotionAttributesDicts = {
            # Populate with necessary attributes
            "color": Color.RED,  # Example attribute, adjust as needed
            # Add other necessary attributes here
        }

        # Create and add the blank arrow to the pictograph
        blank_arrow = BlankArrow(self.pictograph, blank_arrow_attributes)
        blank_arrow.setPos(location)
        self.pictograph.addItem(blank_arrow)
