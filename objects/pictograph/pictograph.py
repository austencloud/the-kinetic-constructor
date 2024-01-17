from typing import TYPE_CHECKING, Dict, List, Literal, Optional, Tuple, Union
from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from Enums import LetterNumberType

from constants import *
from objects.pictograph.pictograph_image_renderer import PictographImageRenderer
from objects.pictograph.pictograph_state_updater import PictographStateUpdater

from ..arrow.arrow_placement_manager.main_arrow_placement_manager import (
    ArrowPlacementManager,
)
from utilities.TypeChecking.prop_types import (
    strictly_placed_props,
    non_strictly_placed_props,
)
from utilities.TypeChecking.letter_lists import all_letters
from utilities.TypeChecking.TypeChecking import Colors, LetterTypeNums, Locations, SpecificPositions

from utilities.letter_item import LetterItem
from ..motion.motion import Motion
from ..prop.prop import Prop
from ..arrow.arrow import Arrow
from ..arrow.ghost_arrow import GhostArrow
from ..prop.ghost_prop import GhostProp
from ..grid import Grid

from .pictograph_event_handler import PictographEventHandler
from .pictograph_init import PictographInit
from .pictograph_menu_handler import PictographMenuHandler
from .position_engines.prop_positioners.main_prop_positioner import (
    PropPlacementManager,
)
from utilities.letter_engine import LetterEngine
from data.rules import beta_ending_letters, alpha_ending_letters, gamma_ending_letters

if TYPE_CHECKING:
    from widgets.ig_tab.ig_scroll.ig_pictograph import IGPictograph
    from widgets.option_picker_tab.option import Option
    from widgets.main_widget import MainWidget


