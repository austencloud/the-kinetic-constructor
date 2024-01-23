from typing import TYPE_CHECKING, Callable, List, Union
from constants import (
    BLUE,
    CLOCKWISE,
    COLOR,
    COUNTER_CLOCKWISE,
    DASH,
    ICON_DIR,
    MOTION_TYPE,
    OPP,
    PROP_ROT_DIR,
    RED,
    SAME,
    STATIC,
    Type2,
    Type3,
    Type4,
    Type5,
    Type6,
)
from utilities.TypeChecking.MotionAttributes import PropRotDirs
from utilities.TypeChecking.TypeChecking import VtgDirections
from ...factories.button_factory.button_factory import ButtonFactory
from ...factories.button_factory.buttons.rot_dir_buttons import (
    VtgDirButton,
    PropRotDirButton,
)

from PyQt6.QtWidgets import QPushButton, QLabel

if TYPE_CHECKING:
    from widgets.scroll_area.components.section_manager.section_widget.section_widget import (
        SectionWidget,
    )
    from widgets.turns_box.turns_box import TurnsBox
    from objects.motion.motion import Motion


class RotDirButtonManager:
    def __init__(self, section_widget: "SectionWidget") -> None:
        self.section = section_widget
        self.previous_turns = 0
        self.prop_rot_dir_buttons: List[
            PropRotDirButton
        ] = self._setup_prop_rot_dir_buttons()
        self.vtg_dir_buttons: List[VtgDirButton] = self._setup_vtg_dir_buttons()
        self.buttons = self.prop_rot_dir_buttons + self.vtg_dir_buttons
        self.section.header_layout.insertStretch(0, 8)
        self.section.header_layout.insertWidget(1, self.opp_button)
        self.section.header_layout.addWidget(self.same_button)
        self.section.header_layout.insertStretch(6, 8)

        self.hide_vtg_dir_buttons()

    def show_vtg_dir_buttons(self):
        self.opp_button.show()
        self.same_button.show()

    def hide_vtg_dir_buttons(self):
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

    def _setup_prop_rot_dir_buttons(self) -> List[QPushButton]:
        self.cw_button: PropRotDirButton = ButtonFactory.create_prop_rot_dir_button(
            f"{ICON_DIR}clock/clockwise.png",
            lambda: self._set_prop_rot_dir(CLOCKWISE),
            CLOCKWISE,
        )
        self.ccw_button: PropRotDirButton = ButtonFactory.create_prop_rot_dir_button(
            f"{ICON_DIR}clock/counter_clockwise.png",
            lambda: self._set_prop_rot_dir(COUNTER_CLOCKWISE),
            COUNTER_CLOCKWISE,
        )
        self.cw_button.unpress()
        self.ccw_button.unpress()

        return [self.cw_button, self.ccw_button]

    def _vtg_dir_callback(self, direction: VtgDirections) -> Callable:
        def callback() -> None:
            self._set_vtg_dir(direction)

        return callback

    def _prop_rot_dir_callback(self, direction: VtgDirections) -> Callable:
        def callback() -> None:
            self._set_prop_rot_dir(direction)

        return callback

    def _set_vtg_dir(self, vtg_dir: VtgDirections) -> None:
        self._update_pictographs_vtg_dir(vtg_dir)
        self._update_button_states(self.vtg_dir_buttons, vtg_dir)

    def _set_prop_rot_dir(self, prop_rot_dir: PropRotDirs) -> None:
        self._update_pictographs_prop_rot_dir(prop_rot_dir)
        self._update_button_states(self.prop_rot_dir_buttons, prop_rot_dir)

    def _update_pictographs_vtg_dir(self, vtg_dir: VtgDirections) -> None:
        for pictograph in self.section.pictographs.values(): 
            for motion in pictograph.motions.values():
                other_motion = pictograph.get.other_motion(motion)
                if motion.check.is_dash() or motion.check.is_static():
                    if other_motion.check.is_shift():
                        pictograph.vtg_dir = vtg_dir
                        if vtg_dir == SAME:
                            self._update_pictograph_vtg_dir(
                                motion, other_motion.prop_rot_dir
                            )
                        elif vtg_dir == OPP:
                            self._update_pictograph_vtg_dir(
                                motion,
                                self._opposite_prop_rot_dir(other_motion.prop_rot_dir),
                            )

    def _update_pictographs_prop_rot_dir(self, prop_rot_dir: PropRotDirs) -> None:
        for pictograph in self.section.scroll_area.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.motion_type in [DASH, STATIC]:
                    attribute_type = self.section.filter_tab.panels[
                        self.section.filter_tab.currentIndex()
                    ].attribute_type
                    box_attribute_value = (
                        self.section.filter_tab.get_currently_visible_panel()
                        .visible_boxes[1]
                        .attribute_value
                    )
                    if attribute_type == MOTION_TYPE:
                        if motion.motion_type == box_attribute_value:
                            self._update_pictograph_prop_rot_dir(motion, prop_rot_dir)
                    elif attribute_type == COLOR:
                        if motion.color == box_attribute_value:
                            self._update_pictograph_prop_rot_dir(motion, prop_rot_dir)

    def _update_pictograph_vtg_dir(
        self, motion: "Motion", vtg_dir: VtgDirections
    ) -> None:
        motion.prop_rot_dir = vtg_dir
        pictograph_dict = {
            motion.color + "_" + PROP_ROT_DIR: vtg_dir,
        }
        motion.pictograph.updater.update_pictograph(pictograph_dict)

    def _update_pictograph_prop_rot_dir(
        self, motion: "Motion", prop_rot_dir: PropRotDirs
    ) -> None:
        motion.prop_rot_dir = prop_rot_dir
        pictograph_dict = {
            motion.color + "_" + PROP_ROT_DIR: prop_rot_dir,
        }
        motion.pictograph.updater.update_pictograph(pictograph_dict)

    def _update_button_states(
        self,
        buttons: List[Union[PropRotDirButton, VtgDirButton]],
        active_direction: VtgDirections,
    ) -> None:
        for button in buttons:
            if button.direction == active_direction:
                button.press()
            else:
                button.unpress()

    def show_prop_rot_dir_buttons(self):
        # Show Prop rotation direction buttons
        self.cw_button.show()
        self.ccw_button.show()

    def hide_prop_rot_dir_buttons(self):
        # Hide Prop rotation direction buttons
        self.cw_button.hide()
        self.ccw_button.hide()

    def _opposite_prop_rot_dir(self, prop_rot_dir: PropRotDirs) -> PropRotDirs:
        return {
            CLOCKWISE: COUNTER_CLOCKWISE,
            COUNTER_CLOCKWISE: CLOCKWISE,
        }.get(prop_rot_dir, prop_rot_dir)

    def update_visibility_based_on_motion(self, letter_type, new_turns) -> None:
        if letter_type in [Type2, Type3]:
            if new_turns > 0:
                if self.previous_turns == 0:
                    self.show_vtg_dir_buttons()
                    self.same_button.press()
                    self.previous_turns = new_turns
            elif new_turns == 0:
                self.previous_turns = 0
                self.hide_vtg_dir_buttons()
        elif letter_type in [Type4, Type5, Type6]:
            if new_turns > 0:
                self.show_prop_rot_dir_buttons()
            elif new_turns == 0:
                self.previous_turns = 0
                self.hide_prop_rot_dir_buttons()
