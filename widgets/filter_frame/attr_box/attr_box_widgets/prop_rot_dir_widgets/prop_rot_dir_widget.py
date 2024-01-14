from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QPushButton, QSizePolicy, QLabel
from PyQt6.QtGui import QIcon
from typing import TYPE_CHECKING, List, Union

from constants import (
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    ICON_DIR,
    LEADING,
    NO_ROT,
    STATIC,
)
from widgets.filter_frame.attr_box.attr_box_widgets.base_attr_box_widget import BaseAttrBoxWidget

if TYPE_CHECKING:
    from widgets.graph_editor_tab.graph_editor_attr_box import GraphEditorAttrBox
    from widgets.filter_frame.attr_box.motion_type_attr_box import MotionTypeAttrBox
    

class PropRotDirWidget(BaseAttrBoxWidget):
    def __init__(
        self,
        attr_box: Union["GraphEditorAttrBox", "MotionTypeAttrBox"],
    ) -> None:
        super().__init__(attr_box)
        self.attr_box: Union["GraphEditorAttrBox", "MotionTypeAttrBox"] = attr_box
        self.same_opp_buttons = self._setup_prop_rot_dir_buttons()

        self.setMinimumWidth(self.attr_box.width())

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
        self._setup_rot_dir_widget()

    def _create_button(self, icon_path, action) -> QPushButton:
        button = QPushButton("", self)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(button.size())
        button.clicked.connect(action)
        button.setContentsMargins(0, 0, 0, 0)
        return button

    def _setup_header_label(self) -> QLabel:
        text = "Leading" if self.attr_box.lead_state == LEADING else "Trailing"
        label = QLabel(text, self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(f"font-weight: bold;")
        return label

    ### EVENT HANDLERS ###

    def update_button_size(self) -> None:
        button_size = self.width() // 3
        for prop_rot_dir_button in self.prop_rot_dir_buttons:
            prop_rot_dir_button.setMinimumSize(button_size, button_size)
            prop_rot_dir_button.setMaximumSize(button_size, button_size)
            prop_rot_dir_button.setIconSize(prop_rot_dir_button.size() * 0.9)

    def resize_prop_rot_dir_widget(self) -> None:
        self.update_button_size()

    def _get_current_prop_rot_dir(self) -> str:
        return (
            CLOCKWISE
            if self.attr_box.prop_rot_dir_widget.cw_button.isChecked()
            else COUNTER_CLOCKWISE
            if self.attr_box.prop_rot_dir_widget.ccw_button.isChecked()
            else NO_ROT
        )

    def _setup_rot_dir_widget(self) -> None:
        rot_dir_layout = QVBoxLayout()
        rot_dir_label = QLabel("Dash/Static\nRot Dir:", self)
        rot_dir_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rot_dir_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rot_dir_layout.addWidget(rot_dir_label)
        rot_dir_layout.addWidget(self.ccw_button)
        rot_dir_layout.addWidget(self.cw_button)
        self.layout.addLayout(rot_dir_layout)

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
            self.ccw_button.setChecked(True)
            self.cw_button.setChecked(False)
        elif prop_rot_dir == CLOCKWISE:
            self.cw_button.setChecked(True)
            self.ccw_button.setChecked(False)

        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.motion_type in [DASH, STATIC]:
                    if motion.arrow.motion.lead_state == self.attr_box.lead_state:
                        pictograph_dict = {
                            f"{motion.color}_prop_rot_dir": prop_rot_dir,
                        }
                        motion.scene.update_pictograph(pictograph_dict)

        if prop_rot_dir:
            self.cw_button.setStyleSheet(
                self.get_vtg_dir_btn_style(pressed=prop_rot_dir == CLOCKWISE)
            )
            self.ccw_button.setStyleSheet(
                self.get_vtg_dir_btn_style(pressed=prop_rot_dir == COUNTER_CLOCKWISE)
            )
        else:
            self.cw_button.setStyleSheet(self.get_vtg_dir_btn_style(pressed=False))
            self.ccw_button.setStyleSheet(self.get_vtg_dir_btn_style(pressed=False))

    def _setup_prop_rot_dir_buttons(self) -> List[QPushButton]:
        self.cw_button = self._create_button(
            f"{ICON_DIR}clock/clockwise.png", lambda: self._set_prop_rot_dir(CLOCKWISE)
        )
        self.ccw_button = self._create_button(
            f"{ICON_DIR}clock/counter_clockwise.png",
            lambda: self._set_prop_rot_dir(COUNTER_CLOCKWISE),
        )

        self.cw_button.setStyleSheet(self.get_vtg_dir_btn_style(pressed=True))
        self.ccw_button.setStyleSheet(self.get_vtg_dir_btn_style(pressed=False))
        self.cw_button.setCheckable(True)
        self.ccw_button.setCheckable(True)
        self.cw_button.setChecked(True)

        buttons = [self.cw_button, self.ccw_button]
        return buttons

    def _simulate_cw_button_click(self) -> None:
        self.cw_button.setChecked(True)
        self.ccw_button.click()
