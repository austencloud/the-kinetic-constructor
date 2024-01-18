from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import QTabWidget, QHBoxLayout
from constants import MOTION_TYPE, COLOR, LEAD_STATE, PRO, ANTI
from utilities.TypeChecking.TypeChecking import (
    LetterTypeNums,
    Letters,
    MotionAttributes,
)
from data.letter_engine_data import (
    motion_type_letter_combinations,
    letter_type_motion_type_map,
)
from widgets.attr_panel.base_attr_panel import BaseAttrPanel
from widgets.attr_panel.motion_type_attr_panel import MotionTypeAttrPanel
from widgets.attr_panel.color_attr_panel import ColorAttrPanel
from widgets.attr_panel.lead_state_attr_panel import LeadStateAttrPanel

if TYPE_CHECKING:
    from widgets.pictograph_scroll_area.scroll_area import ScrollArea


class FilterTab(QTabWidget):
    def __init__(self, scroll_area: "ScrollArea", letter_type: LetterTypeNums) -> None:
        super().__init__(scroll_area)
        self.scroll_area = scroll_area
        self.motion_type_attr_panel = MotionTypeAttrPanel(
            self, self.get_motion_types_from_letter_type(letter_type)
        )
        self.color_attr_panel = ColorAttrPanel(self)
        self.lead_state_attr_panel = LeadStateAttrPanel(self)
        self.panels: List[BaseAttrPanel] = [
            self.motion_type_attr_panel,
            self.color_attr_panel,
            self.lead_state_attr_panel,
        ]
        self.letter_type = letter_type
        self.setup_ui()

    def get_motion_types_from_letter_type(
        self, letter_type: LetterTypeNums
    ) -> List[MotionAttributes]:
        motion_types = letter_type_motion_type_map[letter_type]
        return motion_types

    def setup_ui(self) -> None:
        self.setContentsMargins(0, 0, 0, 0)
        self.layout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def show_tabs_based_on_chosen_letters(self) -> None:
        selected_letters = self.scroll_area.parent_tab.selected_letters
        tabs_to_show = self._determine_tabs_to_show(selected_letters)
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
        tabs_to_show = []
        motion_types_present = set()

        for letter in selected_letters:
            motion_types_present.update(motion_type_letter_combinations[letter])

        if motion_types_present == {PRO} or motion_types_present == {ANTI}:
            tabs_to_show.append(COLOR)
        elif len(motion_types_present) > 1:
            tabs_to_show.extend([MOTION_TYPE, COLOR])
        if ["S", "T", "U", "V"] in selected_letters:
            tabs_to_show.append(LEAD_STATE)

        return tabs_to_show

    def _determine_tabs_to_hide(
        self, tabs_to_show: List[MotionAttributes]
    ) -> List[MotionAttributes]:
        all_tabs = [MOTION_TYPE, COLOR, LEAD_STATE]
        return [tab for tab in all_tabs if tab not in tabs_to_show]

    def show_tabs(self, tabs: List[MotionAttributes]) -> None:
        for tab in tabs:
            if tab == MOTION_TYPE and self.indexOf(self.motion_type_attr_panel) == -1:
                self.addTab(self.motion_type_attr_panel, "Filter by Motion Type")
            elif tab == COLOR and self.indexOf(self.color_attr_panel) == -1:
                self.addTab(self.color_attr_panel, "Filter by Colors")
            elif tab == LEAD_STATE and self.indexOf(self.lead_state_attr_panel) == -1:
                self.addTab(self.lead_state_attr_panel, "Filter by Lead State")

    def hide_tabs(self, tabs: List[MotionAttributes]) -> None:
        for tab in tabs:
            if tab == MOTION_TYPE and self.indexOf(self.motion_type_attr_panel) != -1:
                self.removeTab(self.indexOf(self.motion_type_attr_panel))
            elif tab == COLOR and self.indexOf(self.color_attr_panel) != -1:
                self.removeTab(self.indexOf(self.color_attr_panel))
            elif tab == LEAD_STATE and self.indexOf(self.lead_state_attr_panel) != -1:
                self.removeTab(self.indexOf(self.lead_state_attr_panel))

    def resize_filter_tab(self) -> None:
        for panel in self.panels:
            panel.resize_attr_panel()
