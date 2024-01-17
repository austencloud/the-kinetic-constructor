from typing import TYPE_CHECKING, List

from utilities.TypeChecking.TypeChecking import (
    LetterTypeNums,
)
from ..attr_panel.color_attr_panel import ColorAttrPanel
from ..attr_panel.lead_state_attr_panel import LeadStateAttrPanel
from ..attr_panel.motion_type_attr_panels.Type1_motion_type_attr_panel import (
    Type1MotionTypeAttrPanel,
)
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
from utilities.TypeChecking.letter_lists import (
    Type1_letters,
    Type2_letters,
    Type3_letters,
    Type4_letters,
    Type5_letters,
    Type6_letters,
)


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

    def show_panels_based_on_chosen_letters(self) -> None:
        selected_letters_that_match_section_type: set[Letters] = set()
        letter_types = {
            "Type1": Type1_letters,
            "Type2": Type2_letters,
            "Type3": Type3_letters,
            "Type4": Type4_letters,
            "Type5": Type5_letters,
            "Type6": Type6_letters,
        }

        for letter in self.scroll_area.parent_tab.selected_letters:
            if (
                self.letter_type in letter_types
                and letter in letter_types[self.letter_type]
            ):
                selected_letters_that_match_section_type.add(letter)
        tabs = [
            MOTION_TYPE,
            COLOR,
            LEAD_STATE,
        ]

        motion_types_present = set()
        for letter in selected_letters_that_match_section_type:
            motion_types_present.update(motion_type_letter_combinations[letter])

        tabs_to_show: List[MotionAttributes] = []
        tabs_to_hide: List[MotionAttributes] = []

        if motion_types_present == {PRO} or motion_types_present == {ANTI}:
            tabs_to_show.append(COLOR)
        elif len(motion_types_present) > 1:
            tabs_to_show.extend([MOTION_TYPE, COLOR])
        if selected_letters_that_match_section_type.intersection(["S", "T", "U", "V"]):
            tabs_to_show.append(LEAD_STATE)

        for tab in tabs:
            if tab not in tabs_to_show:
                tabs_to_hide.append(tab)

        self.show_tabs(tabs_to_show)
        self.hide_tabs(tabs_to_hide)

        # Make sure the correct tab is visible
        if tabs_to_show:
            self.setCurrentIndex(
                self.indexOf(getattr(self, f"{tabs_to_show[0].lower()}_attr_panel"))
            )
        self.resize_filter_tab()




