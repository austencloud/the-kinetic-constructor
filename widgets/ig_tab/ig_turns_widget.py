from PyQt6.QtWidgets import QLabel, QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Union
from constants import (
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    ICON_DIR,
    NO_ROT,
)
from objects.motion.motion import Motion
from objects.pictograph.pictograph import Pictograph
from widgets.attr_box_widgets.base_turns_widget import (
    BaseTurnsWidget,
)


if TYPE_CHECKING:
    from widgets.ig_tab.ig_attr_box import IGAttrBox
from PyQt6.QtCore import pyqtBoundSignal


class IGTurnsWidget(BaseTurnsWidget):
    def __init__(self, attr_box: "IGAttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self.initialize_ui()

    def initialize_ui(self) -> None:
        super()._initialize_ui()
        self._create_frames()
        self._add_frames_to_main_layout()
        self.setup_turns_label()
        self.setup_turnbox()
        self.connect_signals()
        self.add_black_borders()
        self.setup_directset_turns_buttons()  # Add this line to set up the new buttons

    def setup_directset_turns_buttons(self) -> None:
        """Set up the buttons for directly setting turns values."""
        turns_values = ["0", "0.5", "1", "1.5", "2", "2.5", "3"]
        self.turns_buttons_layout = QHBoxLayout()  # Horizontal layout for the buttons
        button_style_sheet = """
        QPushButton {
            background-color: #f0f0f0;
            border: 1px solid #c0c0c0;
            border-radius: 5px;
            padding: 5px;
            font-weight: bold;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #e5e5e5;
            border-color: #a0a0a0;
        }
        QPushButton:pressed {
            background-color: #d0d0d0;
        }
        """
        for value in turns_values:
            button = QPushButton(value, self)
            button.setStyleSheet(button_style_sheet)
            button.clicked.connect(lambda checked, v=value: self.set_turns_directly(v))
            self.turns_buttons_layout.addWidget(button)

        # Add the turns buttons layout to the bottom of the main layout
        self.layout.addLayout(self.turns_buttons_layout)

    def set_turns_directly(self, turns: float) -> None:
        """Directly set the turns value for the motion type."""
        if turns in ["0", "1", "2", "3"]:
            self.turnbox.setCurrentText(turns)
        elif turns in ["0.5", "1.5", "2.5"]:
            self.turnbox.setCurrentText(turns)
        self.update_turns_directly()  # This method will now be triggered with the new turns value


    def add_black_borders(self) -> None:
        self.setStyleSheet(
            f"{self.styleSheet()} border: 1px solid black; border-radius: 0px;"
        )

    def _create_frames(self) -> None:
        self.turnbox_frame = self.create_turnbox_frame(QVBoxLayout())
        self.decrement_button_frame = self.create_button_frame(self.decrement_buttons)
        self.increment_button_frame = self.create_button_frame(self.increment_buttons)

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
        self.main_hbox_layout.addWidget(self.decrement_button_frame)
        self.main_hbox_layout.addWidget(self.turnbox_frame)
        self.main_hbox_layout.addWidget(self.increment_button_frame)

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
            self.update_turns_for_pictograph(pictograph, adjustment)

    def update_turns_for_pictograph(
        self, pictograph: Pictograph, adjustment: float
    ) -> None:
        for motion in pictograph.get_motions_by_type(self.attr_box.motion_type):
            self.process_single_motion(motion, adjustment)

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

    def _simulate_cw_button_click(self):
        header_widget = self.attr_box.header_widget
        header_widget.cw_button.setChecked(True)
        header_widget.cw_button.click()

    def _turns_added(self, initial_turns, new_turns):
        return initial_turns == 0 and new_turns > 0

    def _get_current_prop_rot_dir(self) -> str:
        header_widget = self.attr_box.header_widget
        return (
            CLOCKWISE
            if header_widget.cw_button.isChecked()
            else COUNTER_CLOCKWISE
            if header_widget.ccw_button.isChecked()
            else NO_ROT
        )

    def update_turns_directly(self) -> None:
        selected_turns_str = self.turnbox.currentText()
        if not selected_turns_str:
            return

        new_turns = float(selected_turns_str)
        self._update_pictographs_turns(new_turns)

    def _update_pictographs_turns(self, new_turns):
        for pictograph in self.attr_box.pictographs.values():
            for motion in pictograph.motions.values():
                if motion.motion_type == self.attr_box.motion_type:
                    motion.set_turns(new_turns)
                    pictograph_dict = {
                        f"{motion.color}_turns": new_turns,
                    }
                    motion.scene.update_pictograph(pictograph_dict)

    ### EVENT HANDLERS ###

    def update_turnbox_size(self) -> None:
        self.spacing = self.attr_box.attr_panel.width() // 250
        border_radius = min(self.turnbox.width(), self.turnbox.height()) * 0.25
        box_font_size = int(self.attr_box.width() / 10)
        dropdown_arrow_width = int(self.width() * 0.075)  # Width of the dropdown arrow
        border_radius = min(self.turnbox.width(), self.turnbox.height()) * 0.25

        self.turnbox.setMinimumHeight(int(self.attr_box.height() / 4))
        self.turnbox.setMaximumHeight(int(self.attr_box.height() / 4))
        self.turnbox.setMinimumWidth(int(self.attr_box.width() / 3))
        self.turnbox.setMaximumWidth(int(self.attr_box.width() / 3))
        self.turnbox.setFont(QFont("Arial", box_font_size, QFont.Weight.Bold))

        # self.setMinimumWidth(self.attr_box.width() - self.attr_box.border_width * 2)
        # self.setMaximumWidth(self.attr_box.width() - self.attr_box.border_width * 2)

        self.turns_label.setContentsMargins(0, 0, self.spacing, 0)
        self.turns_label.setFont(QFont("Arial", int(self.width() / 22)))

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

    def update_button_size(self) -> None:
        for button in self.buttons:
            button_size = self.calculate_button_size()
            button.update_attr_box_button_size(button_size)

    def calculate_button_size(self) -> int:
        return int(self.attr_box.width() / 5)

    def resize_turns_widget(self) -> None:
        self.update_turnbox_size()
        self.update_button_size()

    def _adjust_turns_callback(self, adjustment: float) -> None:
        self.update_turns_incrementally(adjustment)
        
        