from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, QPoint, QPointF
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer

from objects.props.prop import Prop
from objects.arrow import BlankArrow
from settings.string_constants import IN
from utilities.TypeChecking.TypeChecking import (
    Layer,
    Location,
    Orientation,
    PropAttributesDicts,
    Color,
)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import MainWindow
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from widgets.graph_editor.propbox.propbox import PropBox


class PropBoxDrag(QWidget):
    def __init__(
        self, main_window: "MainWindow", pictograph: "Pictograph", propbox: "PropBox"
    ) -> None:
        super().__init__(main_window)
        self.setParent(main_window)
        self._setup_dependencies(main_window, pictograph, propbox)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Initialize QLabel to show the ghost image of the prop
        self.preview = QLabel(self)
        self.transform = QTransform()
        self.attributes: PropAttributesDicts = {}

    def _setup_dependencies(
        self, main_window: "MainWindow", pictograph: "Pictograph", propbox: "PropBox"
    ) -> None:
        self.propbox = propbox
        self.pictograph = pictograph
        self.main_window = main_window
        self.has_entered_pictograph_once = False
        self.current_rotation_angle = 0
        self.previous_quadrant = None
        self.preview = None
        self.svg_file = None
        self.ghost_arrow = None
        self.start_orientation = IN

    def match_target_prop(self, target_prop: "Prop") -> None:
        self.target_prop = target_prop
        self.set_attributes(target_prop)
        pixmap = self.create_pixmap(target_prop)
        self.preview.setPixmap(pixmap)
        self.preview.setFixedHeight(pixmap.height())
        self.arrow_center = (
            self.target_prop.boundingRect().center() * self.pictograph.view.view_scale
        )
        self.current_rotation_angle = target_prop.get_rotation_angle()
        self.is_svg_mirrored = target_prop.is_svg_mirrored
        self.preview.setPixmap(pixmap)
        self.apply_transformations_to_preview()

    def set_attributes(self, target_prop: "Prop") -> None:
        self.color: Color = target_prop.color
        self.location: Location = target_prop.location
        self.layer: Layer = target_prop.layer
        self.orientation: Orientation = target_prop.orientation

        self.ghost_prop = self.pictograph.ghost_props[self.color]
        self.ghost_prop.target_prop = target_prop

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
        blank_arrow_attributes: PropAttributesDicts = {
            # Populate with necessary attributes
            "color": Color.RED,  # Example attribute, adjust as needed
            # Add other necessary attributes here
        }

        # Create and add the blank arrow to the pictograph
        blank_arrow = BlankArrow(self.pictograph, blank_arrow_attributes)
        blank_arrow.setPos(location)
        self.pictograph.addItem(blank_arrow)
