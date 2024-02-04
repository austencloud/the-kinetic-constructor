from typing import List
from Enums import LetterType, TabName
from constants import PRO, ANTI, DASH, STATIC
from data.letter_engine_data import motion_type_letter_combinations
from typing import List
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from widgets.pictograph.pictograph import Pictograph
    from .filter_tab import FilterTab


class FilterTabVisibilityHandler:
    def __init__(self, filter_tab: "FilterTab"):
        self.filter_tab = filter_tab
        self.section = self.filter_tab.section

        self.tabs = {
            TabName.MOTION_TYPE: self.filter_tab.motion_type_turns_panel,
            TabName.COLOR: self.filter_tab.color_turns_panel,
            TabName.LEAD_STATE: self.filter_tab.lead_state_turns_panel,
        }

    def update_visibility_based_on_selected_letters(self):
        selected_letters = self.section.scroll_area.codex.selected_letters
        tabs_to_show = self._determine_tabs_to_show_based_on_selected_letters(
            selected_letters
        )
        self._update_tabs_visibility(tabs_to_show)

    def _determine_tabs_to_show_based_on_selected_letters(
        self, selected_letters: List[str]
    ) -> List[TabName]:
        motion_types_present = {
            motion_type
            for letter in selected_letters
            if LetterType.get_letter_type(letter) == self.section.letter_type
            for motion_type in self._get_motion_types_from_letter(letter)
        }

        tabs_to_show = set()

        if motion_types_present.intersection({PRO, ANTI, DASH, STATIC}):
            tabs_to_show.add(TabName.COLOR)

        if len(motion_types_present) > 1:
            tabs_to_show.add(TabName.MOTION_TYPE)

        if any(letter in {"S", "T", "U", "V"} for letter in selected_letters):
            tabs_to_show.add(TabName.LEAD_STATE)

        return list(tabs_to_show)

    def _get_motion_types_from_letter(self, letter: str) -> List[str]:
        return motion_type_letter_combinations.get(letter, [])

    def _update_tabs_visibility(self, tabs_to_show: List[TabName]):
        for tab_key, panel in self.tabs.items():
            # Convert the enum to a user-friendly string for the tab label
            tab_label = tab_key.name.replace("_", " ").title()

            if tab_key in tabs_to_show and self.filter_tab.indexOf(panel) == -1:
                self.filter_tab.addTab(panel, tab_label)
            elif tab_key not in tabs_to_show and self.filter_tab.indexOf(panel) != -1:
                self.filter_tab.removeTab(self.filter_tab.indexOf(panel))

        # Update the logic for showing motion type boxes as well, if needed
        if TabName.MOTION_TYPE in tabs_to_show:
            selected_letters = self.section.scroll_area.codex.selected_letters
            self.tabs[TabName.MOTION_TYPE].show_motion_type_boxes_based_on_chosen_letters(selected_letters)


    def apply_turns_from_turns_boxes_to_pictograph(self, pictograph: "Pictograph"):
        turns_values = self.filter_tab.get_current_turns_values()

        # Adjust the keys to use TabName enums instead of strings
        attribute_to_property_and_values = {
            TabName.MOTION_TYPE: (
                "motion_type",
                turns_values.get(TabName.MOTION_TYPE.name.lower(), {}),
            ),
            TabName.COLOR: ("color", turns_values.get(TabName.COLOR.name.lower(), {})),
            TabName.LEAD_STATE: (
                "lead_state",
                turns_values.get(TabName.LEAD_STATE.name.lower(), {}),
            ),
        }

        for motion in pictograph.motions.values():
            for tab_key, (
                motion_attribute,
                attribute_turns,
            ) in attribute_to_property_and_values.items():
                if self.tabs[tab_key].isVisible():
                    self._apply_turns_if_applicable(
                        motion, motion_attribute, attribute_turns
                    )

    def _apply_turns_if_applicable(
        self, motion: "Motion", motion_attribute, attribute_turns
    ):
        attribute_value = getattr(motion, motion_attribute, None)
        if attribute_value in attribute_turns:
            motion.turns_manager.set_turns(attribute_turns[attribute_value])

    def resize_filter_tab(self) -> None:
        for panel in self.filter_tab.panels:
            panel.resize_turns_panel()
