from typing import TYPE_CHECKING, List

from cairo import Filter
from utilities.TypeChecking.TypeChecking import (
    LetterTypeNums,
)
from widgets.filter_frame.attr_panel.color_attr_panel import ColorAttrPanel
from widgets.filter_frame.attr_panel.lead_state_attr_panel import LeadStateAttrPanel
from widgets.filter_frame.attr_panel.motion_type_attr_panels.Type1_motion_type_attr_panel import (
    Type1MotionTypeAttrPanel,
)
from widgets.filter_frame.filter_tab.base_filter_tab import BaseFilterTab

if TYPE_CHECKING:
    from widgets.pictograph_scroll_area.scroll_area import (
        ScrollArea,
    )

from typing import TYPE_CHECKING


class Type1FilterTab(BaseFilterTab):
    def __init__(self, scroll_area: "ScrollArea", letter_type: LetterTypeNums) -> None:
        super().__init__(scroll_area, letter_type)

    def setup_ui(self) -> None:
        super().setup_ui()
        self.motion_type_attr_panel = Type1MotionTypeAttrPanel(
            self.scroll_area.parent_tab
        )
        self.color_attr_panel = ColorAttrPanel(self.scroll_area.parent_tab)
        self.lead_state_attr_panel = LeadStateAttrPanel(self.scroll_area.parent_tab)
        self.tabs: List[
            Type1MotionTypeAttrPanel | ColorAttrPanel | LeadStateAttrPanel
        ] = [
            self.motion_type_attr_panel,
            self.color_attr_panel,
            self.lead_state_attr_panel,
        ]


class Type2FilterTab(BaseFilterTab):
    def __init__(self, scroll_area: "ScrollArea", letter_type: LetterTypeNums) -> None:
        super().__init__(scroll_area, letter_type)


class Type3FilterTab(BaseFilterTab):
    def __init__(self, scroll_area: "ScrollArea", letter_type: LetterTypeNums) -> None:
        super().__init__(scroll_area, letter_type)


class Type4FilterTab(BaseFilterTab):
    def __init__(self, scroll_area: "ScrollArea", letter_type: LetterTypeNums) -> None:
        super().__init__(scroll_area, letter_type)


class Type5FilterTab(BaseFilterTab):
    def __init__(self, scroll_area: "ScrollArea", letter_type: LetterTypeNums) -> None:
        super().__init__(scroll_area, letter_type)


class Type6FilterTab(BaseFilterTab):
    def __init__(self, scroll_area: "ScrollArea", letter_type: LetterTypeNums) -> None:
        super().__init__(scroll_area, letter_type)
