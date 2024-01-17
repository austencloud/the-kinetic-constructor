from typing import TYPE_CHECKING

from cairo import Filter
from utilities.TypeChecking.TypeChecking import (
    LetterTypeNums,
)
from widgets.filter_frame.attr_panel.motion_type_attr_panels.Type1_motion_type_attr_panel import (
    Type1MotionTypeAttrPanel,
)
from widgets.filter_frame.filter_tab.base_filter_tab import FilterTab

if TYPE_CHECKING:
    from widgets.pictograph_scroll_area.scroll_area import (
        ScrollArea,
    )

from typing import TYPE_CHECKING


class Type1FilterTab(FilterTab):
    def __init__(self, scroll_area: "ScrollArea", letter_type: LetterTypeNums) -> None:
        super().__init__(scroll_area, letter_type)

    def setup_ui(self) -> None:
        super().setup_ui()
        self.motion_type_attr_panel = Type1MotionTypeAttrPanel(
            self.scroll_area.parent_tab
        )


class Type2FilterTab(FilterTab):
    def __init__(self, scroll_area: "ScrollArea", letter_type: LetterTypeNums) -> None:
        super().__init__(scroll_area, letter_type)


class Type3FilterTab(FilterTab):
    def __init__(self, scroll_area: "ScrollArea", letter_type: LetterTypeNums) -> None:
        super().__init__(scroll_area, letter_type)


class Type4FilterTab(FilterTab):
    def __init__(self, scroll_area: "ScrollArea", letter_type: LetterTypeNums) -> None:
        super().__init__(scroll_area, letter_type)


class Type5FilterTab(FilterTab):
    def __init__(self, scroll_area: "ScrollArea", letter_type: LetterTypeNums) -> None:
        super().__init__(scroll_area, letter_type)


class Type6FilterTab(FilterTab):
    def __init__(self, scroll_area: "ScrollArea", letter_type: LetterTypeNums) -> None:
        super().__init__(scroll_area, letter_type)
