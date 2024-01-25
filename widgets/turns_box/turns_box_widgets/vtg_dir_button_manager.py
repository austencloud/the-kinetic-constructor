from typing import TYPE_CHECKING, List, Union
from constants import (
    ANTI,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    ICON_DIR,
    OPP,
    PRO,
    PROP_ROT_DIR,
    SAME,
)
from utilities.TypeChecking.MotionAttributes import Colors, MotionTypes, PropRotDirs
from utilities.TypeChecking.TypeChecking import LeadStates, VtgDirections
from ...factories.button_factory.button_factory import ButtonFactory
from ...factories.button_factory.buttons.rot_dir_buttons import (
    VtgDirButton,
)

from PyQt6.QtWidgets import QPushButton

if TYPE_CHECKING:
    from widgets.scroll_area.components.section_manager.section_widget.section_widget import (
        SectionWidget,
    )
    from objects.motion.motion import Motion


class VtgDirButtonManager:
    def __init__(self, section_widget: "SectionWidget") -> None:
        self.section = section_widget
        self.previous_turns = 0

        self.vtg_dir_buttons: List[VtgDirButton] = self._setup_vtg_dir_buttons()
        self.section.header_layout.insertStretch(0, 8)
        self.section.header_layout.insertWidget(1, self.opp_button)
        self.section.header_layout.addWidget(self.same_button)
        self.section.header_layout.insertStretch(6, 8)
        self.hide_vtg_dir_buttons()

    def show_vtg_dir_buttons(self) -> None:
        self.opp_button.show()
        self.same_button.show()

    def hide_vtg_dir_buttons(self) -> None:
        self.opp_button.hide()
        self.same_button.hide()

    def _setup_vtg_dir_buttons(self) -> List[QPushButton]:
        self.same_button: VtgDirButton = ButtonFactory.create_vtg_dir_button(
            f"{ICON_DIR}same_direction.png", lambda: self._set_vtg_dir(SAME), SAME
        )
        self.opp_button: VtgDirButton = ButtonFactory.create_vtg_dir_button(
            f"{ICON_DIR}opp_direction.png", lambda: self._set_vtg_dir(OPP), OPP
        )
        self.same_button.unpress()
        self.opp_button.unpress()

        return [self.same_button, self.opp_button]

    def _set_vtg_dir(self, vtg_dir: VtgDirections) -> None:
        self._update_pictographs_vtg_dir(vtg_dir)
        self._update_button_states(self.vtg_dir_buttons, vtg_dir)

    def _update_pictographs_vtg_dir(self, vtg_dir: VtgDirections) -> None:
        for pictograph in self.section.pictographs.values():
            for motion in pictograph.motions.values():
                other_motion = pictograph.get.other_motion(motion)
                if motion.check.is_dash() or motion.check.is_static():
                    if other_motion.check.is_shift():
                        pictograph.vtg_dir = vtg_dir
                        if vtg_dir == SAME:
                            self._update_pictograph_prop_rot_dir_drom_vtg_dir_setting(
                                motion, other_motion.prop_rot_dir
                            )
                        elif vtg_dir == OPP:
                            self._update_pictograph_prop_rot_dir_drom_vtg_dir_setting(
                                motion,
                                self._opposite_prop_rot_dir(other_motion.prop_rot_dir),
                            )

    def _update_pictograph_prop_rot_dir_drom_vtg_dir_setting(
        self, motion: "Motion", prop_rot_dir: PropRotDirs
    ) -> None:
        motion.prop_rot_dir = prop_rot_dir
        pictograph_dict = {motion.color + "_" + PROP_ROT_DIR: prop_rot_dir}
        motion.pictograph.updater.update_pictograph(pictograph_dict)

    def _update_button_states(
        self, buttons: List[VtgDirButton], active_direction: VtgDirections
    ) -> None:
        for button in buttons:
            if button.direction == active_direction:
                button.press()
            else:
                button.unpress()

    def _opposite_prop_rot_dir(self, prop_rot_dir: PropRotDirs) -> PropRotDirs:
        return {
            CLOCKWISE: COUNTER_CLOCKWISE,
            COUNTER_CLOCKWISE: CLOCKWISE,
        }.get(prop_rot_dir, prop_rot_dir)

    def update_visibility_based_on_motion(self, letter_type, new_turns, attribute_value: Union[Colors, MotionTypes, LeadStates]) -> None:
        if attribute_value in [PRO, ANTI]:
            return
        if new_turns > 0:
            if self.previous_turns == 0:
                self.show_vtg_dir_buttons()
                self.same_button.press()
                self.previous_turns = new_turns
        elif new_turns == 0:
            self.previous_turns = 0
            self.hide_vtg_dir_buttons()

    def unpress_vtg_buttons(self) -> None:
        self.same_button.unpress()
        self.opp_button.unpress()
