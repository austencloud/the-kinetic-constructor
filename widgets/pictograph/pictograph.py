from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from Enums.Enums import Letter, OpenCloseStates, SpecificPosition, VTG_Modes
from Enums.MotionAttributes import Location

from Enums.PropTypes import PropType
from Enums.letters import LetterType
from objects.arrow.arrow import Arrow
from objects.grid import Grid
from objects.motion.motion import Motion
from objects.prop.prop import Prop


from .components.elemental_glyph.elemental_glyph import ElementalGlyph
from .components.start_to_end_pos_glyph.start_to_end_pos_glyph import (
    StartToEndPosGlyph,
)
from .components.tka_glyph.tka_glyph import TKA_Glyph
from .components.vtg_glyph.vtg_glyph import VTG_Glyph
from .components.pictograph_container import (
    PictographContainer,
)

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
from .components.pictograph_image_renderer import PictographImageRenderer
from .components.pictograph_updater import PictographUpdater
from .components.pictograph_initializer import PictographInitializer


if TYPE_CHECKING:
    from widgets.sequence_builder.option_picker.option_picker_scroll_area.option_picker_scroll_area import (
        OptionPickerScrollArea,
    )

    from main_window.main_widget.main_widget import MainWidget


class Pictograph(QGraphicsScene):
    view: PictographView
    arrows: dict[str, Arrow]
    props: dict[str, Prop]
    motions: dict[str, Motion]
    letter: Letter = None
    letter_type: LetterType = None
    pictograph_dict: dict
    motion_dict_list: list[dict]
    start_pos: SpecificPosition
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

    def __init__(
        self,
        main_widget: "MainWidget",
        scroll_area=None,
    ) -> None:
        super().__init__()
        self.main_widget = main_widget
        self.scroll_area: OptionPickerScrollArea = scroll_area
        self.initializer = PictographInitializer(self)
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
