from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import (
    QGraphicsScene,
    QGraphicsPixmapItem,
    QGraphicsSceneMouseEvent,
    QGraphicsDropShadowEffect,
)
from PyQt6.QtGui import QColor
from Enums import LetterType

from objects.arrow.arrow import Arrow
from objects.grid import Grid
from objects.motion.motion import Motion
from objects.prop.prop import Prop

from utilities.TypeChecking.TypeChecking import (
    Letters,
    OpenCloseStates,
    SpecificPositions,
    VtgDirections,
    VtgTimings,
)
from utilities.TypeChecking.MotionAttributes import Colors, Locations
from widgets.pictograph.components.pictograph_frame_styler import PictographFrameStyler

from .components.glyph.glyph import GlyphManager
from .components.pictograph_attr_manager import PictographAttrManager
from .components.pictograph_checker import PictographChecker
from .components.pictograph_getter import PictographGetter
from .components.placement_managers.arrow_placement_manager.arrow_placement_manager import (
    ArrowPlacementManager,
)
from .components.placement_managers.prop_placement_manager.prop_placement_manager import (
    PropPlacementManager,
)
from .components.pictograph_view import PictographView
from .components.wasd_adjustment_manager.wasd_adjustment_manager import (
    WASD_AdjustmentManager,
)
from .components.add_to_sequence_manager import AddToSequenceManager
from .components.pictograph_context_menu_handler import PictographContextMenuHandler
from .components.pictograph_image_renderer import PictographImageRenderer
from .components.pictograph_updater import PictographUpdater
from .components.pictograph_event_handler import PictographMouseEventHandler
from .components.pictograph_init import PictographInit

from archive.dataframe_generators.letter_calculator import LetterCalculator

if TYPE_CHECKING:
    from ..sequence_builder.components.start_position_picker.start_pos_picker_scroll_area import (
        StartPosPickerScrollArea,
    )
    from ..sequence_builder.components.option_picker.option_picker_scroll_area import (
        OptionPickerScrollArea,
    )
    from ..scroll_area.codex_scroll_area import CodexScrollArea
    from ..main_widget.main_widget import MainWidget


class Pictograph(QGraphicsScene):
    view: PictographView
    arrows: dict[Colors, Arrow]
    props: dict[Colors, Prop]
    motions: dict[Colors, Motion]
    letter: Letters = None
    letter_type: LetterType
    pictograph_dict: dict
    motion_dict_list: list[dict]
    start_pos: SpecificPositions
    end_pos: SpecificPositions
    image_loaded: bool
    pixmap: QGraphicsPixmapItem
    arrow_turns: int
    vtg_timing: VtgTimings
    vtg_dir: VtgDirections
    open_close_state: OpenCloseStates
    dragged_arrow: Arrow
    dragged_prop: Prop
    glyph: GlyphManager
    grid: Grid
    locations: dict[Locations, tuple[int, int, int, int]]
    red_motion: Motion
    blue_motion: Motion
    red_arrow: Arrow
    blue_arrow: Arrow
    red_prop: Prop
    blue_prop: Prop
    selected_arrow: Arrow = None

    def __init__(
        self,
        main_widget: "MainWidget",
        scroll_area=None,
    ) -> None:
        super().__init__()
        self.main_widget = main_widget
        self.scroll_area: Union[
            CodexScrollArea, OptionPickerScrollArea, StartPosPickerScrollArea
        ] = scroll_area
        self.initializer = PictographInit(self)
        self.mouse_event_handler = PictographMouseEventHandler(self)
        self.context_menu_handler = PictographContextMenuHandler(self)
        self.updater = PictographUpdater(self)
        self.image_renderer = PictographImageRenderer(self)
        self.get = PictographGetter(self)
        self.check = PictographChecker(self)
        self.view = PictographView(self)
        self.initializer.init_all_components()
        self.arrow_placement_manager = ArrowPlacementManager(self)
        self.prop_placement_manager = PropPlacementManager(self)
        self.wasd_manager = WASD_AdjustmentManager(self)
        self.attr_manager = PictographAttrManager(self)
        self.frame_styler = PictographFrameStyler(self)


    ### EVENT HANDLERS ###

    def mousePressEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        self.mouse_event_handler.handle_mouse_press(event)

    def mouseMoveEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_move(event)

    def mouseReleaseEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_release(event)

    def contextMenuEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        self.context_menu_handler.handle_context_menu(event)
