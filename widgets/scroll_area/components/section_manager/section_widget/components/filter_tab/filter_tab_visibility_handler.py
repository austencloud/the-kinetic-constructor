from typing import List
from Enums import LetterType
from constants import (
    BLUE,
    LEADING,
    PRO,
    ANTI,
    DASH,
    RED,
    STATIC,
    TRAILING,
)
from data.letter_engine_data import motion_type_letter_combinations

from typing import List
from typing import TYPE_CHECKING

from utilities.TypeChecking.MotionAttributes import Turns


if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from widgets.pictograph.pictograph import Pictograph
    from .filter_tab import FilterTab


class FilterTabVisibilityHandler:
    def __init__(self, filter_tab: "FilterTab"):
        self.filter_tab = filter_tab
        self.section = self.filter_tab.section

        self.tabs = {
            "Motion Type": self.filter_tab.motion_type_turns_panel,
            "Color": self.filter_tab.color_turns_panel,
            "Lead State": self.filter_tab.lead_state_turns_panel,
        }

    def update_visibility_based_on_selected_letters(self):
        selected_letters = self.section.scroll_area.codex.selected_letters
        tabs_to_show = self._determine_tabs_to_show_based_on_selected_letters(
            selected_letters
        )
        self._update_tabs_visibility(tabs_to_show)

    def _determine_tabs_to_show_based_on_selected_letters(
        self, selected_letters: List[str]
    ) -> List[str]:
        tabs_to_show = []
        motion_types_present = set()

        for letter in selected_letters:
            letter_type = LetterType.get_letter_type(letter)
            if letter_type == self.section.letter_type:
                motion_types_present.update(self._get_motion_types_from_letter(letter))

        if {PRO, ANTI, DASH, STATIC}.intersection(motion_types_present):
            tabs_to_show.append("Color")

        if len(motion_types_present) > 1:
            tabs_to_show.extend(["Motion Type", "Color"])

        if any(letter in {"S", "T", "U", "V"} for letter in selected_letters):
            tabs_to_show.append("Lead State")

        return tabs_to_show

    def _get_motion_types_from_letter(self, letter: str) -> List[str]:
        return motion_type_letter_combinations.get(letter, [])

    def _update_tabs_visibility(self, tabs_to_show: List[str]):
        for tab_key, panel in self.tabs.items():
            # Use the friendly name for tab display
            if tab_key in tabs_to_show and self.filter_tab.indexOf(panel) == -1:
                self.filter_tab.addTab(
                    panel, tab_key
                )  # Use tab_key which is now user-friendly
            elif tab_key not in tabs_to_show and self.filter_tab.indexOf(panel) != -1:
                self.filter_tab.removeTab(self.filter_tab.indexOf(panel))

        if "Motion Type" in tabs_to_show:
            selected_letters = self.section.scroll_area.codex.selected_letters
            self.tabs["Motion Type"].show_motion_type_boxes_based_on_chosen_letters(
                selected_letters
            )

    def apply_turns_from_turns_boxes_to_pictograph(self, pictograph: "Pictograph"):
        turns_values = self.filter_tab.get_current_turns_values()

        for motion in pictograph.motions.values():
            motion_type, color, lead_state = (
                motion.motion_type,
                motion.color,
                getattr(motion, "Lead State", None),
            )
            # if the motion type tab is visible:
            if self.tabs["Motion Type"].isVisible():
                self._apply_turns_if_applicable(
                    motion, motion_type, turns_values.get("motion_type", {})
                )
            elif self.tabs["Color"].isVisible():
                self._apply_turns_if_applicable(
                    motion, color, turns_values.get("color", {})
                )
            elif self.tabs["Lead State"].isVisible():
                self._apply_turns_if_applicable(
                    motion, lead_state, turns_values.get("lead_state", {})
                )

    def _apply_turns_if_applicable(
        self,
        motion: "Motion",
        attribute_value,
        filter_tab_turn_values_dict: dict[str, int],
    ):
        if attribute_value in [PRO, ANTI, DASH, STATIC]:
            if motion.motion_type == attribute_value:
                motion.turns_manager.set_turns(
                    filter_tab_turn_values_dict[attribute_value]
                )
        elif attribute_value in [RED, BLUE]:
            if motion.color == attribute_value:
                motion.turns_manager.set_turns(
                    filter_tab_turn_values_dict[attribute_value]
                )
        elif attribute_value in [LEADING, TRAILING]:
            if motion.lead_state == attribute_value:
                motion.turns_manager.set_turns(
                    filter_tab_turn_values_dict[attribute_value]
                )

    def resize_filter_tab(self) -> None:
        for panel in self.filter_tab.panels:
            panel.resize_turns_panel()
