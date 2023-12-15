from PyQt6.QtWidgets import QVBoxLayout, QGraphicsSceneMouseEvent, QComboBox
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from objects.prop import (
    BigHoop,
    DoubleStar,
    BigDoubleStar,
    Prop,
    Staff,
    BigStaff,
    Club,
    Buugeng,
    Fan,
    Triad,
    MiniHoop,
    Quiad,
    Sword,
    Guitar,
    Ukulele,
    Chicken,
)

from widgets.graph_editor.object_panel.propbox.propbox_drag import PropBoxDrag
from widgets.graph_editor.object_panel.propbox.propbox_view import PropBoxView
from constants.string_constants import *


from objects.grid import Grid
from widgets.graph_editor.object_panel.objectbox import ObjectBox
from utilities.TypeChecking.TypeChecking import PropTypes, TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.graph_editor import GraphEditor


class PropBox(ObjectBox):
    def __init__(self, main_widget: "MainWidget", graph_editor: "GraphEditor") -> None:
        super().__init__(main_widget, graph_editor)
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.view = PropBoxView(self, graph_editor)
        self.prop_type = STAFF

        self.init_combobox()
        self.pictograph = graph_editor.pictograph

        self.grid = Grid(self)
        self.grid_position = QPointF(0, 0)
        self.grid.setPos(self.grid_position)

        self.drag: PropBoxDrag = None
        self.props: List[Prop] = []

        self.propbox_layout = QVBoxLayout()
        self.propbox_layout.addWidget(self.view)

        self.populate_props()

    def populate_props(self) -> None:
        self.clear_props()
        initial_prop_attributes: List[Dict] = self.get_initial_prop_attributes()

        # Mapping prop types to their respective classes
        prop_classes: Dict[str, type] = {
            STAFF: Staff,
            BIGSTAFF: BigStaff,
            CLUB: Club,
            BUUGENG: Buugeng,
            FAN: Fan,
            TRIAD: Triad,
            MINIHOOP: MiniHoop,
            DOUBLESTAR: DoubleStar,
            BIGHOOP: BigHoop,
            BIGDOUBLESTAR: BigDoubleStar,
            QUIAD: Quiad,
            SWORD: Sword,
            GUITAR: Guitar,
            UKULELE: Ukulele,
            CHICKEN: Chicken,
        }

        for attributes in initial_prop_attributes:
            prop_class = prop_classes.get(self.prop_type)
            if prop_class:
                prop = prop_class(
                    self.pictograph,
                    attributes,
                    self.pictograph.motions[attributes[COLOR]],
                )
                self.setup_prop(prop)
                self.props.append(prop)
            else:
                raise ValueError("Invalid prop type")

    def setup_prop(self, prop: Prop) -> None:
        prop.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        prop.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.set_prop_position(prop)
        self.addItem(prop)

    def get_initial_prop_attributes(self) -> List[Dict]:
        if self.grid.grid_mode == DIAMOND:
            return [
                {
                    COLOR: RED,
                    PROP_TYPE: self.prop_type,
                    PROP_LOCATION: NORTH,
                    LAYER: 1,
                    ORIENTATION: IN,
                },
                {
                    COLOR: BLUE,
                    PROP_TYPE: self.prop_type,
                    PROP_LOCATION: EAST,
                    LAYER: 1,
                    ORIENTATION: IN,
                },
                {
                    COLOR: RED,
                    PROP_TYPE: self.prop_type,
                    PROP_LOCATION: SOUTH,
                    LAYER: 1,
                    ORIENTATION: IN,
                },
                {
                    COLOR: BLUE,
                    PROP_TYPE: self.prop_type,
                    PROP_LOCATION: WEST,
                    LAYER: 1,
                    ORIENTATION: IN,
                },
            ]
        elif self.grid.grid_mode == BOX:
            return [
                {
                    COLOR: RED,
                    PROP_TYPE: self.prop_type,
                    PROP_LOCATION: NORTHEAST,
                    LAYER: 1,
                    ORIENTATION: IN,
                },
                {
                    COLOR: BLUE,
                    PROP_TYPE: self.prop_type,
                    PROP_LOCATION: SOUTHEAST,
                    LAYER: 1,
                    ORIENTATION: IN,
                },
                {
                    COLOR: RED,
                    PROP_TYPE: self.prop_type,
                    PROP_LOCATION: SOUTHWEST,
                    LAYER: 1,
                    ORIENTATION: IN,
                },
                {
                    COLOR: BLUE,
                    PROP_TYPE: self.prop_type,
                    PROP_LOCATION: NORTHWEST,
                    LAYER: 1,
                    ORIENTATION: IN,
                },
            ]
        else:
            raise ValueError("Invalid grid mode")

    def init_combobox(self) -> None:
        self.prop_type_combobox = QComboBox(self.view)
        prop_types = [
            "Staff",
            "BigStaff",
            "Club",
            "Buugeng",
            "Fan",
            "Triad",
            "MiniHoop",
            "Bighoop",
            "Doublestar",
            "Bigdoublestar",
            "Quiad",
            "Sword",
            "Guitar",
            "Ukulele",
            "Chicken",
        ]
        self.prop_type_combobox.addItems(prop_types)

        self.prop_type_combobox.setCurrentText(str(self.prop_type.capitalize()))
        self.prop_type_combobox.currentTextChanged.connect(self.on_prop_type_change)
        self.prop_type_combobox.move(0, 0)

    def on_prop_type_change(self, text: str) -> None:
        new_prop_type = text.lower()
        self.change_prop_type(new_prop_type)
        self.update_prop_type_in_pictograph(new_prop_type)

    def clear_props(self) -> None:
        for prop in self.props[:]:
            self.removeItem(prop)
        self.props.clear()

    def set_prop_position(self, prop: Prop) -> None:
        hand_point = self.grid.get_circle_coordinates(
            f"{prop.prop_location}_{self.grid.grid_mode}_hand_point"
        )
        prop_length = prop.boundingRect().width()
        prop_width = prop.boundingRect().height()
        offset_x = -prop_length / 2
        offset_y = -prop_width / 2
        prop_position = hand_point + QPointF(offset_x, offset_y)
        prop.setPos(prop_position)
        prop.update_appearance()
        prop.setTransformOriginPoint(prop.boundingRect().center())

    def change_prop_type(self, new_prop_type: PropTypes) -> None:
        self.prop_type = new_prop_type
        self.clear_props()
        self.populate_props()

    def update_prop_type_in_pictograph(self, new_prop_type: PropTypes) -> None:
        self.pictograph.initializer.update_props_and_ghost_props(new_prop_type)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        scene_pos = event.scenePos()
        event_pos = self.view.mapFromScene(scene_pos)

        closest_prop = None
        min_distance = float("inf")
        for prop in self.props:
            prop_center = prop.sceneBoundingRect().center()
            distance = (scene_pos - prop_center).manhattanLength()
            if distance < min_distance:
                closest_prop = prop
                min_distance = distance

        if closest_prop:
            self.target_prop = closest_prop
            if not self.drag:
                pictograph = (
                    self.main_widget.graph_editor_widget.graph_editor.pictograph
                )
                self.drag = PropBoxDrag(self.main_window, pictograph, self)
            if event.button() == Qt.MouseButton.LeftButton:
                self.drag.match_target_prop(self.target_prop)
                self.drag.start_drag(event_pos)
        else:
            self.target_prop = None
            event.ignore()

    def mouseMoveEvent(self, event) -> None:
        if self.target_prop and self.drag:
            scene_pos = event.scenePos()
            event_pos = self.view.mapFromScene(scene_pos)
            self.drag.handle_mouse_move(event_pos)
        else:
            cursor_pos = event.scenePos()
            closest_prop = None
            min_distance = float("inf")

            for prop in self.props:
                prop_center = prop.sceneBoundingRect().center()
                distance = (cursor_pos - prop_center).manhattanLength()

                if distance < min_distance:
                    closest_prop = prop
                    min_distance = distance

            for prop in self.props:
                if prop != closest_prop:
                    prop.is_dim(True)  # Highlight all props except the closest one
                else:
                    prop.is_dim(False)  # Do not highlight the closest one

    def mouseReleaseEvent(self, event) -> None:
        if self.target_prop and self.drag:
            scene_pos = event.scenePos()
            event_pos = self.view.mapFromScene(scene_pos)
            self.drag.handle_mouse_release()
            self.target_prop = None
        else:
            event.ignore()

    def dim_all_props(self) -> None:
        for prop in self.props:
            prop.is_dim(True)
