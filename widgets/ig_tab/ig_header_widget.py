from PyQt6.QtWidgets import QHBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING, List
from utilities.TypeChecking.TypeChecking import MotionTypes

from widgets.attr_box_widgets.base_header_widget import BaseHeaderWidget

if TYPE_CHECKING:
    from widgets.ig_tab.ig_attr_box import IGAttrBox
from constants import (
    ANTI,
    CLOCKWISE,
    DASH,
    ICON_DIR,
    PRO,
    STATIC,
)


class IGHeaderWidget(BaseHeaderWidget):
    def __init__(self, attr_box: "IGAttrBox", motion_type: MotionTypes) -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.motion_type = motion_type

        self.header_label = self._setup_header_label()
        self.separator = self.create_separator()

        if self.motion_type in [PRO, ANTI]:
            self._setup_pro_anti_layout()
        if self.motion_type in [DASH, STATIC]:
            self.prop_rot_dir_buttons = self._setup_prop_rot_dir_buttons()
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
        header_layout.addWidget(self.prop_rot_dir_buttons[0])
        header_layout.addStretch(1)
        header_layout.addWidget(self.header_label)
        header_layout.addStretch(1)
        header_layout.addWidget(self.prop_rot_dir_buttons[1])
        self.layout.addLayout(header_layout)
        self.layout.addWidget(self.separator)

    def _setup_prop_rot_dir_buttons(self) -> List[QPushButton]:
        self.cw_button = self._create_button(
            f"{ICON_DIR}clock/clockwise.png", lambda: self._set_prop_rot_dir(CLOCKWISE)
        )

        self.ccw_button = self._create_button(
            f"{ICON_DIR}clock/counter_clockwise.png",
            lambda: self._set_prop_rot_dir(ANTI),
        )

        buttons = [self.cw_button, self.ccw_button]
        return buttons

    def _create_button(self, icon_path, action) -> QPushButton:
        button = QPushButton("", self)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(button.size())
        button.clicked.connect(action)
        # button.setMinimumSize(self.height(), self.height())
        # button.setMaximumSize(self.height(), self.height())
        button.setContentsMargins(0, 0, 0, 0)  # Remove contents margin
        return button

    def _set_prop_rot_dir(self, direction: str) -> None:
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                motion.manipulator.set_prop_rot_dir(direction)

    def _setup_header_label(self) -> QLabel:
        text = ""
        if self.motion_type == PRO:
            text = PRO.capitalize()
        elif self.motion_type == ANTI:
            text = ANTI.capitalize()
        elif self.motion_type == DASH:
            text = DASH.capitalize()
        elif self.motion_type == STATIC:
            text = STATIC.capitalize()

        label = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return label

    def resize_header_widget(self) -> None:
        if self.motion_type in [DASH, STATIC]:
            for button in self.prop_rot_dir_buttons:
                button.setMinimumSize(self.height(), self.height())
                button.setMaximumSize(self.height(), self.height())
                button.setIconSize(button.size() * 0.8)