class Pictograph(QGraphicsScene):
    def __init__(
        self,
        main_widget: "MainWidget",
        graph_type: Literal[
            "main",
            "option",
            "beat",
            "start_pos_beat",
            "ig_pictograph",
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
        self.ghost_arrows: Dict[Colors, GhostArrow] = {}
        self.ghost_props: Dict[Colors, GhostProp] = {}
        self.motions: Dict[Colors, Motion] = {}
        self.letter: all_letters = None
        self.letter_type: LetterTypeNums = None
        self.pictograph_dict: Dict = {}
        self.motion_dict_list: List[Dict] = []
        self.start_pos: SpecificPositions = None
        self.end_pos: SpecificPositions = None
        self.image_loaded: bool = False
        self.pixmap: QGraphicsPixmapItem = None
        self.pictograph_dict = None
        self.arrow_turns = 0
        self.vtg_timing = None
        self.vtg_dir = None
        self.dragged_arrow: Arrow = None
        self.dragged_prop: Prop = None
        self.initializer = PictographInit(self)
        self.event_handler = PictographEventHandler(self)
        self.state_updater = PictographStateUpdater(self)
        self.image_renderer = PictographImageRenderer(self)

        self.grid: Grid = self.initializer.init_grid()
        self.locations: Dict[
            Locations, Tuple[int, int, int, int]
        ] = self.initializer.init_quadrant_boundaries(self.grid)

        self.motions: Dict[Colors, Motion] = self.initializer.init_motions()
        self.red_motion, self.blue_motion = self.motions[RED], self.motions[BLUE]
        self.arrows, self.ghost_arrows = self.initializer.init_arrows()
        self.red_arrow, self.blue_arrow = self.arrows[RED], self.arrows[BLUE]
        self.props, self.ghost_props = self.initializer.init_props(
            self.main_widget.prop_type
        )
        self.red_prop, self.blue_prop = self.props[RED], self.props[BLUE]

        self.view = self._init_view(self.graph_type)
        self.letter_item: LetterItem = self.initializer.init_letter_item()

        self._setup_managers(main_widget)

    def _init_view(self, graph_type) -> QGraphicsView:
        from widgets.graph_editor_tab.graph_editor_pictograph_view import (
            GraphEditorPictographView,
        )
        from widgets.option_picker_tab.option import OptionView
        from widgets.sequence_widget.beat_frame.start_pos_beat import (
            StartPositionBeatView,
        )
        from widgets.sequence_widget.beat_frame.beat import BeatView
        from widgets.ig_tab.ig_scroll.ig_pictograph import IG_Pictograph_View

        if graph_type == MAIN:
            view = GraphEditorPictographView(self)
        elif graph_type == OPTION:
            view = OptionView(self)
        elif graph_type == BEAT:
            view = BeatView(self)
        elif graph_type == START_POS_BEAT:
            view = StartPositionBeatView(self)
        elif graph_type == IG_PICTOGRAPH:
            view = IG_Pictograph_View(self)
        return view

    def _set_letter_renderer(self, letter: str) -> None:
        letter_type = self._get_letter_type(letter)
        svg_path = f"resources/images/letters_trimmed/{letter_type}/{letter}.svg"
        renderer = QSvgRenderer(svg_path)
        if renderer.isValid():
            self.letter_item.setSharedRenderer(renderer)

    def _setup_managers(self, main_widget: "MainWidget") -> None:
        self.pictograph_menu_handler = PictographMenuHandler(main_widget, self)
        self.arrow_placement_manager = ArrowPlacementManager(self)
        self.prop_placement_manager = PropPlacementManager(self)
        self.letter_engine = LetterEngine(self)

    def _create_motion_dict(
        self: Union["Option", "IGPictograph"], pictograph_dict: Dict, color: Colors
    ) -> Dict:
        motion_dict = {
            COLOR: color,
            MOTION_TYPE: pictograph_dict.get(f"{color}_motion_type"),
            PROP_ROT_DIR: pictograph_dict.get(f"{color}_prop_rot_dir"),
            START_LOC: pictograph_dict.get(f"{color}_start_loc"),
            END_LOC: pictograph_dict.get(f"{color}_end_loc"),
            TURNS: pictograph_dict.get(f"{color}_turns"),
            START_ORI: pictograph_dict.get(f"{color}_start_ori"),
        }
        return {k: v for k, v in motion_dict.items() if v != None}

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

    def _get_letter_type(self, letter: all_letters) -> Optional[str]:
        for letter_type in LetterNumberType:
            if letter in letter_type.letters:
                return letter_type.description
        return None

    def get_closest_hand_point(
        self, pos: QPointF
    ) -> Tuple[Optional[str], Optional[QPointF]]:
        min_distance = float("inf")
        nearest_point_name = None
        nearest_point_coords = None
        if self.main_widget.prop_type in strictly_placed_props:
            strict = True
        elif self.main_widget.prop_type in non_strictly_placed_props:
            strict = False
        if self.grid.grid_mode == DIAMOND:
            if strict is True:
                for name, point in self.grid.circle_coordinates_cache["hand_points"][
                    self.grid.grid_mode
                ]["strict"].items():
                    distance = (pos - point).manhattanLength()
                    if distance < min_distance:
                        min_distance = distance
                        nearest_point_name = name
                        nearest_point_coords = point
            elif strict is False:
                for name, point in self.grid.circle_coordinates_cache["hand_points"][
                    self.grid.grid_mode
                ]["normal"].items():
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

    def get_motions_by_type(self, motion_type: str) -> List[Motion]:
        return [
            motion
            for motion in self.motions.values()
            if motion.motion_type == motion_type
        ]

    def get_leading_motion(self) -> Motion:
        if self.red_motion.start_loc == self.blue_motion.end_loc:
            return self.red_motion
        elif self.blue_motion.start_loc == self.red_motion.end_loc:
            return self.blue_motion

    def get_trailing_motion(self) -> Motion:
        if self.red_motion.start_loc == self.blue_motion.end_loc:
            return self.blue_motion
        elif self.blue_motion.start_loc == self.red_motion.end_loc:
            return self.red_motion

    def get_other_motion(self, motion: Motion) -> Motion:
        if motion.color == RED:
            return self.blue_motion
        elif motion.color == BLUE:
            return self.red_motion

    def get_other_arrow(self, arrow: Arrow) -> Arrow:
        if arrow.color == RED:
            return self.blue_arrow
        elif arrow.color == BLUE:
            return self.red_arrow

    ### HELPERS ###

    def select_arrow(self, arrow) -> None:
        self.selected_arrow: Arrow = arrow

    def add_to_sequence_callback(self) -> None:
        new_beat = self.create_new_beat()
        self.main_widget.sequence_widget.beat_frame.add_scene_to_sequence(new_beat)
        self.clear_pictograph()

    def rotate_pictograph(self, direction: str) -> None:
        for motion in self.motions.values():
            motion.manipulator.rotate_motion(direction)

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
        self._update_letter()

    def clear_selections(self) -> None:
        for arrow in self.arrows.values():
            arrow.setSelected(False)
        for prop in self.props.values():
            prop.setSelected(False)
        self.dragged_prop = None
        self.dragged_arrow = None

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

            if new_arrow.loc:
                new_arrow.update_arrow()
                new_ghost_arrow.update_arrow()

            if new_prop.loc:
                new_prop.update_prop()
                new_ghost_prop.update_prop()

            new_arrow.ghost = new_ghost_arrow
            new_prop.ghost = new_ghost_prop

            new_arrow.motion = new_beat.motions[motion.color]
            new_prop.motion = new_beat.motions[motion.color]
            new_ghost_arrow.motion = new_beat.motions[motion.color]
            new_ghost_prop.motion = new_beat.motions[motion.color]

            new_ghost_arrow.hide()
            new_ghost_prop.hide()

            motion_dict = self.motions[motion.color].get_attributes()
            motion_dict[ARROW] = new_arrow
            motion_dict[PROP] = new_prop
            motion_dict[MOTION_TYPE] = new_arrow.motion_type
            new_arrow.turns = motion_dict[TURNS]
            new_arrow.motion.update_motion(motion_dict)

            new_arrow.setTransformOriginPoint(new_arrow.boundingRect().center())
            new_arrow.ghost.setTransformOriginPoint(
                new_arrow.ghost.boundingRect().center()
            )
            new_arrow.update_arrow()
        new_beat.update_pictograph()

        return new_beat


    ### BOOLS ###

    def is_pictograph_dict_complete(self, pictograph_dict: Dict) -> bool:
        required_keys = [
            "letter",
            "start_pos",
            "end_pos",
            "blue_motion_type",
            "blue_prop_rot_dir",
            "blue_start_loc",
            "blue_end_loc",
            "blue_start_ori",
            "blue_turns",
            "red_motion_type",
            "red_prop_rot_dir",
            "red_start_loc",
            "red_end_loc",
            "red_start_ori",
            "red_turns",
        ]
        return all(key in pictograph_dict for key in required_keys)

    def _meets_filter_criteria(self, filters) -> bool:
        blue_turns = str(self.motions[BLUE].turns)
        red_turns = str(self.motions[RED].turns)
        return blue_turns in filters[BLUE_TURNS] and red_turns in filters[RED_TURNS]

    def has_props_in_beta(self) -> bool:
        return self.letter in beta_ending_letters

    def has_props_in_alpha(self) -> bool:
        return self.letter in alpha_ending_letters

    def has_props_in_gamma(self) -> bool:
        return self.letter in gamma_ending_letters

    def has_hybrid_orientations(self) -> bool:
        red_prop, blue_prop = self.props[RED], self.props[BLUE]
        return red_prop.is_radial() != blue_prop.is_radial()

    def has_non_hybrid_orientations(self) -> bool:
        red_prop, blue_prop = self.props[RED], self.props[BLUE]
        return (red_prop.is_radial() == blue_prop.is_radial()) or (
            red_prop.is_antiradial() and blue_prop.is_antiradial()
        )

    def has_all_radial_props(self) -> bool:
        return all(prop.is_radial() for prop in self.props.values())

    def has_all_antiradial_props(self) -> bool:
        return all(prop.is_antiradial() for prop in self.props.values())

    def has_a_dash(self) -> bool:
        for motion in self.motions.values():
            if motion.motion_type == DASH:
                return True
        return False

    def has_a_static_motion(self) -> bool:
        for motion in self.motions.values():
            if motion.motion_type == STATIC:
                return True
        return False


