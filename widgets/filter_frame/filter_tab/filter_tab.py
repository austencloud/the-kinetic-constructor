from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QTabWidget
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
from widgets.filter_frame.attr_panel.color_attr_panel import ColorAttrPanel

if TYPE_CHECKING:
    from widgets.pictograph_scroll_area.pictograph_scroll_area import (
        PictographScrollArea,
    )

from typing import TYPE_CHECKING, List
from ..attr_panel.lead_state_attr_panel import IGLeadStateAttrPanel
from ..attr_panel.motion_type_attr_panel import MotionTypeAttrPanel
from PyQt6.QtWidgets import QHBoxLayout


class FilterTab(QTabWidget):
    def __init__(
        self, scroll_area: "PictographScrollArea", letter_type: LetterTypeNums
    ) -> None:
        super().__init__(scroll_area)
        self.scroll_area = scroll_area
        self.attr_panel = None
        self.letter_type: LetterTypeNums = letter_type
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.motion_type_attr_panel = MotionTypeAttrPanel(self.scroll_area.parent_tab)
        self.color_attr_panel = ColorAttrPanel(self.scroll_area.parent_tab)
        self.lead_state_attr_panel = IGLeadStateAttrPanel(self.scroll_area.parent_tab)

        self.tabs: List[MotionTypeAttrPanel | ColorAttrPanel | IGLeadStateAttrPanel] = [
            self.motion_type_attr_panel,
            self.color_attr_panel,
            self.lead_state_attr_panel,
        ]
        self.setContentsMargins(0, 0, 0, 0)
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def show_tab(self, tabs: List[MotionAttributes]) -> None:
        for tab in tabs:
            if tab == MOTION_TYPE and self.indexOf(self.motion_type_attr_panel) == -1:
                self.addTab(self.motion_type_attr_panel, "Filter by Motion Type")
            elif tab == COLOR and self.indexOf(self.color_attr_panel) == -1:
                self.addTab(self.color_attr_panel, "Filter by Colors")
            elif tab == LEAD_STATE and self.indexOf(self.lead_state_attr_panel) == -1:
                self.addTab(self.lead_state_attr_panel, "Filter by Lead State")

    def hide_tab(self, tabs: List[MotionAttributes]) -> None:
        for tab in tabs:
            if tab == MOTION_TYPE and self.indexOf(self.motion_type_attr_panel) != -1:
                self.removeTab(self.indexOf(self.motion_type_attr_panel))
            elif tab == COLOR and self.indexOf(self.color_attr_panel) != -1:
                self.removeTab(self.indexOf(self.color_attr_panel))
            elif tab == LEAD_STATE and self.indexOf(self.lead_state_attr_panel) != -1:
                self.removeTab(self.indexOf(self.lead_state_attr_panel))

    def show_panels_based_on_chosen_letters(self) -> None:
        # remove all tabs first
        for tab in self.tabs:
            self.removeTab(self.indexOf(tab))

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
            if self.letter_type in letter_types and letter in letter_types[self.letter_type]:
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
        elif motion_types_present == {STATIC} or motion_types_present == {DASH}:
            tabs_to_show.append(COLOR)
        elif len(motion_types_present) > 1:
            tabs_to_show.extend([MOTION_TYPE, COLOR])
        if selected_letters_that_match_section_type.intersection(["S", "T", "U", "V"]):
            tabs_to_show.append(LEAD_STATE)

        for tab in tabs:
            if tab not in tabs_to_show:
                tabs_to_hide.append(tab)

        self.show_tab(tabs_to_show)
        self.hide_tab(tabs_to_hide)

        # Make sure the correct tab is visible
        if tabs_to_show:
            self.setCurrentIndex(
                self.indexOf(getattr(self, f"{tabs_to_show[0].lower()}_attr_panel"))
            )

    def bring_to_front(self, tab: MotionAttributes) -> None:
        if tab == MOTION_TYPE:
            index = self.indexOf(self.motion_type_attr_panel)
        elif tab == COLOR:
            index = self.indexOf(self.color_attr_panel)
        elif tab == LEAD_STATE:
            index = self.indexOf(self.lead_state_attr_panel)
        if index != -1:
            self.setCurrentIndex(index)
