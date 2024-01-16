from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QPushButton,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from typing import TYPE_CHECKING, List
from constants import (
    BLUE,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    HEX_BLUE,
    HEX_RED,
    ICON_DIR,
    NO_ROT,
    OPP,
    RED,
    SAME,
    STATIC,
)
from utilities.TypeChecking.TypeChecking import PropRotDirs, VtgDirections
from .base_attr_box_widget import BaseAttrBoxWidget

if TYPE_CHECKING:
    from ...attr_box.base_attr_box import BaseAttrBox


class VtgDirWidget(BaseAttrBoxWidget):
    def __init__(self, attr_box: "BaseAttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.setup_ui()

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_vbox_layout = QVBoxLayout()
        self.main_vbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

    def setup_ui(self) -> None:
        self._setup_layout()
        self.vtg_dir_buttons = self._setup_vtg_dir_buttons()
        self.setup_rot_dir_section()

    def _setup_vtg_dir_buttons(self) -> List[QPushButton]:
        self.same_button: QPushButton = self._create_button(
            f"{ICON_DIR}same_direction.png", lambda: self._set_vtg_dir(SAME)
        )
        self.opp_button: QPushButton = self._create_button(
            f"{ICON_DIR}opp_direction.png",
            lambda: self._set_vtg_dir(OPP),
        )

        self.same_button.setStyleSheet(self.get_dir_button_style(pressed=False))
        self.opp_button.setStyleSheet(self.get_dir_button_style(pressed=False))
        self.same_button.setCheckable(True)
        self.opp_button.setCheckable(True)

        buttons = [self.same_button, self.opp_button]
        return buttons

    def _set_vtg_dir(self, vtg_dir: VtgDirections) -> None:
        if vtg_dir == SAME:
            self.attr_box.vtg_dir_btn_state = {SAME: True, OPP: False}
        elif vtg_dir == OPP:
            self.attr_box.vtg_dir_btn_state = {SAME: False, OPP: True}
        prop_rot_dir: PropRotDirs = None
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                other_motion = (
                    pictograph.red_motion
                    if motion == pictograph.blue_motion
                    else pictograph.blue_motion
                )
                if motion.color == self.attr_box.color:
                    if motion.motion_type in [DASH, STATIC]:
                        if motion.turns > 0:
                            if vtg_dir is SAME:
                                motion.prop_rot_dir = other_motion.prop_rot_dir
                                prop_rot_dir = other_motion.prop_rot_dir
                            elif vtg_dir is OPP:
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

                if prop_rot_dir:
                    self.same_button.setStyleSheet(
                        self.get_dir_button_style(pressed=vtg_dir == SAME)
                    )
                    self.opp_button.setStyleSheet(
                        self.get_dir_button_style(pressed=vtg_dir == OPP)
                    )
                else:
                    self.same_button.setStyleSheet(
                        self.get_dir_button_style(pressed=False)
                    )
                    self.opp_button.setStyleSheet(
                        self.get_dir_button_style(pressed=False)
                    )

    def _set_default_rotation_direction(self):
        has_turns = any(
            motion.turns > 0
            for pictograph in self.attr_box.pictographs.values()
            for motion in pictograph.motions.values()
            if motion.motion_type == DASH
        )
        self._set_prop_rot_dir(CLOCKWISE if has_turns else None)

    def _set_prop_rot_dir(self, prop_rot_dir: str) -> None:
        if prop_rot_dir == COUNTER_CLOCKWISE:
            self.opp_button.setChecked(True)
            self.same_button.setChecked(False)
        elif prop_rot_dir == CLOCKWISE:
            self.same_button.setChecked(True)
            self.opp_button.setChecked(False)

        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.motion_type in [DASH, STATIC]:
                    if motion.color == self.attr_box.color:
                        pictograph_dict = {
                            f"{motion.color}_prop_rot_dir": prop_rot_dir,
                        }
                        motion.scene.update_pictograph(pictograph_dict)

        if prop_rot_dir:
            self.same_button.setStyleSheet(
                self.get_dir_button_style(pressed=prop_rot_dir == CLOCKWISE)
            )
            self.opp_button.setStyleSheet(
                self.get_dir_button_style(pressed=prop_rot_dir == COUNTER_CLOCKWISE)
            )
        else:
            self.same_button.setStyleSheet(self.get_dir_button_style(pressed=False))
            self.opp_button.setStyleSheet(self.get_dir_button_style(pressed=False))

    def _create_button(self, icon_path, action) -> QPushButton:
        button = QPushButton("", self)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(button.size())
        button.clicked.connect(action)
        button.setContentsMargins(0, 0, 0, 0)
        return button

    def setup_rot_dir_section(self) -> None:
        rot_dir_layout = QVBoxLayout()
        rot_dir_label = QLabel("Dash/Static\nRot Dir:", self)
        rot_dir_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rot_dir_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.opp_button.clicked.connect(self.opp_button_clicked)
        self.same_button.clicked.connect(self.cw_button_clicked)
        rot_dir_layout.addWidget(rot_dir_label)
        rot_dir_layout.addWidget(self.same_button)
        rot_dir_layout.addWidget(self.opp_button)
        self.layout.addLayout(rot_dir_layout)

    def opp_button_clicked(self) -> None:
        pass

    def cw_button_clicked(self) -> None:
        pass

    def add_black_borders(self) -> None:
        self.setStyleSheet(
            f"{self.styleSheet()} border: 1px solid black; border-radius: 0px;"
        )

    ### EVENT HANDLERS ###

    def update_button_size(self) -> None:
        button_size = self.width() // 3
        for prop_rot_dir_button in self.vtg_dir_buttons:
            prop_rot_dir_button.setMinimumSize(button_size, button_size)
            prop_rot_dir_button.setMaximumSize(button_size, button_size)
            prop_rot_dir_button.setIconSize(prop_rot_dir_button.size() * 0.9)

    def resize_prop_rot_dir_widget(self) -> None:
        self.update_button_size()

    def _setup_header_label(self) -> QLabel:
        text = "Left" if self.attr_box.color == BLUE else "Right"
        color_hex = HEX_RED if self.attr_box.color == RED else HEX_BLUE
        label = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"color: {color_hex}; font-weight: bold;")
        return label

    def _get_current_prop_rot_dir(self) -> str:
        return (
            CLOCKWISE
            if self.attr_box.same_button.isChecked()
            else COUNTER_CLOCKWISE
            if self.attr_box.opp_button.isChecked()
            else NO_ROT
        )
