from PyQt6.QtWidgets import QVBoxLayout, QGraphicsSceneMouseEvent, QComboBox
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from objects.prop import Prop, Staff, Club, Buugeng, Fan, Triad, Hoop

from widgets.graph_editor.object_panel.propbox.propbox_drag import PropBoxDrag
from widgets.graph_editor.object_panel.propbox.propbox_view import PropBoxView
from settings.string_constants import *


from objects.grid import Grid
from widgets.graph_editor.object_panel.objectbox import ObjectBox
from utilities.TypeChecking.TypeChecking import PropTypes, TYPE_CHECKING, Dict, List

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.pictograph.pictograph import Pictograph


class PropBox(ObjectBox):
    def __init__(self, main_widget: "MainWidget", pictograph: "Pictograph") -> None:
        super().__init__(main_widget, pictograph)
        self.main_widget = main_widget
        self.main_window = main_widget.main_window
        self.view = PropBoxView(self)
        self.prop_type = STAFF

        self.init_combobox()
        self.pictograph = pictograph

        self.grid = Grid(self)
        self.grid_position = QPointF(0, 0)
        self.grid.setPos(self.grid_position)

        self.drag = None
        self.props = []

        self.propbox_layout = QVBoxLayout()
        self.propbox_layout.addWidget(self.view)

        # self.init_propbox_clubs()
        # self.init_propbox_buugeng()
        # self.init_propbox_fans()
        # self.init_propbox_triads()
        # self.init_propbox_hoops()

        self.staffs: List[Staff] = []
        self.clubs: List[Club] = []
        self.buugeng: List[Buugeng] = []
        self.fans: List[Fan] = []
        self.triads: List[Triad] = []
        self.hoops: List[Hoop] = []

        self.populate_props()

    def populate_props(self) -> None:
        self.clear_props()
        initial_prop_attributes: List[Dict] = [
            {
                COLOR: RED,
                PROP_LOCATION: NORTH,
                LAYER: 1,
                ORIENTATION: IN,
            },
            {
                COLOR: BLUE,
                PROP_LOCATION: EAST,
                LAYER: 1,
                ORIENTATION: IN,
            },
            {
                COLOR: RED,
                PROP_LOCATION: SOUTH,
                LAYER: 1,
                ORIENTATION: IN,
            },
            {
                COLOR: BLUE,
                PROP_LOCATION: WEST,
                LAYER: 1,
                ORIENTATION: IN,
            },
        ]

        for attributes in initial_prop_attributes:
            if self.prop_type == STAFF:
                prop = Staff(self.pictograph, attributes)
            elif self.prop_type == CLUB:
                prop = Club(self.pictograph, attributes)
            elif self.prop_type == BUUGENG:
                prop = Buugeng(self.pictograph, attributes)
            elif self.prop_type == FAN:
                prop = Fan(self.pictograph, attributes)
            elif self.prop_type == TRIAD:
                prop = Triad(self.pictograph, attributes)
            elif self.prop_type == HOOP:
                prop = Hoop(self.pictograph, attributes)
            else:
                raise ValueError("Invalid prop type")

            prop.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
            prop.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable, True)
            self.set_prop_position(prop)
            self.addItem(prop)
            self.props.append(prop)

    def init_combobox(self) -> None:
        self.prop_type_combobox = QComboBox(self.view)
        # Populate the combobox with prop types, assuming prop types are strings in a list
        prop_types = ["Staff", "Club", "Buugeng", "Fan", "Triad", "Hoop"]
        self.prop_type_combobox.addItems(prop_types)
        # Set the default value to the current prop type
        self.prop_type_combobox.setCurrentText(str(self.prop_type.capitalize()))
        # Connect the combobox to change the prop type when a different prop is selected
        self.prop_type_combobox.currentTextChanged.connect(self.on_prop_type_change)
        # Position the combobox at the top right
        self.prop_type_combobox.move(
            0, 0
        )  # Position will be adjusted after the view is initialized

    def on_prop_type_change(self, text: str) -> None:
        new_prop_type = text.lower()
        self.change_prop_type(new_prop_type)
        self.update_prop_type_in_pictograph(new_prop_type)

    def clear_props(self) -> None:
        # Log the props before removal for debugging
        for prop in self.props[:]:  # Iterate over a shallow copy of the list
            self.removeItem(prop)
        self.props.clear()  # Clear the list after all items have been removed from the scene
        # Log after clearing to confirm

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
        self.pictograph.initializer.update_prop_set_and_ghost_props(new_prop_type)

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
                pictograph = self.main_widget.graph_editor.pictograph
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
                distance = (
                    cursor_pos - prop_center
                ).manhattanLength()  # Manhattan distance for simplicity

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


    def update_propbox_size(self) -> None:
        self.view.setFixedSize(
            int(self.pictograph.view.height() * 1 / 2),
            int(self.pictograph.view.height() * 1 / 2),
        )
