from typing import Dict
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsScene

from data.letter_engine_data import letter_types
from objects.arrow import Arrow
from objects.grid import Grid
from objects.prop import Prop
from objects.prop import Staff
from objects.motion import Motion
from settings.string_constants import (
    BLUE,
    BOX,
    COLOR,
    DIAMOND,
    END_LOCATION,
    LETTER_SVG_DIR,
    MOTION_TYPE,
    RED,
    ROTATION_DIRECTION,
    STAFF,
    START_LOCATION,
    TURNS,
    START_ORIENTATION,
    END_ORIENTATION,
    START_LAYER,
    END_LAYER,
    ARROW_LOCATION,
)
from utilities.letter_engine import LetterEngine
from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
    Colors,
    Layers,
    MotionAttributesDicts,
    List,
    MotionTypes,
    Optional,
    Orientations,
    Tuple,
)
from widgets.graph_editor.pictograph.pictograph_event_handler import (
    PictographEventHandler,
)
from widgets.graph_editor.pictograph.pictograph_view import PictographView
from widgets.graph_editor.pictograph.pictograph_init import PictographInit
from widgets.graph_editor.pictograph.pictograph_menu_handler import (
    PictographMenuHandler,
)
from widgets.graph_editor.pictograph.position_engines.arrow_positioner import (
    ArrowPositioner,
)
from widgets.graph_editor.pictograph.position_engines.prop_positioner import (
    PropPositioner,
)

if TYPE_CHECKING:
    from utilities.pictograph_generator import PictographGenerator
    from widgets.main_widget import MainWidget
    from widgets.graph_editor.graph_editor import GraphEditor
from objects.letter_item import LetterItem


