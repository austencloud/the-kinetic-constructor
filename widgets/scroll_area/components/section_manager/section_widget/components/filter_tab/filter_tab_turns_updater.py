from constants import MOTION_TYPE, COLOR, LEAD_STATE
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.pictograph.pictograph import Pictograph
    from objects.motion.motion import Motion
    from widgets.scroll_area.components.section_manager.section_widget.components.filter_tab.filter_tab import (
        FilterTab,
    )


class FilterTabTurnsUpdater:
    def __init__(self, filter_tab_manager: "FilterTab"):
        self.manager = filter_tab_manager

    def apply_turns(self, pictograph: "Pictograph"):
        turns_values = self.manager.get_current_turns_values()

        for motion in pictograph.motions.values():
            self._apply_motion_type_turns(motion, turns_values.get(MOTION_TYPE, {}))
            self._apply_color_turns(motion, turns_values.get(COLOR, {}))
            self._apply_lead_state_turns(motion, turns_values.get(LEAD_STATE, {}))

            pictograph.updater.update_pictograph()

    def _apply_motion_type_turns(self, motion: "Motion", motion_type_turns):
        if motion.motion_type in motion_type_turns:
            motion.turns_manager.set_turns(motion_type_turns[motion.motion_type])

    def _apply_color_turns(self, motion: "Motion", color_turns):
        if motion.color in color_turns:
            motion.turns_manager.set_turns(color_turns[motion.color])

    def _apply_lead_state_turns(self, motion: "Motion", lead_state_turns):
        if hasattr(motion, "lead_state") and motion.lead_state in lead_state_turns:
            motion.turns_manager.set_turns(lead_state_turns[motion.lead_state])
