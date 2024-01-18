from typing import TYPE_CHECKING, List

from utilities.TypeChecking.TypeChecking import (
    LetterTypeNums,
)
from ..attr_panel.color_attr_panel import ColorAttrPanel
from ..attr_panel.lead_state_attr_panel import LeadStateAttrPanel
from ..attr_panel.motion_type_attr_panel import MotionTypeAttrPanel
from .base_filter_tab import BaseFilterTab

if TYPE_CHECKING:
    from ..pictograph_scroll_area.scroll_area import (
        ScrollArea,
    )

from typing import TYPE_CHECKING
from constants import COLOR, LEAD_STATE, MOTION_TYPE, PRO, ANTI
from data.letter_engine_data import motion_type_letter_combinations
from utilities.TypeChecking.TypeChecking import (
    LetterTypeNums,
    Letters,
    MotionAttributes,
)


class Type1FilterTab(BaseFilterTab):
    def __init__(self, scroll_area: "ScrollArea", letter_type: LetterTypeNums) -> None:
        super().__init__(scroll_area, letter_type)

    def setup_ui(self) -> None:
        super().setup_ui()
        self._setup_tabs()

    def _setup_tabs(self) -> None:
        self.motion_type_attr_panel = MotionTypeAttrPanel(
            self.scroll_area.parent_tab, [PRO, ANTI]
        )
        self.color_attr_panel = ColorAttrPanel(self.scroll_area.parent_tab)
        self.lead_state_attr_panel = LeadStateAttrPanel(self.scroll_area.parent_tab)
        self.tabs: List[MotionTypeAttrPanel | ColorAttrPanel | LeadStateAttrPanel] = [
            self.motion_type_attr_panel,
            self.color_attr_panel,
            self.lead_state_attr_panel,
        ]

    def show_tabs_based_on_chosen_letters(self) -> None:
        selected_letters_that_match_section_type: set[Letters] = set()

        for letter in self.scroll_area.parent_tab.selected_letters:
            selected_letters_that_match_section_type.add(letter)

        tabs_to_show = self._determine_tabs_to_show(
            selected_letters_that_match_section_type
        )
        tabs_to_hide = self._determine_tabs_to_hide(tabs_to_show)

        self.show_tabs(tabs_to_show)
        self.hide_tabs(tabs_to_hide)

        if tabs_to_show:
            self.setCurrentIndex(
                self.indexOf(getattr(self, f"{tabs_to_show[0].lower()}_attr_panel"))
            )
        self.resize_filter_tab()

    def _determine_tabs_to_show(
        self, selected_letters: set[Letters]
    ) -> List[MotionAttributes]:
        tabs_to_show: List[MotionAttributes] = []
        motion_types_present = set()

        for letter in selected_letters:
            motion_types_present.update(motion_type_letter_combinations[letter])

        if motion_types_present == {PRO} or motion_types_present == {ANTI}:
            tabs_to_show.append(COLOR)
        elif len(motion_types_present) > 1:
            tabs_to_show.extend([MOTION_TYPE, COLOR])
        if selected_letters.intersection(["S", "T", "U", "V"]):
            tabs_to_show.append(LEAD_STATE)

        return tabs_to_show

    def _determine_tabs_to_hide(
        self, tabs_to_show: List[MotionAttributes]
    ) -> List[MotionAttributes]:
        tabs = [MOTION_TYPE, COLOR, LEAD_STATE]
        tabs_to_hide: List[MotionAttributes] = []

        for tab in tabs:
            if tab not in tabs_to_show:
                tabs_to_hide.append(tab)

        return tabs_to_hide
