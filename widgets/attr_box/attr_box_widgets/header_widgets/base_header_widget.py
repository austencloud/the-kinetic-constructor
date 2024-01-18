from typing import TYPE_CHECKING
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt

from widgets.attr_box.attr_box_widgets.base_attr_box_widget import AttrBoxWidget


if TYPE_CHECKING:
    from widgets.attr_box.base_attr_box import BaseAttrBox

from PyQt6.QtWidgets import QFrame
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, List
from utilities.TypeChecking.TypeChecking import VtgDirections
from widgets.buttons.prop_rot_dir_button import PropRotDirButton
from widgets.buttons.vtg_dir_button import VtgDirButton

if TYPE_CHECKING:
    pass
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

class HeaderWidget(AttrBoxWidget):
    def __init__(self, attr_box) -> None:
        super().__init__(attr_box)
        self.attr_box: "BaseAttrBox" = attr_box
        self.setMinimumWidth(self.attr_box.width())
        self.header_label: QLabel = None
        self.separator: QFrame = self.create_separator()

    def create_separator(self) -> QFrame:
        separator = QFrame(self)
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Raised)
        separator.setStyleSheet("color: #000000;")
        return separator

    def _setup_layout(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.addStretch(1)
        self.layout.addWidget(self.header_label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.separator)

    def _setup_layout_with_vtg_dir_buttons(self) -> None:
        self.layout = QHBoxLayout(self)
        self.layout.addStretch(5)
        self.layout.addWidget(self.same_button)
        self.layout.addStretch(1)
        self.layout.addWidget(self.header_label)
        self.layout.addStretch(1)
        self.layout.addWidget(self.opp_button)
        self.layout.addStretch(5)
        self.layout.addWidget(self.separator)

    def _setup_header_label(self, text) -> QLabel:
        font_color = ""
        font_size = 30
        font_weight = "bold"

        if text == "Left":
            font_color = "#2E3192"
        elif text == "Right":
            font_color = "#ED1C24"
        else:
            font_color = "#000000"

        label = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(
            f"color: {font_color}; font-size: {font_size}px; font-weight: {font_weight};"
        )
        return label

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
        for pictograph in self.attr_box.attr_panel.parent_tab.scroll_area.pictographs.values():
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
        for pictograph in self.attr_box.attr_panel.parent_tab.scroll_area.pictographs.values():
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
