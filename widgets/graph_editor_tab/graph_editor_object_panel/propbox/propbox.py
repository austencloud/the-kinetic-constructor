from PyQt6.QtWidgets import QVBoxLayout, QGraphicsSceneMouseEvent, QComboBox
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtSvgWidgets import QGraphicsSvgItem
from objects.prop.prop import *
from objects.prop.prop_types import BigTriad
from utilities.TypeChecking.prop_types import PropTypesList
from widgets.graph_editor_tab.graph_editor_object_panel.base_objectbox.base_objectbox import (
    BaseObjectBox,
)
from widgets.graph_editor_tab.graph_editor_object_panel.propbox.propbox_drag import (
    PropBoxDrag,
)
from widgets.graph_editor_tab.graph_editor_object_panel.propbox.propbox_view import (
    PropBoxView,
)
from constants import *
from objects.grid import Grid
from utilities.TypeChecking.TypeChecking import TYPE_CHECKING, Dict, List
from utilities.TypeChecking.prop_types import (
    PropTypes,
    strictly_placed_props,
)

if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor_tab.graph_editor_frame import GraphEditorFrame


class PropBox(BaseObjectBox):
    def __init__(
        self, main_widget: "MainWidget", graph_editor: "GraphEditorFrame"
    ) -> None:
        super().__init__(main_widget, graph_editor)
        self.setup_properties(main_widget, graph_editor)
        self.setup_ui()
        self.populate_props()

    def setup_properties(
        self, main_widget: "MainWidget", graph_editor: "GraphEditorFrame"
    ) -> None:
        self.main_widget = main_widget
        self.view = PropBoxView(self, graph_editor)
        self.prop_type = main_widget.prop_type
        self.pictograph = graph_editor.main_pictograph
        self.grid = Grid(self)
        self.grid_position = QPointF(0, 0)
        self.grid.setPos(self.grid_position)
        self.drag: PropBoxDrag = None
        self.props: List[Prop] = []

    def setup_ui(self) -> None:
        self.init_combobox()
        self.propbox_layout = QVBoxLayout()
        self.propbox_layout.addWidget(self.view)

    def init_combobox(self) -> None:
        self.prop_type_combobox = QComboBox(self.view)
        for item in PropTypesList:
            self.prop_type_combobox.addItem(str(item.capitalize()))

    def populate_props(self) -> None:
        self.clear_props()
        default_prop_dicts: List[Dict] = self.get_initial_prop_attributes()
        prop_classes: Dict[str, type] = self.get_prop_classes()

        for prop_dict in default_prop_dicts:
            self.create_and_setup_prop(prop_dict, prop_classes)

    def get_prop_classes(self) -> Dict[str, type]:
        from objects.prop.prop_types import (
            Staff,
            BigStaff,
            Club,
            Buugeng,
            BigBuugeng,
            Fractalgeng,
            Fan,
            BigFan,
            Triad,
            MiniHoop,
            DoubleStar,
            BigHoop,
            BigDoubleStar,
            Quiad,
            Sword,
            Guitar,
            Ukulele,
            Chicken,
        )

        return {
            STAFF: Staff,
            BIGSTAFF: BigStaff,
            CLUB: Club,
            BUUGENG: Buugeng,
            BIGBUUGENG: BigBuugeng,
            FRACTALGENG: Fractalgeng,
            FAN: Fan,
            BIGFAN: BigFan,
            TRIAD: Triad,
            BIGTRIAD: BigTriad,
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

    def create_and_setup_prop(
        self, prop_dict: Dict, prop_classes: Dict[str, type]
    ) -> None:
        prop_class = prop_classes.get(self.prop_type)
        if not prop_class:
            raise ValueError("Invalid prop type")

        prop = prop_class(
            self.pictograph,
            prop_dict,
            self.pictograph.motions[prop_dict[COLOR]],
        )
        self.setup_prop(prop)
        self.props.append(prop)

    def setup_prop(self, prop: Prop) -> None:
        prop.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsMovable, True)
        prop.setFlag(QGraphicsSvgItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.set_prop_position(prop)
        self.addItem(prop)

    def get_initial_prop_attributes(self) -> List[Dict]:
        if self.grid.grid_mode == DIAMOND:
            return self.get_diamond_mode_attributes()
        elif self.grid.grid_mode == BOX:
            return self.get_box_mode_attributes()
        else:
            raise ValueError("Invalid grid mode")

    def get_diamond_mode_attributes(self) -> List[Dict]:
        return [
            {
                PROP_TYPE: self.prop_type,
                LOC: NORTH,
                ORI: IN,
                COLOR: RED,
            },
            {
                COLOR: BLUE,
                PROP_TYPE: self.prop_type,
                LOC: EAST,
                ORI: IN,
            },
            {
                COLOR: RED,
                PROP_TYPE: self.prop_type,
                LOC: SOUTH,
                ORI: IN,
            },
            {
                COLOR: BLUE,
                PROP_TYPE: self.prop_type,
                LOC: WEST,
                ORI: IN,
            },
        ]

    def get_box_mode_attributes(self) -> List[Dict]:
        return [
            {
                COLOR: RED,
                PROP_TYPE: self.prop_type,
                LOC: NORTHEAST,
                ORI: IN,
            },
            {
                COLOR: BLUE,
                PROP_TYPE: self.prop_type,
                LOC: SOUTHEAST,
                ORI: IN,
            },
            {
                COLOR: RED,
                PROP_TYPE: self.prop_type,
                LOC: SOUTHWEST,
                ORI: IN,
            },
            {
                COLOR: BLUE,
                PROP_TYPE: self.prop_type,
                LOC: NORTHWEST,
                ORI: IN,
            },
        ]

    def on_prop_type_change(self, text: str) -> None:
        new_prop_type = text.lower()
        self.change_prop_type(new_prop_type)
        self.update_prop_type_in_pictograph(new_prop_type)

    def clear_props(self) -> None:
        for prop in self.props:
            self.removeItem(prop)
        self.props.clear()

    def set_prop_position(self, prop: Prop) -> None:
        # Use cached coordinates directly
        if prop in strictly_placed_props:
            hand_point = self.grid.circle_coordinates_cache["hand_points"][
                self.main_widget.grid_mode
            ]["strict"][f"strict_{prop.loc}_{self.main_widget.grid_mode}_hand_point"]
        else:
            hand_point = self.grid.circle_coordinates_cache["hand_points"][
                self.main_widget.grid_mode
            ]["normal"][f"{prop.loc}_{self.main_widget.grid_mode}_hand_point"]
        prop_length = prop.boundingRect().width()
        prop_width = prop.boundingRect().height()
        offset_x = -prop_length / 2
        offset_y = -prop_width / 2
        prop_position = hand_point + QPointF(offset_x, offset_y)
        prop.setPos(prop_position)
        prop._update_prop_rotation_angle()
        prop.setTransformOriginPoint(prop.boundingRect().center())

    def change_prop_type(self, new_prop_type: PropTypes) -> None:
        self.prop_type = new_prop_type
        self.clear_props()
        self.populate_props()

    def update_prop_type_in_pictograph(self, new_prop_type: PropTypes) -> None:
        for prop in self.pictograph.props.values():
            prop.update_prop_type(new_prop_type)
        for ghost_prop in self.pictograph.ghost_props.values():
            ghost_prop.update_prop_type(new_prop_type)
        self.pictograph.main_widget.prop_type = new_prop_type
        self.pictograph.update_pictograph()

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
                    self.main_widget.graph_editor_tab.graph_editor.main_pictograph
                )
                self.drag = PropBoxDrag(self.main_widget, pictograph, self)
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
                    prop.is_dim(True)
                else:
                    prop.is_dim(False)

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
