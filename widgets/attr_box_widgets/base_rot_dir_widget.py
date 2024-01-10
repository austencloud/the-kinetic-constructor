from PyQt6.QtWidgets import (
    QLabel,
)
from PyQt6.QtCore import Qt

from typing import TYPE_CHECKING, List, Union
from widgets.attr_box_widgets.base_attr_box_widget import (
    BaseAttrBoxWidget,
)

if TYPE_CHECKING:
    from widgets.graph_editor_tab.graph_editor_header_widget import (
        GraphEditorHeaderWidget,
    )
    from widgets.ig_tab.ig_filter_tab.by_motion_type.ig_motion_type_header_widget import (
        IGMotionTypeHeaderWidget,
    )
    from widgets.ig_tab.ig_filter_tab.by_motion_type.ig_motion_type_attr_box import (
        IGMotionTypeAttrBox,
    )
    from widgets.graph_editor_tab.graph_editor_attr_box import (
        GraphEditorAttrBox,
    )
from constants import BLUE, CLOCKWISE, COUNTER_CLOCKWISE, DASH, HEX_BLUE, HEX_RED, ICON_DIR, RED, STATIC
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton


class BaseRotDirWidget(BaseAttrBoxWidget):
    def __init__(
        self: Union["GraphEditorHeaderWidget", "IGMotionTypeHeaderWidget"],
        attr_box: Union["GraphEditorAttrBox", "IGMotionTypeAttrBox"],
    ) -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.prop_rot_dir_buttons = self._setup_prop_rot_dir_buttons()

        self.setMinimumWidth(self.attr_box.width())

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
                    if motion.arrow.lead_state == self.attr_box.lead_state:
                        pictograph_dict = {
                            f"{motion.color}_prop_rot_dir": prop_rot_dir,
                        }
                        motion.scene.update_pictograph(pictograph_dict)

        if prop_rot_dir:
            self.cw_button.setStyleSheet(
                self.get_button_style(pressed=prop_rot_dir == CLOCKWISE)
            )
            self.ccw_button.setStyleSheet(
                self.get_button_style(pressed=prop_rot_dir == COUNTER_CLOCKWISE)
            )
        else:
            self.cw_button.setStyleSheet(self.get_button_style(pressed=False))
            self.ccw_button.setStyleSheet(self.get_button_style(pressed=False))


    def _setup_prop_rot_dir_buttons(self) -> List[QPushButton]:
        self.cw_button = self._create_button(
            f"{ICON_DIR}clock/clockwise.png", lambda: self._set_prop_rot_dir(CLOCKWISE)
        )
        self.ccw_button = self._create_button(
            f"{ICON_DIR}clock/counter_clockwise.png",
            lambda: self._set_prop_rot_dir(COUNTER_CLOCKWISE),
        )

        self.cw_button.setStyleSheet(self.get_button_style(pressed=True))
        self.ccw_button.setStyleSheet(self.get_button_style(pressed=False))
        self.cw_button.setCheckable(True)
        self.ccw_button.setCheckable(True)
        self.cw_button.setChecked(True)

        buttons = [self.cw_button, self.ccw_button]
        return buttons

    def _simulate_cw_button_click(self) -> None:
        self.cw_button.setChecked(True)
        self.ccw_button.click()
