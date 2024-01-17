from typing import TYPE_CHECKING, List

from utilities.TypeChecking.TypeChecking import (
    LetterTypeNums,
)
from ..attr_panel.color_attr_panel import ColorAttrPanel
from ..attr_panel.lead_state_attr_panel import LeadStateAttrPanel
from ..attr_panel.motion_type_attr_panels.Type2_motion_type_attr_panel import (
    Type2MotionTypeAttrPanel,
)
from .base_filter_tab import BaseFilterTab

if TYPE_CHECKING:
    from ..pictograph_scroll_area.scroll_area import (
        ScrollArea,
    )

from typing import TYPE_CHECKING
from constants import COLOR, LEAD_STATE, MOTION_TYPE, PRO, ANTI, STATIC, DASH
from data.letter_engine_data import motion_type_letter_combinations
from utilities.TypeChecking.TypeChecking import (
    LetterTypeNums,
    Letters,
    MotionAttributes,
)
from utilities.TypeChecking.letter_lists import (
    Type1_letters,
    Type2_letters,
    Type3_letters,
    Type4_letters,
    Type5_letters,
    Type6_letters,
)



class Type2FilterTab(BaseFilterTab):
    def __init__(self, scroll_area: "ScrollArea", letter_type: LetterTypeNums) -> None:
        super().__init__(scroll_area, letter_type)

    def setup_ui(self) -> None:
        super().setup_ui()
        self.motion_type_attr_panel = Type2MotionTypeAttrPanel(
            self.scroll_area.parent_tab
        )
        self.color_attr_panel = ColorAttrPanel(self.scroll_area.parent_tab)
        self.tabs: List[Type2MotionTypeAttrPanel | ColorAttrPanel] = [
            self.motion_type_attr_panel,
            self.color_attr_panel,
        ]
