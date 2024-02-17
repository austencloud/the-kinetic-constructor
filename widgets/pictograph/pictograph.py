from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import (
    QGraphicsScene,
    QGraphicsPixmapItem,
    QGraphicsSceneMouseEvent,
)
from Enums.Enums import (
    Letter,
    OpenCloseStates,
    SpecificPositions,
    VTG_Directions,
    VTG_Modes,
    VTG_Timings,
)
from Enums.MotionAttributes import Color, Location

from Enums.PropTypes import PropTypes
from Enums.letters import LetterType
from objects.arrow.arrow import Arrow
from objects.grid import Grid
from objects.motion.motion import Motion
from objects.prop.prop import Prop


from widgets.pictograph.components.elemental_glyph.elemental_glyph import ElementalGlyph
from widgets.pictograph.components.tka_glyph.tka_glyph import TKA_Glyph
from widgets.pictograph.components.vtg_glyph.vtg_glyph import VTG_Glyph
from widgets.sequence_widget.beat_frame.pictograph_container import PictographContainer

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
from .components.pictograph_context_menu_handler import PictographContextMenuHandler
from .components.pictograph_image_renderer import PictographImageRenderer
from .components.pictograph_updater import PictographUpdater
from .components.pictograph_event_handler import PictographMouseEventHandler
from .components.pictograph_init import PictographInit


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
    arrows: dict[Color, Arrow]
    props: dict[Color, Prop]
    motions: dict[Color, Motion]
    letter: Letter = None
    letter_type: LetterType
    pictograph_dict: dict
    motion_dict_list: list[dict]
    start_pos: SpecificPositions
    end_pos: SpecificPositions
    image_loaded: bool
    pixmap: QGraphicsPixmapItem
    arrow_turns: int
    vtg_mode: VTG_Modes = None
    vtg_timing: VTG_Timings
    vtg_dir: VTG_Directions
    vtg_glyph: VTG_Glyph
    elemental_glyph: ElementalGlyph
    open_close_state: OpenCloseStates
    dragged_arrow: Arrow
    dragged_prop: Prop
    tka_glyph: TKA_Glyph
    grid: Grid
    locations: dict[Location, tuple[int, int, int, int]]
    red_motion: Motion
    blue_motion: Motion
    red_arrow: Arrow
    blue_arrow: Arrow
    red_prop: Prop
    blue_prop: Prop
    selected_arrow: Arrow = None
    turns_tuple: str = None
    prop_type: PropTypes = None

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
        self.container = PictographContainer(self)
        self.initializer.init_all_components()
        self.arrow_placement_manager = ArrowPlacementManager(self)
        self.prop_placement_manager = PropPlacementManager(self)
        self.wasd_manager = WASD_AdjustmentManager(self)
        self.attr_manager = PictographAttrManager(self)

    ### EVENT HANDLERS ###

    def mousePressEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        self.mouse_event_handler.handle_mouse_press(event)

    def mouseMoveEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_move(event)

    def mouseReleaseEvent(self, event) -> None:
        self.mouse_event_handler.handle_mouse_release(event)

    def contextMenuEvent(self, event: "QGraphicsSceneMouseEvent") -> None:
        self.context_menu_handler.handle_context_menu(event)
