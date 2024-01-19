from typing import TYPE_CHECKING, Dict, List, Tuple
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsPixmapItem

from objects.arrow.arrow import Arrow
from objects.arrow.arrow_placement_manager.managers.main_arrow_placement_manager import (
    ArrowPlacementManager,
)
from objects.arrow.ghost_arrow import GhostArrow
from objects.grid import Grid
from objects.motion.motion import Motion
from objects.prop.ghost_prop import GhostProp
from objects.prop.prop import Prop
from objects.prop.prop_placement_manager.prop_placement_manager import (
    PropPlacementManager,
)
from utilities.TypeChecking.TypeChecking import (
    Colors,
    LetterTypeNums,
    Letters,
    Locations,
    SpecificPositions,
    VtgDirections,
    VtgTimings,
)
from widgets.pictograph.pictograph_attr_manager import PictographAttrManager
from widgets.pictograph.pictograph_checker import PictographChecker
from widgets.pictograph.pictograph_getter import PictographGetter
from widgets.pictograph.pictograph_view import PictographView
from widgets.pictograph.wasd_adjustment_manager.wasd_adjustment_manager import (
    WASD_AdjustmentManager,
)
from .pictograph_add_to_sequence_manager import AddToSequenceManager
from .pictograph_context_menu_handler import PictographContextMenuHandler
from .pictograph_image_renderer import PictographImageRenderer
from .pictograph_state_updater import PictographStateUpdater
from .pictograph_event_handler import PictographMouseEventHandler
from .pictograph_init import PictographInit
from utilities.letter_item import LetterItem
from utilities.letter_engine import LetterCalculator

if TYPE_CHECKING:
    from widgets.scroll_area.scroll_area import ScrollArea
    from widgets.main_widget.main_widget import MainWidget


class Pictograph(QGraphicsScene):
    
    
    def __init__(self, main_widget: "MainWidget", scroll_area: "ScrollArea") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.scroll_area = scroll_area
        self.initializer = PictographInit(self)
        self.mouse_event_handler = PictographMouseEventHandler(self)
        self.context_menu_handler = PictographContextMenuHandler(self)
        self.state_updater = PictographStateUpdater(self)
        self.image_renderer = PictographImageRenderer(self)
        self.add_to_sequence_manager = AddToSequenceManager(self)
        self.wasd_adjustment_manager = WASD_AdjustmentManager(self)
        self.get = PictographGetter(self)
        self.check = PictographChecker(self)
        self.view = PictographView(self)
        self.initializer.init_all_components()
        self.arrow_placement_manager = ArrowPlacementManager(self)
        self.prop_placement_manager = PropPlacementManager(self)
        self.letter_calculator = LetterCalculator(self)
        self.attr_manager = PictographAttrManager(self)

    ### EVENT HANDLERS ###

    def mousePressEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_press(event)

    def mouseMoveEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_move(event)

    def mouseReleaseEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_release(event)

    def contextMenuEvent(self, event) -> None:
        self.context_menu_handler.handle_context_menu(event)


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
    selected_arrow: Arrow
