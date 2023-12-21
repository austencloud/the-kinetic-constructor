import re
from typing import Dict, Literal
from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView
import pandas as pd

from data.letter_engine_data import letter_types
from data.positions_map import get_specific_start_end_positions
from objects.arrow.arrow import Arrow
from objects.ghosts.ghost_arrow import GhostArrow
from objects.ghosts.ghost_prop import GhostProp
from objects.grid import Grid
from objects.prop.prop import Prop
from objects.motion import Motion
from constants.string_constants import (
    ARROW,
    BLUE,
    BOX,
    COLOR,
    DIAMOND,
    END_LOCATION,
    END_POSITION,
    LETTER_BTN_ICON_DIR,
    LETTERS_TRIMMED_SVG_DIR,
    MOTION_TYPE,
    PROP,
    RED,
    ROTATION_DIRECTION,
    STAFF,
    START_LOCATION,
    START_POS,
    START_POSITION,
    TURNS,
    START_ORIENTATION,
    END_ORIENTATION,
    START_LAYER,
    END_LAYER,
    ARROW_LOCATION,
)
from utilities.TypeChecking.Letters import Letters
from utilities.TypeChecking.SpecificPositions import SpecificPositions
from utilities.letter_engine import LetterEngine
from utilities.TypeChecking.TypeChecking import (
    TYPE_CHECKING,
    Colors,
    Locations,
    MotionAttributesDicts,
    List,
    Optional,
    PropTypes,
    Tuple,
)
from objects.pictograph.pictograph_event_handler import (
    PictographEventHandler,
)
from objects.pictograph.pictograph_init import PictographInit
from objects.pictograph.pictograph_menu_handler import (
    PictographMenuHandler,
)
from objects.pictograph.position_engines.arrow_positioner import ArrowPositioner
from objects.pictograph.position_engines.prop_positioner import PropPositioner


if TYPE_CHECKING:
    from widgets.main_widget import MainWidget
    from widgets.graph_editor_tab.graph_editor import GraphEditor

from objects.letter_item import LetterItem


