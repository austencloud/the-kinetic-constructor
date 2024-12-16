from typing import TYPE_CHECKING, Union
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsTextItem
from Enums.Enums import Letter, OpenCloseStates, VTG_Modes
from Enums.MotionAttributes import Location
from Enums.PropTypes import PropType
from Enums.letters import LetterType
from base_widgets.base_pictograph.bordered_pictograph_view import BorderedPictographView
from main_window.main_widget.learn_widget.base_classes.base_lesson_widget.lesson_pictograph_view import (
    LessonPictographView,
)

from main_window.main_widget.learn_widget.codex_widget.codex_pictograph_view import CodexPictographView
from main_window.main_widget.sequence_builder.start_pos_picker.start_pos_picker_pictograph_view import (
    StartPosPickerPictographView,
)

from main_window.main_widget.sequence_widget.beat_frame.reversal_symbol_manager import (
    ReversalSymbolManager,
)
from objects.arrow.arrow import Arrow
from objects.grid import Grid
from objects.motion.motion import Motion
from objects.prop.prop import Prop
from placement_managers.arrow_placement_manager.arrow_placement_manager import (
    ArrowPlacementManager,
)
from placement_managers.prop_placement_manager.prop_placement_manager import (
    PropPlacementManager,
)
from .elemental_glyph.elemental_glyph import ElementalGlyph
from .start_to_end_pos_glyph.start_to_end_pos_glyph import StartToEndPosGlyph
from .tka_glyph.tka_glyph import TKA_Glyph
from .vtg_glyph.vtg_glyph import VTG_Glyph
from .pictograph_attr_manager import PictographAttrManager
from .pictograph_checker import PictographChecker
from .pictograph_getter import PictographGetter
from .pictograph_view import PictographView
from .wasd_adjustment_manager.wasd_adjustment_manager import WASD_AdjustmentManager
from .pictograph_image_renderer import PictographImageRenderer
from .pictograph_updater import PictographUpdater
from .pictograph_initializer import PictographInitializer


if TYPE_CHECKING:
    from main_window.main_widget.main_widget import MainWidget


class BasePictograph(QGraphicsScene):
    view: Union[
        PictographView,
        BorderedPictographView,
        LessonPictographView,
        StartPosPickerPictographView,
        CodexPictographView,
    ]
    arrows: dict[str, Arrow]
    props: dict[str, Prop]
    motions: dict[str, Motion]
    letter: Letter = None
    letter_type: LetterType = None
    pictograph_dict: dict
    motion_dict_list: list[dict]
    start_pos: str
    end_pos: str
    image_loaded: bool
    pixmap: QGraphicsPixmapItem
    arrow_turns: int
    vtg_mode: VTG_Modes = None
    timing: str
    direction: str
    vtg_glyph: VTG_Glyph
    elemental_glyph: ElementalGlyph
    open_close_state: OpenCloseStates
    dragged_arrow: Arrow
    dragged_prop: Prop
    tka_glyph: TKA_Glyph
    start_to_end_pos_glyph: StartToEndPosGlyph
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
    prop_type: PropType = None
    is_blank: bool = False
    disable_gold_overlay: bool = False
    quiz_mode: bool = False
    blue_reversal = False
    blue_reversal_symbol: "QGraphicsTextItem" = None
    red_reversal = False
    red_reversal_symbol: "QGraphicsTextItem" = None
    # styled_border_overlay: "StyledBorderOverlay"

    def __init__(self, main_widget: "MainWidget") -> None:
        super().__init__()
        self.main_widget = main_widget
        self.initializer = PictographInitializer(self)
        self.updater = PictographUpdater(self)
        self.image_renderer = PictographImageRenderer(self)
        self.get = PictographGetter(self)
        self.check = PictographChecker(self)
        self.arrow_placement_manager = ArrowPlacementManager(self)
        self.wasd_manager = WASD_AdjustmentManager(self)
        self.initializer.init_all_components()
        self.prop_placement_manager = PropPlacementManager(self)
        self.attr_manager = PictographAttrManager(self)
        self.reversal_symbol_manager = ReversalSymbolManager(self)
