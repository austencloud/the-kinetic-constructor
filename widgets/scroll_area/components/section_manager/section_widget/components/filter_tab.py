from typing import TYPE_CHECKING, List
from PyQt6.QtWidgets import QTabWidget, QHBoxLayout
from Enums import LetterType
from constants import DASH, MOTION_TYPE, COLOR, LEAD_STATE, PRO, ANTI, STATIC
from utilities.TypeChecking.TypeChecking import (
    LetterTypes,
    Letters,
    MotionAttributes,
)
from data.letter_engine_data import (
    motion_type_letter_combinations,
    letter_type_motion_type_map,
)
from widgets.turns_panel import TurnsPanel


if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph
    from widgets.scroll_area.components.section_manager.section_widget.section_widget import (
        SectionWidget,
    )


class FilterTab(QTabWidget):
    def __init__(self, section: "SectionWidget") -> None:
        super().__init__(section)
        self.section = section
        self.attr_box_border_width = 3
        self.motion_type_turns_panel = TurnsPanel(self, MOTION_TYPE)
        self.color_turns_panel = TurnsPanel(self, COLOR)
        self.lead_state_turns_panel = TurnsPanel(self, LEAD_STATE)
        self.panels: List[TurnsPanel] = [
            self.motion_type_turns_panel,
            self.color_turns_panel,
            self.lead_state_turns_panel,
        ]
        self.setup_ui()
        self.currentChanged.connect(self.on_current_changed)

    def on_current_changed(self, index: int) -> None:
        for pictograph in self.section.scroll_area.pictographs.values():
            if (
                LetterType.get_letter_type(pictograph.letter)
                == self.section.letter_type
            ):
                for motion in pictograph.motions.values():
                    motion.turns_manager.set_turns(0)
                pictograph.updater.update_pictograph()
        for panel in self.panels:
            for box in panel.boxes:
                box.turns_widget.display_manager.update_turns_display("0")
                box.prop_rot_dir_button_manager.hide_prop_rot_dir_buttons()
        self.section.vtg_dir_button_manager.hide_vtg_dir_buttons()

    def get_motion_types_from_letter_type(
        self, letter_type: LetterTypes
    ) -> List[MotionAttributes]:
        motion_types = letter_type_motion_type_map[letter_type]
        return motion_types

    def setup_ui(self) -> None:
        self.setContentsMargins(0, 0, 0, 0)
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

    def show_tabs_based_on_chosen_letters(self) -> None:
        selected_letters = self.section.scroll_area.codex.selected_letters
        relevant_selected_letters = [
            letter
            for letter in selected_letters
            if LetterType.get_letter_type(letter) == self.section.letter_type
        ]
        tabs_to_show = self._determine_tabs_to_show(relevant_selected_letters)
        tabs_to_hide = self._determine_tabs_to_hide(tabs_to_show)
        self.show_tabs(tabs_to_show)
        self.hide_tabs(tabs_to_hide)
        self.motion_type_turns_panel.show_motion_type_boxes_based_on_chosen_letters(
            selected_letters
        )

    def _determine_tabs_to_show(
        self, selected_letters: set[Letters]
    ) -> List[MotionAttributes]:
        tabs_to_show = []
        motion_types_present = set()

        for letter_str in selected_letters:
            motion_types_present.update(motion_type_letter_combinations[letter_str])

        if (
            motion_types_present == {PRO}
            or motion_types_present == {ANTI}
            or motion_types_present == {DASH}
            or motion_types_present == {STATIC}
        ):
            tabs_to_show.append(COLOR)
        elif len(motion_types_present) > 1:
            tabs_to_show.extend([MOTION_TYPE, COLOR])
        if any(letter_str in {"S", "T", "U", "V"} for letter_str in selected_letters):
            tabs_to_show.append(LEAD_STATE)

        for letter in selected_letters:
            if LetterType.get_letter_type(letter) == self.section.letter_type:
                break
        else:
            tabs_to_show.clear()

        return tabs_to_show

    def _determine_tabs_to_hide(
        self, tabs_to_show: List[MotionAttributes]
    ) -> List[MotionAttributes]:
        all_tabs = [MOTION_TYPE, COLOR, LEAD_STATE]
        return [tab for tab in all_tabs if tab not in tabs_to_show]

    def show_tabs(self, tabs: List[MotionAttributes]) -> None:
        for tab in tabs:
            if tab == COLOR and self.indexOf(self.color_turns_panel) == -1:
                self.addTab(self.color_turns_panel, "Filter by Colors")
            elif (
                tab == MOTION_TYPE and self.indexOf(self.motion_type_turns_panel) == -1
            ):
                self.addTab(self.motion_type_turns_panel, "Filter by Motion Type")
            elif tab == LEAD_STATE and self.indexOf(self.lead_state_turns_panel) == -1:
                self.addTab(self.lead_state_turns_panel, "Filter by Lead State")

    def hide_tabs(self, tabs: List[MotionAttributes]) -> None:
        if not tabs:
            self.clear()
        else:
            for tab in tabs:
                if tab == COLOR and self.indexOf(self.color_turns_panel) != -1:
                    self.removeTab(self.indexOf(self.color_turns_panel))
                elif (
                    tab == MOTION_TYPE
                    and self.indexOf(self.motion_type_turns_panel) != -1
                ):
                    self.removeTab(self.indexOf(self.motion_type_turns_panel))
                elif (
                    tab == LEAD_STATE
                    and self.indexOf(self.lead_state_turns_panel) != -1
                ):
                    self.removeTab(self.indexOf(self.lead_state_turns_panel))

    def get_current_turns_values(self) -> dict[MotionAttributes, dict]:
        turns_values = {
            attribute_type: {
                box.attribute_value: box.turns_widget.display_manager.get_current_turns_value()
                for box in panel.boxes
            }
            for panel in self.panels
            for attribute_type in [panel.attribute_type]
        }
        return turns_values

    def apply_turns_to_pictograph(self, pictograph: "Pictograph") -> None:
        turns_values = self.get_current_turns_values()
        for motion in pictograph.motions.values():
            motion_type = motion.motion_type
            if motion_type in turns_values[MOTION_TYPE]:
                motion.turns_manager.set_turns(turns_values[MOTION_TYPE][motion_type])

            if motion.color in turns_values[COLOR]:
                motion.turns_manager.set_turns(turns_values[COLOR][motion.color])

            if (
                hasattr(motion, "lead_state")
                and motion.lead_state in turns_values[LEAD_STATE]
            ):
                motion.turns_manager.set_turns(
                    turns_values[LEAD_STATE][motion.lead_state]
                )

    def resize_filter_tab(self) -> None:
        for panel in self.panels:
            panel.resize_turns_panel()

    def get_currently_visible_panel(self) -> TurnsPanel:
        return self.panels[self.currentIndex()]
