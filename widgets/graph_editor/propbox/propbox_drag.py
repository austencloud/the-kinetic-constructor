from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, QPoint, QPointF, QSize
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer
from objects.props.prop import Prop
from objects.arrow import BlankArrow
from utilities.TypeChecking.TypeChecking import *
from typing import TYPE_CHECKING
from settings.string_constants import *

if TYPE_CHECKING:
    from main import MainWindow
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from widgets.graph_editor.propbox.propbox import PropBox

class PropBoxDrag(QWidget):
    def __init__(self, main_window: "MainWindow", pictograph: "Pictograph", propbox: "PropBox") -> None:
        super().__init__(main_window)
        self.setParent(main_window)
        self._setup_dependencies(main_window, pictograph, propbox)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.preview = QLabel(self)
        self.transform = QTransform()
        self.attributes: PropAttributesDicts = {}

    def _setup_dependencies(self, main_window: "MainWindow", pictograph: "Pictograph", propbox: "PropBox") -> None:
        self.propbox = propbox
        self.pictograph = pictograph
        self.main_window = main_window
        self.has_entered_pictograph_once = False
        self.current_rotation_angle = 0
        self.previous_quadrant = None
        self.preview = None
        self.svg_file = None
        self.ghost_arrow = None

    def match_target_prop(self, target_prop: "Prop") -> None:
        self.target_prop = target_prop
        self.set_attributes(target_prop)
        pixmap = self.create_pixmap()
        self.preview.setPixmap(pixmap)
        self.prop_center = (self.target_prop.boundingRect().center() * self.pictograph.view.view_scale)
        self.current_rotation_angle = self.get_rotation_angle()

    def get_rotation_angle(self) -> RotationAngle:
        angle_map: Dict[Tuple[Layer, Orientation], Dict[Location, RotationAngle]] = {
            (1, IN): {NORTH: 90, SOUTH: 270, WEST: 0, EAST: 180},
            (1, OUT): {NORTH: 270, SOUTH: 90, WEST: 180, EAST: 0},
            (2, CLOCKWISE): {NORTH: 0, SOUTH: 180, WEST: 270, EAST: 90},
            (2, COUNTER_CLOCKWISE): {NORTH: 180, SOUTH: 0, WEST: 90, EAST: 270},
        }
        key = (self.layer, self.orientation)
        return angle_map.get(key, {}).get(self.location, 0)

    def set_attributes(self, target_prop: "Prop") -> None:
        self.color: Color = target_prop.color
        self.location: Location = target_prop.location
        self.layer: Layer = target_prop.layer
        self.orientation: Orientation = target_prop.orientation
        self.ghost_prop = self.pictograph.ghost_props[self.color]
        self.ghost_prop.target_prop = target_prop

    def start_drag(self, event_pos: "QPoint") -> None:
        self.move_to_cursor(event_pos)
        self.show()

    def move_to_cursor(self, event_pos: QPoint) -> None:
        local_pos = self.propbox.view.mapTo(self.main_window, event_pos)
        self.center = QPointF((self.width()/2), self.height()/2)
        self.move(local_pos - self.center.toPoint())

    def create_pixmap(self) -> None:        
        # Load the SVG data with the correct color
        new_svg_data = self.target_prop.set_svg_color(self.color)
        renderer = QSvgRenderer()
        renderer.load(new_svg_data)

        # Create the original pixmap from the SVG
        original_size = renderer.defaultSize() * self.pictograph.view.view_scale
        original_pixmap = QPixmap(original_size)
        self.setFixedSize(original_size)
        self.preview.setFixedSize(original_size)
        original_pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(original_pixmap)
        renderer.render(painter)
        painter.end()

        # Determine the rotation angle
        angle = self.get_rotation_angle()

        # Apply rotation transformation
        rotate_transform = QTransform().rotate(angle)
        rotated_pixmap = original_pixmap.transformed(rotate_transform)
        #rotate the label and widget too
        self.setFixedSize(rotated_pixmap.size())
        self.preview.setFixedSize(rotated_pixmap.size())

        # Set the rotated pixmap to the QLabel
        self.preview.setPixmap(rotated_pixmap)
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)

        return rotated_pixmap

    def _create_blank_arrow_at_location(self, location: QPointF) -> None:
        # Define attributes for a blank arrow
        blank_arrow_attributes: PropAttributesDicts = {
            # Populate with necessary attributes
            "color": RED,  # Example attribute, adjust as needed
            # Add other necessary attributes here
        }

        # Create and add the blank arrow to the pictograph
        blank_arrow = BlankArrow(self.pictograph, blank_arrow_attributes)
        blank_arrow.setPos(location)
        self.pictograph.addItem(blank_arrow)
