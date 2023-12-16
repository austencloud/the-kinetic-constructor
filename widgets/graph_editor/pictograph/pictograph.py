from re import S
from typing import Dict
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsScene

from data.letter_engine_data import letter_types
from objects.arrow.arrow import Arrow
from objects.grid import Grid
from objects.prop import Prop
from objects.motion import Motion
from constants.string_constants import (
    ARROW,
    BLUE,
    BOX,
    COLOR,
    DIAMOND,
    END_LOCATION,
    LETTER_SVG_DIR,
    MOTION_TYPE,
    PROP,
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
    PropTypes,
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
        self.arrows: Dict[Colors, Arrow] = {}
        self.props: Dict[Colors, Prop] = {}
        self.motions: Dict[Colors, Motion] = {}
        self.current_letter: str = None

    def setup_components(self, main_widget: "MainWidget") -> None:
        self.generator: PictographGenerator = None
        self.event_handler = PictographEventHandler(self)

        self.dragged_arrow: Arrow = None
        self.dragged_prop: Prop = None
        self.initializer = PictographInit(self)

        self.prop_type: PropTypes = STAFF
        self.arrow_turns = 0

        self.grid: Grid = self.initializer.init_grid()
        self.view: PictographView = self.initializer.init_view()
        self.letter_item: LetterItem = self.initializer.init_letter_item()
        self.locations = self.initializer.init_locations(self.grid)

        self.motions = self.initializer.init_motions()
        self.arrows = self.initializer.init_arrows()
        self.ghost_arrows = self.initializer.init_ghost_arrows()
        self.props = self.initializer.init_props(self.prop_type)
        self.ghost_props = self.initializer.init_ghost_props(self.prop_type)

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

    ### EVENT HANDLERS ###

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

        for arrow in self.arrows.values():
            center = arrow.pos() + arrow.boundingRect().center()
            if arrow.color == RED:
                red_position = center
            elif arrow.color == BLUE:
                blue_position = center
        return red_position, blue_position

    def get_state(self) -> List[MotionAttributesDicts]:
        state = []
        for motion in self.motions.values():
            state.append(
                {
                    COLOR: motion.color,
                    MOTION_TYPE: motion.motion_type,
                    ROTATION_DIRECTION: motion.rotation_direction,
                    ARROW_LOCATION: motion.arrow_location,
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
        self.main_widget.sequence_widget.beat_frame.add_scene_to_sequence(copied_scene)
        self.clear_pictograph()

    def rotate_pictograph(self, direction: str) -> None:
        for arrow in self.arrows:
            arrow.rotate_arrow(direction)

    def clear_pictograph(self) -> None:
        self.arrows = {}
        self.props = {}
        for motion in self.motions.values():
            motion.reset_motion_attributes()
        for item in self.items():
            if isinstance(item, Arrow) or isinstance(item, Prop):
                self.removeItem(item)

        self.update_pictograph()

    def clear_selections(self) -> None:
        for arrow in self.arrows.values():
            arrow.setSelected(False)
        for prop in self.props.values():
            prop.setSelected(False)
        self.dragged_prop = None
        self.dragged_arrow = None

    def copy_scene(self) -> QGraphicsScene:
        from widgets.sequence_widget.beat_frame.beat import Beat

        new_beat = Beat(self.main_widget, self.graph_editor)
        new_beat.setSceneRect(self.sceneRect())
        new_beat.motions = self.motions

        for item in self.items():
            if isinstance(item, Arrow):
                new_arrow = Arrow(
                    new_beat, item.get_attributes(), new_beat.motions[item.color]
                )
                new_arrow.setTransformOriginPoint(new_arrow.boundingRect().center())
                new_arrow.setPos(item.pos())
                new_arrow.setZValue(item.zValue())
                new_beat.addItem(new_arrow)
                new_beat.arrows[new_arrow.color] = new_arrow
                motion = new_beat.motions[new_arrow.color]
                new_arrow.motion = motion
                motion.arrow = new_arrow

            elif isinstance(item, Prop):
                new_prop = Prop(
                    new_beat, item.get_attributes(), new_beat.motions[item.color]
                )
                new_prop.setPos(item.pos())
                new_prop.setZValue(item.zValue())
                new_beat.addItem(new_prop)
                new_beat.props[new_prop.color] = new_prop
                motion = new_beat.motions[new_prop.color]
                new_prop.motion = motion
                motion.prop = new_prop

        for arrow in new_beat.arrows.values():
            for prop in new_beat.props.values():
                if arrow.color == prop.color:
                    arrow.prop = prop
                    prop.arrow = arrow

        for arrow in new_beat.arrows.values():
            for ghost_arrow in new_beat.ghost_arrows.values():
                if arrow.color == ghost_arrow.color:
                    arrow.ghost_arrow = ghost_arrow
                    ghost_arrow.motion = new_beat.motions[arrow.color]
                    ghost_arrow.update_attributes(arrow.get_attributes())
                    ghost_arrow.set_is_svg_mirrored_from_attributes()
                    ghost_arrow.update_mirror()
                    ghost_arrow.update_svg(arrow.svg_file)
                    ghost_arrow.update_appearance()

        for prop in new_beat.props.values():
            for ghost_prop in new_beat.ghost_props.values():
                if prop.color == ghost_prop.color:
                    prop.ghost_prop = ghost_prop
                    ghost_prop.update_prop_type(prop.prop_type)

        for ghost_arrow in new_beat.ghost_arrows.values():
            for motion in new_beat.motions.values():
                if ghost_arrow.color == motion.color:
                    ghost_arrow.motion = motion

        for ghost_prop in new_beat.ghost_props.values():
            for motion in new_beat.motions.values():
                if ghost_prop.color == motion.color:
                    ghost_prop.motion = motion

        new_beat.update_pictograph()

        return new_beat

    ### UPDATERS ###

    def update_attr_panel(self) -> None:
        for motion in self.motions.values():
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
            # check if all the motions have motion types and arrow locations
            for motion in self.motions.values():
                if motion.motion_type is None or motion.arrow_location is None:
                    return
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
