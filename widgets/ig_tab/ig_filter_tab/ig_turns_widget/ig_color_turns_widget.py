from PyQt6.QtWidgets import (
    QLabel,
    QFrame,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Union
from constants import (
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    ICON_DIR,
    NO_ROT,
    STATIC,
)
from objects.motion.motion import Motion
from objects.pictograph.pictograph import Pictograph
from widgets.attr_box_widgets.base_turns_widget import (
    BaseTurnsWidget,
)


if TYPE_CHECKING:
    from widgets.ig_tab.ig_filter_tab.by_color.ig_color_attr_box import IGColorAttrBox
from PyQt6.QtCore import pyqtBoundSignal


class IGColorTurnsWidget(BaseTurnsWidget):
    def __init__(self, attr_box: "IGColorAttrBox") -> None:
        super().__init__(attr_box)
        self._initialize_ui()


    def add_black_borders(self) -> None:
        self.setStyleSheet(
            f"{self.styleSheet()} border: 1px solid black; border-radius: 0px;"
        )

    def _create_frames(self) -> None:
        self.turnbox_frame = self.create_turnbox_frame(QVBoxLayout())
        self.subtract_button_frame = self.create_button_frame(
            self.subtract_turns_buttons
        )
        self.add_button_frame = self.create_button_frame(self.add_turns_buttons)

    def setup_turns_label(self) -> None:
        self.turns_label = QLabel("Turns", self)
        self.turns_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turnbox_frame.layout().addWidget(self.turns_label)

    def setup_turnbox(self) -> None:
        self.turnbox_frame.layout().addWidget(self.turnbox)
        self.set_layout_margins_and_alignment()

    def _add_frames_to_main_layout(self) -> None:
        main_frame = QFrame()
        main_frame.setLayout(self.main_hbox_layout)
        self.main_hbox_layout.addWidget(self.subtract_button_frame)
        self.main_hbox_layout.addWidget(self.turnbox_frame)
        self.main_hbox_layout.addWidget(self.add_button_frame)

        self.layout.addWidget(main_frame)

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

    def connect_signals(self) -> None:
        self.turnbox.currentIndexChanged.connect(self.update_turns_directly)

    def update_turns_incrementally(self, adjustment: float) -> None:
        self.disconnect_signal(self.turnbox.currentIndexChanged)
        self.process_turns_for_all_motions(adjustment)
        self.connect_signal(self.turnbox.currentIndexChanged)

    def process_turns_for_all_motions(self, adjustment: float) -> None:
        for pictograph in self.attr_box.get_pictographs():
            self.process_single_motion(
                pictograph.motions[self.attr_box.color], adjustment
            )

    def connect_signal(self, signal: pyqtBoundSignal) -> None:
        signal.connect(self.update_turns_directly)

    def disconnect_signal(self, signal: pyqtBoundSignal) -> None:
        signal.disconnect(self.update_turns_directly)

    def process_single_motion(self, motion: Motion, adjustment: float) -> None:
        initial_turns = motion.turns
        new_turns = self._calculate_new_turns(motion.turns, adjustment)
        self.update_turns_display(new_turns)

        motion.set_turns(new_turns)

        if motion.is_dash_or_static() and self._turns_added(initial_turns, new_turns):
            self._simulate_cw_button_click()
        pictograph_dict = {
            f"{motion.color}_turns": new_turns,
        }
        motion.scene.update_pictograph(pictograph_dict)

    def _calculate_new_turns(self, current_turns, adjustment):
        return max(0, min(3, current_turns + adjustment))

    def update_turns_display(self, turns: Union[int, float]) -> None:
        turns_str = self.format_turns(turns)
        self.turnbox.setCurrentText(turns_str)

    @staticmethod
    def format_turns(turns: Union[int, float]) -> str:
        return str(int(turns)) if turns.is_integer() else str(turns)

    def _simulate_cw_button_click(self) -> None:
        self.attr_box.prop_rot_dir_widget.cw_button.setChecked(True)
        self.attr_box.prop_rot_dir_widget.cw_button.click()

    def _turns_added(self, initial_turns, new_turns):
        return initial_turns == 0 and new_turns > 0

    def _get_current_prop_rot_dir(self) -> str:
        return (
            CLOCKWISE
            if self.attr_box.prop_rot_dir_widget.cw_button.isChecked()
            else COUNTER_CLOCKWISE
            if self.attr_box.prop_rot_dir_widget.ccw_button.isChecked()
            else NO_ROT
        )


    def _update_pictographs_turns(self, new_turns):
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.color == self.attr_box.color:
                    motion.set_turns(new_turns)

                    if motion.motion_type in [DASH, STATIC] and (
                        motion.prop_rot_dir == NO_ROT and motion.turns > 0
                    ):
                        motion.manipulator.set_prop_rot_dir(
                            self._get_current_prop_rot_dir()
                        )
                        pictograph_dict = {
                            f"{motion.color}_turns": new_turns,
                            f"{motion.color}_prop_rot_dir": self._get_current_prop_rot_dir(),
                        }
                    else:
                        pictograph_dict = {
                            f"{motion.color}_turns": new_turns,
                        }
                    motion.scene.update_pictograph(pictograph_dict)

    ### EVENT HANDLERS ###

    def update_ig_color_turnbox_size(self) -> None:
        self.spacing = self.attr_box.attr_panel.width() // 250
        border_radius = min(self.turnbox.width(), self.turnbox.height()) * 0.25
        box_font_size = int(self.attr_box.width() / 14)
        dropdown_arrow_width = int(self.width() * 0.075)  # Width of the dropdown arrow
        border_radius = min(self.turnbox.width(), self.turnbox.height()) * 0.25
        turns_label_font = QFont("Arial", int(self.width() / 25))
        turnbox_font = QFont("Arial", box_font_size, QFont.Weight.Bold)

        self.turnbox.setMinimumHeight(int(self.attr_box.width() / 8))
        self.turnbox.setMaximumHeight(int(self.attr_box.width() / 8))
        self.turnbox.setMinimumWidth(int(self.attr_box.width() / 4))
        self.turnbox.setMaximumWidth(int(self.attr_box.width() / 4))
        self.turns_label.setContentsMargins(0, 0, self.spacing, 0)
        self.turns_label.setFont(turns_label_font)
        self.turnbox.setFont(turnbox_font)

        # Adjust the stylesheet to add padding inside the combo box on the left
        self.turnbox.setStyleSheet(
            f"""
            QComboBox {{
                padding-left: 2px; /* add some padding on the left for the text */
                padding-right: 0px; /* make room for the arrow on the right */
                border: {self.attr_box.combobox_border}px solid black;
                border-radius: {border_radius}px;
            }}
            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: {dropdown_arrow_width}px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid; /* visually separate the arrow part */
                border-top-right-radius: {border_radius}px;
                border-bottom-right-radius: {border_radius}px;
            }}
            QComboBox::down-arrow {{
                image: url("{ICON_DIR}/combobox_arrow.png");
                width: {int(dropdown_arrow_width * 0.6)}px;
                height: {int(dropdown_arrow_width * 0.6)}px;
            }}
        """
        )

    def update_ig_color_turns_button_size(self) -> None:
        for turns_button in self.turns_buttons:
            button_size = self.calculate_turns_button_size()
            turns_button.update_attr_box_turns_button_size(button_size)

    def calculate_turns_button_size(self) -> int:
        return int(self.attr_box.width() / 10)

    def resize_turns_widget(self) -> None:
        self.update_ig_color_turnbox_size()
        self.update_ig_color_turns_button_size()

    def _adjust_turns_callback(self, adjustment: float) -> None:
        self.update_turns_incrementally(adjustment)
