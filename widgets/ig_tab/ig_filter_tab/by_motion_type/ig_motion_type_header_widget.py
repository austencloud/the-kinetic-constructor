from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING, List
from utilities.TypeChecking.TypeChecking import MotionTypes, VtgDirections

from ....attr_box_widgets.base_header_widget import BaseHeaderWidget

if TYPE_CHECKING:
    from .ig_motion_type_attr_box import IGMotionTypeAttrBox
from constants import (
    ANTI,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    ICON_DIR,
    OPP,
    PRO,
    SAME,
    STATIC,
)


class IGMotionTypeHeaderWidget(BaseHeaderWidget):
    def __init__(
        self, attr_box: "IGMotionTypeAttrBox", motion_type: MotionTypes
    ) -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.motion_type = motion_type

        self.header_label = self._setup_header_label()
        self.separator = self.create_separator()

        if self.motion_type in [PRO, ANTI]:
            self._setup_pro_anti_layout()
        if self.motion_type in [DASH, STATIC]:
            self.same_opp_buttons = self._setup_prop_rot_dir_buttons()
            self._set_default_rotation_direction()
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
        header_layout.addStretch(3)
        header_layout.addWidget(self.same_opp_buttons[0])
        header_layout.addStretch(1)
        header_layout.addWidget(self.header_label)
        header_layout.addStretch(1)
        header_layout.addWidget(self.same_opp_buttons[1])
        header_layout.addStretch(3)
        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.separator)

    def _set_default_rotation_direction(self) -> None:
        has_turns = any(
            motion.turns > 0
            for pictograph in self.attr_box.pictographs.values()
            for motion in pictograph.motions.values()
            if motion.motion_type == DASH
        )
        self._set_vtg_direction(CLOCKWISE if has_turns else None)

    def _set_vtg_direction(self, vtg_direction: VtgDirections) -> None:
        prop_rot_dir = None
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.motion_type == self.attr_box.motion_type:
                    other_motion = (
                        pictograph.red_motion
                        if motion == pictograph.blue_motion
                        else pictograph.blue_motion
                    )
                    if motion.motion_type in [DASH, STATIC]:
                        if motion.turns > 0:
                            if vtg_direction is SAME:
                                motion.prop_rot_dir = other_motion.prop_rot_dir
                                prop_rot_dir = other_motion.prop_rot_dir
                            elif vtg_direction is OPP:
                                if other_motion.prop_rot_dir == CLOCKWISE:
                                    motion.prop_rot_dir = COUNTER_CLOCKWISE
                                    prop_rot_dir = COUNTER_CLOCKWISE
                                elif other_motion.prop_rot_dir == COUNTER_CLOCKWISE:
                                    motion.prop_rot_dir = CLOCKWISE
                                    prop_rot_dir = CLOCKWISE
                            else:
                                prop_rot_dir = None
                    if motion.turns > 0:
                        pictograph_dict = {
                            f"{motion.color}_prop_rot_dir": prop_rot_dir,
                        }
                        motion.scene.update_pictograph(pictograph_dict)

            if self.attr_box.motion_type in [DASH, STATIC]:
                self.same_button.setChecked(
                    prop_rot_dir == other_motion.prop_rot_dir
                    and prop_rot_dir is not None
                    and other_motion.prop_rot_dir is not None
                )
                self.opp_button.setChecked(
                    prop_rot_dir != other_motion.prop_rot_dir
                    and prop_rot_dir is not None
                    and other_motion.prop_rot_dir is not None
                )

                if prop_rot_dir:
                    self.same_button.setStyleSheet(
                        self.get_button_style(pressed=vtg_direction == SAME)
                    )
                    self.opp_button.setStyleSheet(
                        self.get_button_style(pressed=vtg_direction == OPP)
                    )
                else:
                    self.same_button.setStyleSheet(self.get_button_style(pressed=False))
                    self.opp_button.setStyleSheet(self.get_button_style(pressed=False))

    def _setup_prop_rot_dir_buttons(self) -> List[QPushButton]:
        self.same_button: QPushButton = self._create_button(
            f"{ICON_DIR}same_direction.png", lambda: self._set_vtg_direction(SAME)
        )
        self.opp_button: QPushButton = self._create_button(
            f"{ICON_DIR}opp_direction.png",
            lambda: self._set_vtg_direction(OPP),
        )

        self.same_button.setStyleSheet(self.get_button_style(pressed=True))
        self.opp_button.setStyleSheet(self.get_button_style(pressed=False))
        self.same_button.setCheckable(True)
        self.opp_button.setCheckable(True)

        buttons = [self.same_button, self.opp_button]
        return buttons

    def get_button_style(self, pressed: bool) -> str:
        if pressed:
            return """
                QPushButton {
                    background-color: #ccd9ff;
                    border: 2px solid #555555;
                    border-bottom-color: #888888; /* darker shadow on the bottom */
                    border-right-color: #888888; /* darker shadow on the right */
                    padding: 5px;
                }
            """
        else:
            return """
                QPushButton {
                    background-color: white;
                    border: 1px solid black;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #e6f0ff;
                }
            """

    def _create_button(self, icon_path, action) -> QPushButton:
        button = QPushButton("", self)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(button.size())
        button.clicked.connect(action)
        button.setContentsMargins(0, 0, 0, 0)
        return button

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
            for button in self.same_opp_buttons:
                button.setMinimumSize(button_size, button_size)
                button.setMaximumSize(button_size, button_size)
                button.setIconSize(button.size() * 0.9)