class Pictograph(QGraphicsScene):
    def __init__(self, main_widget: "MainWidget", graph_editor: "GraphEditor") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.graph_editor = graph_editor

        self.setup_scene()
        self.setup_components(main_widget)

    def setup_scene(self) -> None:
        self.setSceneRect(0, 0, 750, 900)
        self.setBackgroundBrush(Qt.GlobalColor.white)
        self.arrows: List[Arrow] = []
        self.props: List[Prop] = []
        self.motions: List[Motion] = []
        self.current_letter: str = None

    def setup_components(self, main_widget: "MainWidget") -> None:
        self.letters = main_widget.letters
        self.generator: PictographGenerator = None
        self.event_handler = PictographEventHandler(self)

        self.dragged_arrow: Arrow = None
        self.dragged_prop: Staff = None
        self.initializer = PictographInit(self)

        self.prop_type: Prop = STAFF

        self.prop_set: Dict[Colors, Prop] = self.initializer.init_prop_set(
            self.prop_type
        )
        self.ghost_arrows = self.initializer.init_ghost_arrows()
        self.ghost_props = self.initializer.init_ghost_props(self.prop_type)

        self.grid: Grid = self.initializer.init_grid()
        self.view: PictographView = self.initializer.init_view()
        self.letter_item: LetterItem = self.initializer.init_letter_item()
        self.locations = self.initializer.init_locations(self.grid)

        self.setup_managers(main_widget)

    def set_letter_renderer(self, letter: str) -> None:
        letter_type = self.get_current_letter_type()
        svg_path = f"{LETTER_SVG_DIR}/{letter_type}/{letter}.svg"
        renderer = QSvgRenderer(svg_path)
        if renderer.isValid():
            self.letter_item.setSharedRenderer(renderer)

    def setup_managers(self, main_widget: "MainWidget") -> None:
        self.pictograph_menu_handler = PictographMenuHandler(main_widget, self)
        self.arrow_positioner = ArrowPositioner(self)
        self.prop_positioner = PropPositioner(self)
        self.letter_engine = LetterEngine(self)

    ### EVENTS ###

    def mousePressEvent(self, event) -> None:
        self.main_widget.deselect_all_except(self)
        self.event_handler.handle_mouse_press(event)

    def mouseMoveEvent(self, event) -> None:
        self.event_handler.handle_mouse_move(event)

    def mouseReleaseEvent(self, event) -> None:
        self.event_handler.handle_mouse_release(event)

    def contextMenuEvent(self, event) -> None:
        self.event_handler.handle_context_menu(event)

    ### GETTERS ###

    def get_current_arrow_coordinates(
        self,
    ) -> Tuple[Optional[QPointF], Optional[QPointF]]:
        red_position = None
        blue_position = None

        for arrow in self.arrows:
            center = arrow.pos() + arrow.boundingRect().center()
            if arrow.color == RED:
                red_position = center
            elif arrow.color == BLUE:
                blue_position = center
        return red_position, blue_position

    def get_state(self) -> List[MotionAttributesDicts]:
        state = []
        for motion in self.motions:
            state.append(
                {
                    COLOR: motion.color,
                    MOTION_TYPE: motion.motion_type,
                    ROTATION_DIRECTION: motion.rotation_direction,
                    ARROW_LOCATION: motion.arrow.arrow_location,
                    START_LOCATION: motion.start_location,
                    END_LOCATION: motion.end_location,
                    TURNS: motion.turns,
                    START_LOCATION: motion.start_location,
                    END_LOCATION: motion.end_location,
                    START_ORIENTATION: motion.start_orientation,
                    END_ORIENTATION: motion.end_orientation,
                    START_LAYER: motion.start_layer,
                    END_LAYER: motion.end_layer,
                }
            )
        return state

    def get_current_letter_type(self) -> Optional[str]:
        if self.current_letter is not None:
            for letter_type, letters in letter_types.items():
                if self.current_letter in letters:
                    return letter_type
        else:
            return None

    def get_motion_by_color(self, color: str) -> Optional[Motion]:
        for motion in self.motions:
            if motion.color == color:
                return motion

    def get_arrow_by_color(self, color: str) -> Optional[Arrow]:
        for arrow in self.arrows:
            if arrow.color == color:
                return arrow

    def get_prop_by_color(self, color: str) -> Optional[Staff]:
        for prop in self.prop_set.values():
            if prop.color == color:
                return prop

    def get_closest_hand_point(
        self, pos: QPointF
    ) -> Tuple[Optional[str], Optional[QPointF]]:
        min_distance = float("inf")
        nearest_point_name = None
        nearest_point_coords = None

        if self.grid.grid_mode == DIAMOND:
            for name, point in self.grid.diamond_hand_points.items():
                distance = (pos - point).manhattanLength()
                if distance < min_distance:
                    min_distance = distance
                    nearest_point_name = name
                    nearest_point_coords = point

        elif self.grid.grid_mode == BOX:
            for name, point in self.grid.box_hand_points.items():
                distance = (pos - point).manhattanLength()
                if distance < min_distance:
                    min_distance = distance
                    nearest_point_name = name
                    nearest_point_coords = point

        return nearest_point_name, nearest_point_coords

    def get_closest_layer2_point(
        self, pos: QPointF
    ) -> Tuple[Optional[str], Optional[QPointF]]:
        min_distance = float("inf")
        nearest_point_name = None
        nearest_point_coords = None

        if self.grid.grid_mode == DIAMOND:
            for name, point in self.grid.diamond_layer2_points.items():
                distance = (pos - point).manhattanLength()
                if distance < min_distance:
                    min_distance = distance
                    nearest_point_name = name
                    nearest_point_coords = point

        elif self.grid.grid_mode == BOX:
            for name, point in self.grid.box_layer2_points.items():
                distance = (pos - point).manhattanLength()
                if distance < min_distance:
                    min_distance = distance
                    nearest_point_name = name
                    nearest_point_coords = point

        return nearest_point_name, nearest_point_coords

    ### HELPERS ###

    def add_to_sequence_callback(self) -> None:
        copied_scene = self.copy_scene()
        self.main_widget.sequence.frame.add_scene_to_sequence(copied_scene)
        self.clear_pictograph()

    def rotate_pictograph(self, direction: str) -> None:
        for arrow in self.arrows:
            arrow.rotate_arrow(direction)

    def clear_pictograph(self) -> None:
        self.arrows = []
        self.props = []
        self.motions = []
        for item in self.items():
            if isinstance(item, Arrow) or isinstance(item, Prop):
                self.removeItem(item)

        self.update_pictograph()

    def clear_selections(self) -> None:
        for arrow in self.arrows:
            arrow.setSelected(False)
        for prop in self.props:
            prop.setSelected(False)
        self.dragged_prop = None
        self.dragged_arrow = None

    def add_motion(
        self,
        arrow: Arrow,
        prop: Prop,
        motion_type: MotionTypes,
        start_orientation: Orientations,
        start_layer: Layers,
    ) -> None:
        motion_attributes: MotionAttributesDicts = {
            COLOR: arrow.color,
            MOTION_TYPE: motion_type,
            ROTATION_DIRECTION: arrow.rotation_direction,
            ARROW_LOCATION: arrow.arrow_location,
            TURNS: arrow.turns,
            START_ORIENTATION: start_orientation,
            START_LAYER: start_layer,
        }

        motion = Motion(self, arrow, prop, motion_attributes)
        arrow.motion = motion
        prop.motion = motion

        for m in self.motions:
            if m.color == motion.color:
                self.motions.remove(m)

        self.motions.append(motion)

    def copy_scene(self) -> QGraphicsScene:
        from widgets.sequence.beat import Beat

        new_scene = Beat(self.main_widget, self.graph_editor)
        new_scene.setSceneRect(self.sceneRect())
        new_scene.motions = self.motions

        for item in self.items():
            if isinstance(item, Arrow):
                new_arrow = Arrow(new_scene, item.get_attributes())
                new_arrow.setTransformOriginPoint(new_arrow.boundingRect().center())
                new_arrow.setPos(item.pos())
                new_arrow.setZValue(item.zValue())
                new_scene.addItem(new_arrow)
                new_scene.arrows.append(new_arrow)
                motion = new_scene.get_motion_by_color(new_arrow.color)
                new_arrow.motion = motion
                motion.arrow = new_arrow

            elif isinstance(item, Prop):
                new_prop = Prop(new_scene, item.get_attributes())
                new_prop.setPos(item.pos())
                new_prop.setZValue(item.zValue())
                new_scene.addItem(new_prop)
                new_scene.props.append(new_prop)
                motion = new_scene.get_motion_by_color(new_prop.color)
                new_prop.motion = motion
                motion.prop = new_prop

        for arrow in new_scene.arrows:
            for prop in new_scene.props:
                if arrow.color == prop.color:
                    arrow.prop = prop
                    prop.arrow = arrow

        for arrow in new_scene.arrows:
            for ghost_arrow in new_scene.ghost_arrows.values():
                if arrow.color == ghost_arrow.color:
                    arrow.ghost_arrow = ghost_arrow
                    ghost_arrow.update_attributes(arrow.get_attributes())
                    ghost_arrow.set_is_svg_mirrored_from_attributes()
                    ghost_arrow.update_mirror()
                    ghost_arrow.update_svg(arrow.svg_file)
                    ghost_arrow.update_appearance()

        for prop in new_scene.props:
            for ghost_prop in new_scene.ghost_props.values():
                if prop.color == ghost_prop.color:
                    prop.ghost_prop = ghost_prop
                    ghost_prop.update_prop_type(prop.prop_type)

        for ghost_arrow in new_scene.ghost_arrows.values():
            for motion in new_scene.motions:
                if ghost_arrow.color == motion.color:
                    ghost_arrow.motion = motion

        for ghost_prop in new_scene.ghost_props.values():
            for motion in new_scene.motions:
                if ghost_prop.color == motion.color:
                    ghost_prop.motion = motion

        new_scene.update_pictograph()

        return new_scene

    ### UPDATERS ###

    def update_attr_panel(self):
        # Pass the selected motion color to update_attr_panel
        motions = [
            motion
            for motion in [
                self.get_motion_by_color(RED),
                self.get_motion_by_color(BLUE),
            ]
            if motion is not None
        ]

        if not motions:
            self.graph_editor.attr_panel.clear_all_attr_boxes()
        for motion in motions:
            self.graph_editor.attr_panel.update_attr_panel(motion.color)

    def update_pictograph(self) -> None:
        self.update_letter()
        self.update_arrows()
        self.update_props()
        self.update_attr_panel()

    def update_arrows(self) -> None:
        self.arrow_positioner.update_arrow_positions()

    def update_props(self) -> None:
        self.prop_positioner.update_prop_positions()

    def update_letter(self) -> None:
        if len(self.props) == 2:
            self.current_letter = self.letter_engine.get_current_letter()
        else:
            self.current_letter = None
        self.update_letter_item(self.current_letter)
        self.letter_item.position_letter_item(self.letter_item)

    def update_letter_item(self, letter: str) -> None:
        if letter:
            self.set_letter_renderer(letter)
        else:
            self.letter_item.setSharedRenderer(
                QSvgRenderer(f"{LETTER_SVG_DIR}/blank.svg")
            )
