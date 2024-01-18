from typing import TYPE_CHECKING, Callable, List
from constants import (
    BLUE,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    ICON_DIR,
    OPP,
    PROP_ROT_DIR,
    RED,
    SAME,
    STATIC,
)
from utilities.TypeChecking.TypeChecking import VtgDirections
from ..buttons.prop_rot_dir_button import PropRotDirButton
from ..buttons.vtg_dir_button import VtgDirButton

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QPushButton

if TYPE_CHECKING:
    from widgets.attr_box.motion_type_attr_box import MotionTypeAttrBox


class RotDirButtonManager:
    def __init__(self, attr_box: "MotionTypeAttrBox") -> None:
        self.attr_box = attr_box

        self.prop_rot_dir_buttons: List[
            PropRotDirButton
        ] = self._setup_prop_rot_dir_buttons()
        self.vtg_dir_buttons: List[VtgDirButton] = self._setup_vtg_dir_buttons()

    def create_vtg_dir_button(
        self, icon_path: str, callback: Callable
    ) -> "VtgDirButton":
        button = VtgDirButton(self.attr_box)
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(callback)
        return button

    def create_prop_rot_dir_button(
        self, icon_path: str, callback: Callable
    ) -> "PropRotDirButton":
        button = PropRotDirButton(self.attr_box)
        button.setIcon(QIcon(icon_path))
        button.clicked.connect(callback)
        return button

    def _setup_vtg_dir_buttons(self) -> List[QPushButton]:
        self.same_button: VtgDirButton = self.create_vtg_dir_button(
            f"{ICON_DIR}same_direction.png", lambda: self._set_vtg_dir(SAME)
        )
        self.opp_button: VtgDirButton = self.create_vtg_dir_button(
            f"{ICON_DIR}opp_direction.png",
            lambda: self._set_vtg_dir(OPP),
        )
        self.same_button.unpress()
        self.opp_button.unpress()
        self.same_button.hide()
        self.opp_button.hide()
        return [self.same_button, self.opp_button]

    def _setup_prop_rot_dir_buttons(self) -> List[QPushButton]:
        self.cw_button: PropRotDirButton = self.create_prop_rot_dir_button(
            f"{ICON_DIR}clock/clockwise.png", lambda: self._set_prop_rot_dir(CLOCKWISE)
        )
        self.ccw_button: PropRotDirButton = self.create_prop_rot_dir_button(
            f"{ICON_DIR}clock/counter_clockwise.png",
            lambda: self._set_prop_rot_dir(COUNTER_CLOCKWISE),
        )
        self.cw_button.unpress()
        self.ccw_button.unpress()
        self.cw_button.hide()
        self.ccw_button.hide()
        return [self.cw_button, self.ccw_button]

    def _set_vtg_dir(self, vtg_dir: VtgDirections) -> None:
        for (
            pictograph
        ) in self.attr_box.attr_panel.filter_tab.scroll_area.pictographs.values():
            for motion in pictograph.motions.values():
                other_motion = pictograph.motions[RED if motion.color == BLUE else BLUE]
                if motion.is_dash() or motion.is_static():
                    if other_motion.is_shift():
                        if motion.motion_type == self.attr_box.motion_type:
                            if vtg_dir == SAME:
                                self.same_button.press()
                                self.opp_button.unpress()
                                motion.prop_rot_dir = other_motion.prop_rot_dir
                                pictograph_dict = {
                                    motion.color
                                    + "_"
                                    + PROP_ROT_DIR: other_motion.prop_rot_dir,
                                }
                                motion.scene.state_updater.update_pictograph(
                                    pictograph_dict
                                )
                            elif vtg_dir == OPP:
                                self.same_button.unpress()
                                self.opp_button.press()
                                if other_motion.prop_rot_dir == CLOCKWISE:
                                    motion.prop_rot_dir = COUNTER_CLOCKWISE
                                    pictograph_dict = {
                                        motion.color
                                        + "_"
                                        + PROP_ROT_DIR: COUNTER_CLOCKWISE,
                                    }
                                    motion.scene.state_updater.update_pictograph(
                                        pictograph_dict
                                    )
                                elif other_motion.prop_rot_dir == COUNTER_CLOCKWISE:
                                    motion.prop_rot_dir = CLOCKWISE
                                    pictograph_dict = {
                                        motion.color + "_" + PROP_ROT_DIR: CLOCKWISE,
                                    }
                                    motion.scene.state_updater.update_pictograph(
                                        pictograph_dict
                                    )

    def _set_prop_rot_dir(self, prop_rot_dir: VtgDirections) -> None:
        for (
            pictograph
        ) in self.attr_box.attr_panel.filter_tab.scroll_area.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.motion_type in [DASH, STATIC]:
                    if motion.motion_type == self.attr_box.motion_type:
                        pictograph_dict = {
                            f"{motion.color}_prop_rot_dir": prop_rot_dir,
                        }
                        motion.scene.state_updater.update_pictograph(pictograph_dict)
        if prop_rot_dir:
            if prop_rot_dir == CLOCKWISE:
                self.cw_button.press()
                self.ccw_button.unpress()
            elif prop_rot_dir == COUNTER_CLOCKWISE:
                self.cw_button.unpress()
                self.ccw_button.press()
        else:
            self.cw_button.unpress()
            self.ccw_button.unpress()

    def show_vtg_dir_buttons(self) -> None:
        for i in range(len(self.prop_rot_dir_buttons)):
            self.attr_box.header_widget.layout.replaceWidget(
                self.prop_rot_dir_buttons[i], self.vtg_dir_buttons[i]
            )
            self.prop_rot_dir_buttons[i].hide()
            self.vtg_dir_buttons[i].show()

    def show_prop_rot_dir_buttons(self) -> None:
        for i in range(len(self.vtg_dir_buttons)):
            self.attr_box.header_widget.layout.replaceWidget(
                self.vtg_dir_buttons[i], self.prop_rot_dir_buttons[i]
            )
            self.vtg_dir_buttons[i].hide()
            self.prop_rot_dir_buttons[i].show()

    def hide_buttons(self) -> None:
        for button in self.prop_rot_dir_buttons + self.vtg_dir_buttons:
            button.hide()
