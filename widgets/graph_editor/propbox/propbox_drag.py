from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import Qt, QPoint, QPointF
from PyQt6.QtGui import QPixmap, QPainter, QTransform
from PyQt6.QtSvg import QSvgRenderer
from objects.props import Prop
from objects.arrow import StaticArrow
from utilities.TypeChecking.TypeChecking import *
from typing import TYPE_CHECKING
from settings.string_constants import *

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
        self.previous_location = None
        self.preview = None
        self.svg_file = None
        self.ghost_arrow = None

    def match_target_prop(self, target_prop: "Prop") -> None:
        self.target_prop = target_prop
        self.set_attributes(target_prop)
        pixmap = self.create_pixmap()
        self.preview.setPixmap(pixmap)
        self.prop_center = (
            self.target_prop.boundingRect().center() * self.pictograph.view.view_scale
        )
        self.current_rotation_angle = self.get_rotation_angle()

    def get_rotation_angle(self) -> RotationAngle:
        angle_map: Dict[Tuple[Layer, Orientation], Dict[Location, RotationAngle]] = {
            (1, IN): {NORTH: 90, SOUTH: 270, WEST: 0, EAST: 180},
            (1, OUT): {NORTH: 270, SOUTH: 90, WEST: 180, EAST: 0},
            (2, CLOCKWISE): {NORTH: 0, SOUTH: 180, WEST: 270, EAST: 90},
            (2, COUNTER_CLOCKWISE): {NORTH: 180, SOUTH: 0, WEST: 90, EAST: 270},
        }
        key = (self.layer, self.orientation)
        return angle_map.get(key, {}).get(self.prop_location, 0)

    def set_attributes(self, target_prop: "Prop") -> None:
        self.prop_type: PropType = target_prop.prop_type
        self.color: Color = target_prop.color
        self.prop_location: Location = target_prop.prop_location
        self.layer: Layer = target_prop.layer
        self.orientation: Orientation = target_prop.orientation
        self.ghost_prop = self.pictograph.ghost_props[self.color]
        self.ghost_prop.target_prop = target_prop

    def start_drag(self, event_pos: "QPoint") -> None:
        self.move_to_cursor(event_pos)
        self.show()

    def move_to_cursor(self, event_pos: QPoint) -> None:
        local_pos = self.propbox.view.mapTo(self.main_window, event_pos)
        self.center = QPointF((self.width() / 2), self.height() / 2)
        self.move(local_pos - self.center.toPoint())

    def create_pixmap(self) -> None:
        new_svg_data = self.target_prop.set_svg_color(self.color)
        renderer = QSvgRenderer()
        renderer.load(new_svg_data)

        scaled_size = renderer.defaultSize() * self.pictograph.view.view_scale
        original_pixmap = QPixmap(scaled_size)
        self.setFixedSize(scaled_size)
        self.preview.setFixedSize(scaled_size)
        original_pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(original_pixmap)
        renderer.render(painter)
        painter.end()

        angle = self.get_rotation_angle()

        rotate_transform = QTransform().rotate(angle)
        rotated_pixmap = original_pixmap.transformed(rotate_transform)
        self.setFixedSize(rotated_pixmap.size())
        self.preview.setFixedSize(rotated_pixmap.size())

        self.preview.setPixmap(rotated_pixmap)
        self.preview.setAlignment(Qt.AlignmentFlag.AlignCenter)

        return rotated_pixmap

    ### EVENT HANDLERS ###

    def handle_mouse_move(self, event_pos: QPoint) -> None:
        if self.preview:
            self.move_to_cursor(event_pos)
            if self.is_over_pictograph(event_pos):
                self.handle_enter_pictograph(event_pos)

    def is_over_pictograph(self, event_pos: QPoint) -> bool:
        pos_in_main_window = self.propbox.view.mapToGlobal(event_pos)
        local_pos_in_pictograph = self.pictograph.view.mapFromGlobal(pos_in_main_window)
        return self.pictograph.view.rect().contains(local_pos_in_pictograph)

    def handle_enter_pictograph(self, event_pos: QPoint) -> None:
        if not self.has_entered_pictograph_once:
            self.just_entered_pictograph = True
            self.has_entered_pictograph_once = True
            self.remove_same_color_prop()

        if self.has_entered_pictograph_once:
            self.just_entered_pictograph = False

        pos_in_main_window = self.propbox.view.mapToGlobal(event_pos)
        view_pos_in_pictograph = self.pictograph.view.mapFromGlobal(pos_in_main_window)
        scene_pos = self.pictograph.view.mapToScene(view_pos_in_pictograph)
        new_location = self.pictograph.get_location(scene_pos.x(), scene_pos.y())

        if self.previous_location != new_location and new_location:
            self.previous_location = new_location
            self.update_preview_for_new_location(new_location)
            self.ghost_prop.update_ghost_prop(self.attributes)

    def remove_same_color_prop(self) -> None:
        for prop in self.pictograph.props[:]:
            if prop.isVisible() and prop.color == self.color:
                self.pictograph.removeItem(prop)
                self.pictograph.props.remove(prop)
        for prop in self.pictograph.props[:]:
            if prop.isVisible() and prop.color == self.color:
                self.pictograph.removeItem(prop)
                self.pictograph.props.remove(prop)

    def update_preview_for_new_location(self, new_location: Location) -> None:
        self.prop_location = new_location

        self.ghost_prop.prop_type = self.prop_type
        self.ghost_prop.color = self.color
        self.ghost_prop.prop_location = new_location
        self.ghost_prop.orientation = self.orientation
        self.ghost_prop.layer = self.layer

        ghost_svg = self.ghost_prop.get_svg_file(self.prop_type)

        self.ghost_prop.update_svg(ghost_svg)

        self.update_rotation()
        self.update_static_arrow_during_drag()

        self.pictograph.add_motion(
            self.ghost_prop,
            self.ghost_prop.arrow,
            IN,
            1,
        )

        if self.ghost_prop not in self.pictograph.props:
            self.pictograph.props.append(self.ghost_prop)
        if self.ghost_prop not in self.pictograph.items():
            self.pictograph.addItem(self.ghost_prop)
        self.pictograph.update_pictograph()

    def update_prop_during_drag(self) -> None:
        for prop in self.pictograph.prop_set.values():
            if prop.color == self.color:
                if prop not in self.pictograph.props:
                    self.pictograph.props.append(prop)

                prop.set_attributes_from_dict(
                    {
                        COLOR: self.color,
                        LOCATION: self.end_location,
                        LAYER: 1,
                    }
                )
                prop.arrow = self.ghost_arrow
                self.ghost_arrow.prop = prop

                if prop not in self.pictograph.items():
                    self.pictograph.addItem(prop)
                prop.show()
                prop.update_appearance()
                self.pictograph.update_pictograph()

    def update_rotation(self) -> None:
        renderer = QSvgRenderer(self.target_prop.svg_file)
        scaled_size = renderer.defaultSize() * self.pictograph.view.view_scale
        pixmap = QPixmap(scaled_size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        with painter as painter:
            renderer.render(painter)

        angle = self.get_rotation_angle()

        unrotate_transform = QTransform().rotate(-self.current_rotation_angle)
        unrotated_pixmap = self.preview.pixmap().transformed(unrotate_transform)

        rotate_transform = QTransform().rotate(angle)
        rotated_pixmap = unrotated_pixmap.transformed(rotate_transform)

        self.current_rotation_angle = angle
        self.preview.setPixmap(rotated_pixmap)

    def _create_static_arrow_at_location(self, location: QPointF) -> None:
        static_arrow_attributes: PropAttributesDicts = {
            "color": RED,  # Example attribute, adjust as needed
        }

        static_arrow = StaticArrow(self.pictograph, static_arrow_attributes)
        static_arrow.setPos(location)
        self.pictograph.addItem(static_arrow)
