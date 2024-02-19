from typing import List
from Enums.Enums import LetterType, TurnsTabAttribute
from constants import CLOCKWISE, COUNTER_CLOCKWISE, PRO, ANTI, DASH, STATIC
from data.letter_engine_data import motion_type_letter_combinations
from typing import List
from typing import TYPE_CHECKING

from widgets.codex_turns_panel import CodexTurnsPanel


if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from widgets.pictograph.pictograph import Pictograph
    from .turns_tab import TurnsTab


class TurnsTabVisibilityHandler:
    """
    Manages the visibility of filter tabs based on selected letters within a section.
    Dynamically updates which filter tabs are visible
    Applies turns to newly added pictographs based on filters.

    Attributes:
        turns_tab (FilterTab): The parent filter tab.
        section (SectionWidget): The parent section widget.
        tabs (dict[TabName, QWidget]): The filter tabs to manage.

    Methods:
        update_visibility_based_on_selected_letters()
        apply_turns_from_turns_boxes_to_pictograph(pictograph)
        resize_turns_tab()
    """

    def __init__(self, turns_tab: "TurnsTab"):
        self.turns_tab = turns_tab
        self.section = self.turns_tab.section

        self.turns_panels: dict[TurnsTabAttribute, CodexTurnsPanel] = {
            TurnsTabAttribute.MOTION_TYPE: self.turns_tab.motion_type_turns_panel,
            TurnsTabAttribute.COLOR: self.turns_tab.color_turns_panel,
            TurnsTabAttribute.LEAD_STATE: self.turns_tab.lead_state_turns_panel,
        }

    def update_visibility_based_on_selected_letters(self):
        selected_letters = self.section.scroll_area.codex.selected_letters
        tabs_to_show = self._determine_tabs_to_show_based_on_selected_letters(
            selected_letters
        )
        self._update_tabs_visibility(tabs_to_show)

    def _determine_tabs_to_show_based_on_selected_letters(
        self, selected_letters: List[str]
    ) -> List[TurnsTabAttribute]:
        motion_types_present = {
            motion_type
            for letter in selected_letters
            if LetterType.get_letter_type(letter) == self.section.letter_type
            for motion_type in self._get_motion_types_from_letter(letter)
        }

        tabs_to_show = set()
        if motion_types_present.intersection({PRO, ANTI, DASH, STATIC}):
            tabs_to_show.add(TurnsTabAttribute.COLOR)
        if len(motion_types_present) > 1:
            tabs_to_show.add(TurnsTabAttribute.MOTION_TYPE)
        if self.section.letter_type == LetterType.Type1:
            if any(letter in {"S", "T", "U", "V"} for letter in selected_letters):
                tabs_to_show.add(TurnsTabAttribute.LEAD_STATE)

        return list(tabs_to_show)

    def _get_motion_types_from_letter(self, letter: str) -> List[str]:
        return motion_type_letter_combinations.get(letter, [])

    def _update_tabs_visibility(self, tabs_to_show: List[TurnsTabAttribute]):
        for attribute, turns_panel in self.turns_panels.items():
            tab_label = attribute.name.replace("_", " ").title()

            if attribute in tabs_to_show and self.turns_tab.indexOf(turns_panel) == -1:
                self.turns_tab.addTab(turns_panel, tab_label)
            elif (
                attribute not in tabs_to_show
                and self.turns_tab.indexOf(turns_panel) != -1
            ):
                self.turns_tab.removeTab(self.turns_tab.indexOf(turns_panel))

        if TurnsTabAttribute.MOTION_TYPE in tabs_to_show:
            selected_letters = self.section.scroll_area.codex.selected_letters
            self.turns_panels[
                TurnsTabAttribute.MOTION_TYPE
            ].show_motion_type_boxes_based_on_chosen_letters(selected_letters)

    def apply_turns_from_turns_boxes_to_pictograph(self, pictograph: "Pictograph"):
        turns_values = self.turns_tab.get_current_turns_values()

        attribute_to_property_and_values = {
            TurnsTabAttribute.MOTION_TYPE: (
                "motion_type",
                turns_values.get(TurnsTabAttribute.MOTION_TYPE),
            ),
            TurnsTabAttribute.COLOR: (
                "color",
                turns_values.get(TurnsTabAttribute.COLOR),
            ),
            TurnsTabAttribute.LEAD_STATE: (
                "lead_state",
                turns_values.get(TurnsTabAttribute.LEAD_STATE),
            ),
        }

        for motion in pictograph.motions.values():
            for tab_key, (
                motion_attribute,
                attribute_turns,
            ) in attribute_to_property_and_values.items():
                if self.turns_panels[tab_key].isVisible():
                    self._apply_turns_if_applicable(
                        motion, motion_attribute, attribute_turns
                    )

    def _apply_turns_if_applicable(
        self, motion: "Motion", motion_attribute, attribute_turns
    ):
        attribute_value = getattr(motion, motion_attribute, None)
        if attribute_value in attribute_turns:
            motion.turns_manager.set_turns(attribute_turns[attribute_value])
            if attribute_turns[attribute_value] > 0:
                self.set_motion_prop_rot_dir_to_match_the_buttons_currently_pressed(
                    motion
                )

    def set_motion_prop_rot_dir_to_match_the_buttons_currently_pressed(
        self, motion: "Motion"
    ) -> None:
        if self.turns_tab.section.vtg_dir_button_manager.same_button.is_pressed():
            motion.prop_rot_dir = motion.pictograph.get.other_motion(
                motion
            ).prop_rot_dir
        elif self.turns_tab.section.vtg_dir_button_manager.opp_button.is_pressed():
            motion.prop_rot_dir = (
                CLOCKWISE
                if motion.pictograph.get.other_motion(motion).prop_rot_dir
                == COUNTER_CLOCKWISE
                else COUNTER_CLOCKWISE
            )

    def resize_turns_tab(self) -> None:
        for panel in self.turns_tab.panels:
            panel.resize_turns_panel()
