from PyQt6.QtWidgets import (
    QLabel,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from typing import TYPE_CHECKING, List
from constants import (
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    ICON_DIR,
    NO_ROT,
    STATIC,
)


from widgets.attr_box_widgets.base_attr_box_widget import BaseAttrBoxWidget

if TYPE_CHECKING:
    from widgets.ig_tab.ig_filter_tab.by_lead_state.ig_lead_state_attr_box import IGLeadStateAttrBox

class IGLeadStatePropRotDirWidget(BaseAttrBoxWidget):
    def __init__(self, attr_box: "IGLeadStateAttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.initialize_ui()

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_vbox_layout = QVBoxLayout()
        self.main_vbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

    def initialize_ui(self) -> None:
        self._setup_layout()
        self.prop_rot_dir_buttons = self._setup_prop_rot_dir_buttons()
        self.setup_rot_dir_section()

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

    def setup_rot_dir_section(self) -> None:
        rot_dir_layout = QVBoxLayout()
        rot_dir_label = QLabel("Dash/Static\nRot Dir:", self)
        rot_dir_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rot_dir_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ccw_button.clicked.connect(self.ccw_button_clicked)
        self.cw_button.clicked.connect(self.cw_button_clicked)
        rot_dir_layout.addWidget(rot_dir_label)
        rot_dir_layout.addWidget(self.ccw_button)
        rot_dir_layout.addWidget(self.cw_button)
        self.layout.addLayout(rot_dir_layout)

    def ccw_button_clicked(self) -> None:
        pass

    def cw_button_clicked(self) -> None:
        pass

    def add_black_borders(self) -> None:
        self.setStyleSheet(
            f"{self.styleSheet()} border: 1px solid black; border-radius: 0px;"
        )

    def create_turnbox_frame(self, layout) -> QFrame:
        frame = QFrame()
        frame.setLayout(layout)
        self._configure_layout(layout)
        return frame

    def set_layout_margins_and_alignment(self) -> None:
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def create_button_frame(self, buttons) -> QFrame:
        frame = QFrame()
        layout = QVBoxLayout(frame)
        self._configure_layout(layout)
        for button in buttons:
            layout.addWidget(button)
        return frame

    def _configure_layout(self, layout: QVBoxLayout):
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(0)

    def _turns_added(self, initial_turns, new_turns):
        return initial_turns == 0 and new_turns > 0

    def _get_current_prop_rot_dir(self) -> str:
        return (
            CLOCKWISE
            if self.cw_button.isChecked()
            else COUNTER_CLOCKWISE
            if self.ccw_button.isChecked()
            else NO_ROT
        )

    ### EVENT HANDLERS ###

    def update_button_size(self) -> None:
        button_size = self.width() // 3
        for prop_rot_dir_button in self.prop_rot_dir_buttons:
            prop_rot_dir_button.setMinimumSize(button_size, button_size)
            prop_rot_dir_button.setMaximumSize(button_size, button_size)
            prop_rot_dir_button.setIconSize(prop_rot_dir_button.size() * 0.9)

    def resize_prop_rot_dir_widget(self) -> None:
        self.update_button_size()
