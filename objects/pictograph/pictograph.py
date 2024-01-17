from typing import TYPE_CHECKING, Dict, List, Literal, Optional, Tuple
from PyQt6.QtCore import Qt
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsPixmapItem
from Enums import LetterNumberType

from constants import *
from objects.pictograph.pictograph_add_to_sequence_manager import AddToSequenceManager
from objects.pictograph.pictograph_context_menu_handler import (
    PictographContextMenuHandler,
)
from objects.pictograph.pictograph_image_renderer import PictographImageRenderer
from objects.pictograph.pictograph_state_updater import PictographStateUpdater

from ..arrow.arrow_placement_manager.main_arrow_placement_manager import (
    ArrowPlacementManager,
)
from utilities.TypeChecking.letter_lists import all_letters
from utilities.TypeChecking.TypeChecking import (
    Colors,
    LetterTypeNums,
    Letters,
    Locations,
    SpecificPositions,
    VtgDirections,
    VtgTimings,
)

from utilities.letter_item import LetterItem
from ..motion.motion import Motion
from ..prop.prop import Prop
from ..arrow.arrow import Arrow
from ..arrow.ghost_arrow import GhostArrow
from ..prop.ghost_prop import GhostProp
from ..grid import Grid

from .pictograph_event_handler import PictographMouseEventHandler
from .pictograph_init import PictographInit
from .position_engines.prop_positioners.main_prop_positioner import PropPlacementManager
from utilities.letter_engine import LetterEngine
from data.rules import beta_ending_letters, alpha_ending_letters, gamma_ending_letters

if TYPE_CHECKING:
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

        self.initializer = PictographInit(self)
        self.mouse_event_handler = PictographMouseEventHandler(self)
        self.context_menu_handler = PictographContextMenuHandler(self)
        self.state_updater = PictographStateUpdater(self)
        self.image_renderer = PictographImageRenderer(self)
        self.add_to_sequence_manager = AddToSequenceManager(self)

        self.initializer.init_all_components()
        self.arrow_placement_manager = ArrowPlacementManager(self)
        self.prop_placement_manager = PropPlacementManager(self)
        self.letter_engine = LetterEngine(self)
        self.setup_scene()

    def setup_scene(self) -> None:
        self.setSceneRect(0, 0, 950, 950)
        self.setBackgroundBrush(Qt.GlobalColor.white)

    def _set_letter_renderer(self, letter: str) -> None:
        letter_type = self._get_letter_type(letter)
        svg_path = f"resources/images/letters_trimmed/{letter_type}/{letter}.svg"
        renderer = QSvgRenderer(svg_path)
        if renderer.isValid():
            self.letter_item.setSharedRenderer(renderer)

    ### EVENT HANDLERS ###

    def mousePressEvent(self, event) -> None:
        self.main_widget.deselect_all_except(self)
        self.mouse_event_handler.handle_mouse_press(event)

    def mouseMoveEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_move(event)

    def mouseReleaseEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_release(event)

    def contextMenuEvent(self, event) -> None:
        self.context_menu_handler.handle_context_menu(event)

    ### GETTERS ###

    def _get_letter_type(self, letter: all_letters) -> Optional[str]:
        for letter_type in LetterNumberType:
            if letter in letter_type.letters:
                return letter_type.description
        return None

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

    def generate_pictograph_dict_from_attributes(self) -> Dict:
        pictograph_dict = {
            "letter": self.letter,
            "start_pos": self.start_pos,
            "end_pos": self.end_pos,
            "blue_motion_type": self.blue_motion.motion_type,
            "blue_prop_rot_dir": self.blue_motion.prop_rot_dir,
            "blue_start_loc": self.blue_motion.start_loc,
            "blue_end_loc": self.blue_motion.end_loc,
            "blue_start_ori": self.blue_motion.start_ori,
            "blue_turns": self.blue_motion.turns,
            "red_motion_type": self.red_motion.motion_type,
            "red_prop_rot_dir": self.red_motion.prop_rot_dir,
            "red_start_loc": self.red_motion.start_loc,
            "red_end_loc": self.red_motion.end_loc,
            "red_start_ori": self.red_motion.start_ori,
            "red_turns": self.red_motion.turns,
        }
        return pictograph_dict

    ### HELPERS ###

    def show(self):
        self.view.setVisible(True)

    def hide(self):
        self.view.setVisible(False)

    def select_arrow(self, arrow) -> None:
        self.selected_arrow: Arrow = arrow

    def rotate_pictograph(self, direction: str) -> None:
        for motion in self.motions.values():
            motion.manipulator.rotate_motion(direction)

    def clear_selections(self) -> None:
        for arrow in self.arrows.values():
            arrow.setSelected(False)
        for prop in self.props.values():
            prop.setSelected(False)
        self.dragged_prop = None
        self.dragged_arrow = None

    ### BOOLS ###

    def is_view_visible(self) -> bool:
        return self.view.isVisible()

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

    arrows: Dict[Colors, Arrow]
    props: Dict[Colors, Prop]
    ghost_arrows: Dict[Colors, GhostArrow]
    ghost_props: Dict[Colors, GhostProp]
    motions: Dict[Colors, Motion]
    letter: Letters
    letter_type: LetterTypeNums
    pictograph_dict: Dict
    motion_dict_list: List[Dict]
    start_pos: SpecificPositions
    end_pos: SpecificPositions
    image_loaded: bool
    pixmap: QGraphicsPixmapItem
    arrow_turns: int
    vtg_timing: VtgTimings
    vtg_dir: VtgDirections
    dragged_arrow: Arrow
    dragged_prop: Prop
    view: QGraphicsView
    letter_item: LetterItem
    grid: Grid
    locations: Dict[Locations, Tuple[int, int, int, int]]
    red_motion: Motion
    blue_motion: Motion
    red_arrow: Arrow
    blue_arrow: Arrow
    red_prop: Prop
    blue_prop: Prop