class Pictograph(QGraphicsScene):
    def __init__(
        self,
        main_widget: "MainWidget",
        graph_type: Literal[
            "main", "option", "beat", "start_position", "ig_pictograph"
        ],
    ) -> None:
        super().__init__()
        self.main_widget = main_widget
        self.graph_type = graph_type

        self.setup_scene()
        self.setup_components(main_widget)

    def setup_scene(self) -> None:
        self.setSceneRect(0, 0, 950, 950)
        self.setBackgroundBrush(Qt.GlobalColor.white)

    def setup_components(self, main_widget: "MainWidget") -> None:
        self.arrows: Dict[Colors, Arrow] = {}
        self.props: Dict[Colors, Prop] = {}
        self.motions: Dict[Colors, Motion] = {}
        self.current_letter: Letters = None
        self.pictograph_dict: Dict = {}
        self.motion_dict_list: List[Dict] = []
        self.start_position: SpecificPositions = None
        self.end_position: SpecificPositions = None
        self.view_scale = 1
        self.event_handler = PictographEventHandler(self)

        self.dragged_arrow: Arrow = None
        self.dragged_prop: Prop = None
        self.initializer = PictographInit(self)

        self.prop_type: PropTypes = STAFF
        self.arrow_turns = 0

        self.grid: Grid = self.initializer.init_grid()

        self.view = self.init_view(self.graph_type)

        self.letter_item: LetterItem = self.initializer.init_letter_item()
        self.locations: Dict[
            Locations, Tuple[int, int, int, int]
        ] = self.initializer.init_locations(self.grid)

        self.motions: Dict[Colors, Motion] = self.initializer.init_motions()

        self.arrows: Dict[Colors, Arrow] = self.initializer.init_arrows()
        self.props: Dict[Colors, Prop] = self.initializer.init_props(self.prop_type)

        self.ghost_arrows: Dict[
            Colors, GhostArrow
        ] = self.initializer.init_ghost_arrows()
        self.ghost_props: Dict[Colors, GhostProp] = self.initializer.init_ghost_props(
            self.prop_type
        )

        self.setup_managers(main_widget)

    def init_view(self, graph_type) -> QGraphicsView:
        from widgets.graph_editor_tab.main_pictograph_view import MainPictographView
        from widgets.option_picker_tab.option import OptionView
        from widgets.sequence_widget.beat_frame.start_position import StartPositionView
        from widgets.sequence_widget.beat_frame.beat import BeatView
        from widgets.image_generator_tab.ig_pictograph import IG_Pictograph_View

        if graph_type == "main":
            view = MainPictographView(self)
        elif graph_type == "option":
            view = OptionView(self)
        elif graph_type == "beat":
            view = BeatView(self)
        elif graph_type == "start_position":
            view = StartPositionView(self)
        elif graph_type == "ig_pictograph":
            view = IG_Pictograph_View(self)
        return view

    def set_letter_renderer(self, letter: str) -> None:
        letter_type = self.get_current_letter_type()
        svg_path = f"{LETTERS_TRIMMED_SVG_DIR}/{letter_type}/{letter}.svg"
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

    def get_start_end_positions(self) -> Optional[SpecificPositions]:
        specific_positions = get_specific_start_end_positions(
            self.motions[RED], self.motions[BLUE]
        )
        if specific_positions:
            start_position = specific_positions[START_POSITION]
            end_position = specific_positions[END_POSITION]
        return start_position, end_position

    def get_state(self) -> pd.DataFrame:
        start_position = self.get_start_end_positions()[0]
        end_position = self.get_start_end_positions()[1]

        state_data = {
            "letter": self.current_letter,
            "start_position": start_position,
            "end_position": end_position,
            "blue_motion_type": None,
            "blue_rotation_direction": None,
            "blue_start_location": None,
            "blue_end_location": None,
            "blue_turns": None,
            "blue_start_orientation": None,
            "blue_end_orientation": None,
            "blue_start_layer": None,
            "blue_end_layer": None,
            "red_motion_type": None,
            "red_rotation_direction": None,
            "red_start_location": None,
            "red_end_location": None,
            "red_turns": None,
            "red_start_orientation": None,
            "red_end_orientation": None,
            "red_start_layer": None,
            "red_end_layer": None,
        }

        for motion in self.motions.values():
            color_prefix = f"{motion.color}_"
            state_data[color_prefix + "motion_type"] = motion.motion_type
            state_data[color_prefix + "rotation_direction"] = motion.rotation_direction
            state_data[color_prefix + "start_location"] = motion.start_location
            state_data[color_prefix + "end_location"] = motion.end_location
            state_data[color_prefix + "turns"] = motion.turns
            state_data[color_prefix + "start_orientation"] = motion.start_orientation
            state_data[color_prefix + "end_orientation"] = motion.end_orientation
            state_data[color_prefix + "start_layer"] = motion.start_layer
            state_data[color_prefix + "end_layer"] = motion.end_layer

        return pd.DataFrame([state_data])

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
        new_beat = self.create_new_beat()
        self.main_widget.sequence_widget.beat_frame.add_scene_to_sequence(new_beat)
        self.clear_pictograph()

    def rotate_pictograph(self, direction: str) -> None:
        for arrow in self.arrows.values():
            arrow.manipulator.rotate_arrow(direction)

    def clear_pictograph(self) -> None:
        for motion in self.motions.values():
            motion.clear_attributes()
        for arrow in self.arrows.values():
            arrow.clear_attributes()
        for prop in self.props.values():
            prop.clear_attributes()
        for ghost_arrow in self.ghost_arrows.values():
            ghost_arrow.clear_attributes()
        for ghost_prop in self.ghost_props.values():
            ghost_prop.clear_attributes()
        for item in self.items():
            if isinstance(item, Arrow) or isinstance(item, Prop):
                self.removeItem(item)
        self.update_letter()

    def clear_selections(self) -> None:
        for arrow in self.arrows.values():
            arrow.setSelected(False)
        for prop in self.props.values():
            prop.setSelected(False)
        self.dragged_prop = None
        self.dragged_arrow = None

    ### UPDATERS ###

    def update_attr_panel(self) -> None:
        for motion in self.motions.values():
            self.main_widget.graph_editor_tab.graph_editor.attr_panel.update_attr_panel(
                motion.color
            )

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
        if all(motion.motion_type for motion in self.motions.values()):
            self.current_letter = self.letter_engine.get_current_letter()
            self.set_letter_renderer(self.current_letter)
            self.letter_item.position_letter_item(self.letter_item)
        else:
            self.current_letter = None
            svg_path = f"{LETTER_BTN_ICON_DIR}/blank.svg"
            renderer = QSvgRenderer(svg_path)
            if renderer.isValid():
                self.letter_item.setSharedRenderer(renderer)

    def create_new_beat(self) -> QGraphicsScene:
        from widgets.sequence_widget.beat_frame.beat import Beat

        new_beat = Beat(self.main_widget)
        new_beat.setSceneRect(self.sceneRect())
        for motion in self.motions.values():
            new_beat.motions[motion.color] = Motion(new_beat, motion.get_attributes())
            new_arrow = Arrow(
                new_beat, motion.arrow.get_attributes(), new_beat.motions[motion.color]
            )

            new_prop = Prop(
                new_beat, motion.prop.get_attributes(), new_beat.motions[motion.color]
            )

            new_ghost_arrow = GhostArrow(
                new_beat, motion.arrow.get_attributes(), new_beat.motions[motion.color]
            )

            new_ghost_prop = GhostProp(
                new_beat, motion.prop.get_attributes(), new_beat.motions[motion.color]
            )

            new_beat.arrows[new_arrow.color] = new_arrow
            new_beat.props[new_prop.color] = new_prop

            new_beat.motions[motion.color].arrow = new_arrow
            new_beat.motions[motion.color].prop = new_prop
            new_beat.motions[motion.color].arrow.ghost = new_ghost_arrow
            new_beat.motions[motion.color].prop.ghost = new_ghost_prop

            new_beat.arrows[motion.color] = new_arrow
            new_beat.props[motion.color] = new_prop
            new_beat.ghost_arrows[motion.color] = new_ghost_arrow
            new_beat.ghost_props[motion.color] = new_ghost_prop

            if new_arrow.location:
                new_arrow.update_appearance()
                new_ghost_arrow.update_appearance()

            if new_prop.location:
                new_prop.update_appearance()
                new_ghost_prop.update_appearance()

            new_arrow.ghost = new_ghost_arrow
            new_prop.ghost = new_ghost_prop

            new_arrow.motion = new_beat.motions[motion.color]
            new_prop.motion = new_beat.motions[motion.color]
            new_ghost_arrow.motion = new_beat.motions[motion.color]
            new_ghost_prop.motion = new_beat.motions[motion.color]

            new_beat.addItem(new_arrow)
            new_beat.addItem(new_prop)
            new_beat.addItem(new_ghost_arrow)
            new_beat.addItem(new_ghost_prop)

            new_ghost_arrow.hide()
            new_ghost_prop.hide()

            motion_dict = self.motions[motion.color].get_attributes()
            motion_dict[ARROW] = new_arrow
            motion_dict[PROP] = new_prop
            motion_dict[MOTION_TYPE] = new_arrow.motion_type
            new_arrow.motion.setup_attributes(motion_dict)

        new_beat.update_pictograph()

        return new_beat
