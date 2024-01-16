from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING, List
from utilities.TypeChecking.TypeChecking import MotionTypes, PropRotDirs, VtgDirections
from widgets.buttons.prop_rot_dir_button import PropRotDirButton
from widgets.buttons.vtg_dir_button import VtgDirButton
from widgets.filter_frame.attr_box.attr_box_widgets.header_widgets.base_header_widget import (
    HeaderWidget,
)

if TYPE_CHECKING:
    from widgets.filter_frame.attr_box.motion_type_attr_box import MotionTypeAttrBox
from constants import (
    ANTI,
    BLUE,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    ICON_DIR,
    OPP,
    PRO,
    PROP_ROT_DIR,
    RED,
    SAME,
    STATIC,
    VTG_DIR,
)


class MotionTypeHeaderWidget(HeaderWidget):
    def __init__(self, attr_box, motion_type: MotionTypes) -> None:
        super().__init__(attr_box)
        self.attr_box: "MotionTypeAttrBox" = attr_box
        self.motion_type = motion_type

        self.header_label = self._setup_header_label()
        self.separator = self.create_separator()

        if self.motion_type in [PRO, ANTI]:
            self._setup_pro_anti_layout()
        if self.motion_type in [DASH, STATIC]:
            self.vtg_dir_buttons: List[VtgDirButton] = self._setup_vtg_dir_buttons()
            self.prop_rot_dir_buttons: List[PropRotDirButton] = self._setup_prop_rot_dir_buttons()
            # self._set_default_vtg_direction()
            self._setup_dash_static_layout()

    def _setup_pro_anti_layout(self) -> None:
        super()._setup_layout()
        header_layout = QHBoxLayout()
        header_layout.addStretch(1)
        header_layout.addWidget(self.header_label)
        header_layout.addStretch(1)
        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.separator)

    def _setup_dash_static_layout(self) -> None:
        super()._setup_layout()
        header_layout = QHBoxLayout()
        header_layout.addStretch(5)
        header_layout.addWidget(self.same_button)
        header_layout.addStretch(1)
        header_layout.addWidget(self.header_label)
        header_layout.addStretch(1)
        header_layout.addWidget(self.opp_button)
        header_layout.addStretch(5)
        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.separator)


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
        for pictograph in self.attr_box.pictographs.values():
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
                                    motion.color + "_" + PROP_ROT_DIR: other_motion.prop_rot_dir,
                                }
                                motion.scene.update_pictograph(pictograph_dict)
                            elif vtg_dir == OPP:
                                self.same_button.unpress()
                                self.opp_button.press()
                                if other_motion.prop_rot_dir == CLOCKWISE:
                                    motion.prop_rot_dir = COUNTER_CLOCKWISE
                                    pictograph_dict = {
                                        motion.color + "_" + PROP_ROT_DIR: COUNTER_CLOCKWISE,
                                    }
                                    motion.scene.update_pictograph(pictograph_dict)
                                elif other_motion.prop_rot_dir == COUNTER_CLOCKWISE:
                                    motion.prop_rot_dir = CLOCKWISE
                                    pictograph_dict = {
                                        motion.color + "_" + PROP_ROT_DIR: CLOCKWISE,
                                    }
                                    motion.scene.update_pictograph(pictograph_dict)

        


    def _set_prop_rot_dir(self, prop_rot_dir: VtgDirections) -> None:
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.motion_type in [DASH, STATIC]:
                    if motion.motion_type == self.attr_box.motion_type:
                        pictograph_dict = {
                            f"{motion.color}_prop_rot_dir": prop_rot_dir,
                        }
                        motion.scene.update_pictograph(pictograph_dict)
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

    def _setup_header_label(self) -> QLabel:
        font_size = 30
        font_weight = "bold"
        if self.motion_type == PRO:
            text = PRO.capitalize()
        elif self.motion_type == ANTI:
            text = ANTI.capitalize()
        elif self.motion_type == DASH:
            text = DASH.capitalize()
        elif self.motion_type == STATIC:
            text = STATIC.capitalize()
        label = QLabel(text, self)
        label.setStyleSheet(f"font-size: {font_size}px; font-weight: {font_weight};")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def resize_header_widget(self) -> None:
        self.setMinimumHeight(int(self.attr_box.height() / 4))
        self.setMaximumHeight(int(self.attr_box.height() / 4))

        if self.motion_type in [DASH, STATIC]:
            button_size = int(self.height() * 0.9)
            for button in self.vtg_dir_buttons + self.prop_rot_dir_buttons:
                button.setMinimumSize(button_size, button_size)
                button.setMaximumSize(button_size, button_size)
                button.setIconSize(button.size() * 0.9)
