from typing import TYPE_CHECKING, Literal
from PyQt6.QtWidgets import QTabWidget
from constants import COLOR, LEAD_STATE, MOTION_TYPE, PRO, ANTI, STATIC, DASH
from data.letter_engine_data import motion_type_letter_combinations
from utilities.TypeChecking.TypeChecking import Letters
from widgets.filter_frame.attr_panel.color_attr_panel import ColorAttrPanel

if TYPE_CHECKING:
    from widgets.pictograph_scroll_area.pictograph_scroll_area import (
        PictographScrollArea,
    )

from typing import TYPE_CHECKING, List
from ..attr_panel.lead_state_attr_panel import IGLeadStateAttrPanel
from ..attr_panel.motion_type_attr_panel import MotionTypeAttrPanel
from PyQt6.QtWidgets import QHBoxLayout


class ScrollAreaFilterTab(QTabWidget):
    def __init__(self, scroll_area: "PictographScrollArea") -> None:
        super().__init__(scroll_area)
        self.scroll_area = scroll_area
        self.attr_panel = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.motion_type_attr_panel = MotionTypeAttrPanel(self.scroll_area.parent_tab)
        self.color_attr_panel = ColorAttrPanel(self.scroll_area.parent_tab)
        self.lead_state_attr_panel = IGLeadStateAttrPanel(self.scroll_area.parent_tab)
        self.addTab(self.motion_type_attr_panel, "Filter by Motion Type")
        self.addTab(self.color_attr_panel, "Filter by Colors")
        self.addTab(self.lead_state_attr_panel, "Filter by Lead State")
        self.panels: List[
            MotionTypeAttrPanel | ColorAttrPanel | IGLeadStateAttrPanel
        ] = [
            self.motion_type_attr_panel,
            self.color_attr_panel,
            self.lead_state_attr_panel,
        ]
        self.setContentsMargins(0, 0, 0, 0)
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def show_panel(self, panel: Literal["motion_type", "color", "lead_state"]) -> None:
        if panel == MOTION_TYPE:
            self.setCurrentWidget(self.motion_type_attr_panel)
        elif panel == COLOR:
            self.setCurrentWidget(self.color_attr_panel)
        elif panel == LEAD_STATE:
            self.setCurrentWidget(self.lead_state_attr_panel)


    def show_panels_based_on_chosen_letters(self) -> None:
        selected_letters = set(self.scroll_area.parent_tab.selected_letters)

        motion_types_present = set()
        for letter in selected_letters:
            motion_types_present.update(motion_type_letter_combinations[letter])

        if motion_types_present == {PRO}:
            self.show_panel("color")
        elif motion_types_present == {ANTI}:
            self.show_panel("color")
        elif PRO in motion_types_present and ANTI in motion_types_present:
            self.show_panel("motion_type")
            self.show_panel("color")
        elif motion_types_present.issubset({STATIC, DASH}):
            self.show_panel("color")
        else:
            self.show_panel("motion_type")
            self.show_panel("color")
            self.show_panel("lead_state")

        if selected_letters.intersection(["S", "T", "U", "V"]):
            self.show_panel("lead_state")
