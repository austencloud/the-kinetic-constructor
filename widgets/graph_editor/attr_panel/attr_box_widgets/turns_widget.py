from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from typing import Literal, Dict, TYPE_CHECKING, Tuple
from objects.motion import Motion
from settings.string_constants import CLOCKWISE_ICON, COUNTER_CLOCKWISE_ICON, ICON_DIR
from widgets.graph_editor.attr_panel.attr_box_widgets.custom_combo_box import (
    CustomComboBox,
)

from widgets.graph_editor.attr_panel.custom_button import CustomButton

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class TurnsWidget(QFrame):
    def __init__(self, attr_box: "AttrBox") -> None:
        super().__init__()
        self.attr_box = attr_box
        self.clockwise_pixmap = self._load_clock_pixmap(CLOCKWISE_ICON)
        self.counter_clockwise_pixmap = self._load_clock_pixmap(COUNTER_CLOCKWISE_ICON)
        self._init_ui()

    def _init_ui(self) -> None:
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(0)

        self.header_frame = self._create_frame(self._create_clocks_and_turnbox_layout())
        self.buttons_frame = self._create_frame(self._create_buttons_layout())

        self.layout.addWidget(self.header_frame)
        self.layout.addWidget(self.buttons_frame)

        for clock in [self.clock_left, self.clock_right]:
            clock.setScaledContents(True)
        self.clock_left.clear()
        self.clock_right.clear()

    ### CREATE WIDGETS ###

    def _create_clocks_and_turnbox_layout(self) -> QHBoxLayout:
        clocks_and_turnbox_layout: QHBoxLayout = QHBoxLayout()
        clocks_and_turnbox_layout.setContentsMargins(0, 0, 0, 0)
        clocks_and_turnbox_layout.setSpacing(0)

        self.turnbox_frame = self._create_turnbox_frame()
        self.clock_left, self.clock_right = self._create_clock_labels()

        clocks_and_turnbox_layout.addWidget(self.clock_left)
        clocks_and_turnbox_layout.addWidget(self.turnbox_frame)
        clocks_and_turnbox_layout.addWidget(self.clock_right)
        return clocks_and_turnbox_layout

    def _create_clock_labels(self) -> Tuple[QLabel, QLabel]:
        clock_left, clock_right = QLabel(), QLabel()
        for clock in [clock_left, clock_right]:
            clock_layout = QVBoxLayout(clock)
            clock_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            clock.setPixmap(self.clockwise_pixmap)
            clock_size = int(
                (
                    (self.attr_box.attr_panel.width() / 2 - self.turnbox_frame.width())
                    / 2
                )
                * 0.7
            )
            clock.setMaximumSize(clock_size, clock_size)
            clock.setScaledContents(True)

        return clock_left, clock_right

    def _create_buttons_layout(self) -> QHBoxLayout:
        buttons_layout = QHBoxLayout()
        button_texts = ["-1", "-0.5", "+0.5", "+1"]
        callbacks = [
            self._subtract_turn_callback,
            self._subtract_half_turn_callback,
            self._add_half_turn_callback,
            self._add_turn_callback,
        ]

        for text, callback in zip(button_texts, callbacks):
            button = self._create_turns_button(text, callback, text in ["-1", "+1"])
            buttons_layout.addWidget(button)

        return buttons_layout

    def _create_frame(self, layout) -> QFrame:
        frame = QFrame()
        frame.setLayout(layout)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        return frame

    def _create_turnbox_frame(self) -> QFrame:
        turnbox_frame = QFrame(self)

        turnbox_layout = QVBoxLayout(turnbox_frame)
        turnbox_layout.setContentsMargins(0, 0, 0, 0)
        turnbox_layout.setSpacing(0)
        turnbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.turnbox_header = QLabel("Turns", self)
        self.turnbox_header.setFont(
            QFont("Arial", int(self.attr_box.attr_panel.width() / 35))
        )
        self.turnbox_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.turns_box = self._create_turns_box()
        turnbox_layout.addWidget(self.turnbox_header)
        turnbox_layout.addWidget(self.turns_box)

        turnbox_frame.setMaximumWidth(self.turns_box.width() + 2)  # border width

        return turnbox_frame

    def _create_buttons(self) -> None:
        self.subtract_turn_button = self._create_turns_button(
            "-1", self._subtract_turn_callback, is_full_turn=True
        )
        self.subtract_half_turn_button = self._create_turns_button(
            "-0.5", self._subtract_half_turn_callback, is_full_turn=False
        )
        self.add_half_turn_button = self._create_turns_button(
            "+0.5", self._add_half_turn_callback, is_full_turn=False
        )
        self.add_turn_button = self._create_turns_button(
            "+1", self._add_turn_callback, is_full_turn=True
        )

        top_layout = QHBoxLayout()
        bottom_layout = QHBoxLayout()

        self.layout.addLayout(top_layout)
        self.layout.addLayout(bottom_layout)

        top_layout.addWidget(self.turnbox_frame)

        bottom_layout.addWidget(self.subtract_turn_button)
        bottom_layout.addWidget(self.subtract_half_turn_button)
        bottom_layout.addWidget(self.add_half_turn_button)
        bottom_layout.addWidget(self.add_turn_button)

    def _create_turns_box(self) -> CustomComboBox:
        turns_box = CustomComboBox(self)
        turns_box.setFont(
            QFont(
                "Arial", int(self.attr_box.attr_panel.width() / 16), QFont.Weight.Bold
            )
        )

        turns_box.setContentsMargins(0, 0, 0, 0)

        # Populate the combo box with the specified turns choices
        turns_choices = [0.5, 1, 1.5, 2, 2.5, 3]
        for choice in turns_choices:
            turns_box.addItem(str(choice))  # Convert the number to a string

        return turns_box

    def _create_turns_button(
        self, text: Literal["+1", "-1", "+0.5", "-0.5"], callback, is_full_turn: bool
    ) -> CustomButton:
        button_size = int(self.attr_box.width() * 0.2)
        if not is_full_turn:
            button_size = int(button_size * 0.75)  # Half turn buttons are smaller

        button = CustomButton(self)
        button.setText(text)
        button.setFont(
            QFont("Arial", int(button_size / 3))
        )  # Adjust font size based on button size
        button.setMaximumSize(button_size, button_size)
        button.clicked.connect(callback)

        return button

    ### SETUP WIDGETS ###

    def _setup_button_frame(self, full_turn_button, half_turn_button) -> QFrame:
        # set a frame so that the buttons are stacked vertically
        button_frame = QFrame(self)
        button_frame_layout = QVBoxLayout(button_frame)
        button_frame_layout.setContentsMargins(0, 0, 0, 0)
        button_frame_layout.setSpacing(0)
        button_frame_layout.addWidget(full_turn_button)
        button_frame_layout.addWidget(half_turn_button)
        return button_frame

    def _setup_button_frames(self) -> Dict[str, QFrame]:
        button_frames = {}

        self.subtract_turn_button = self._create_turns_button(
            "-1", self._subtract_turn_callback
        )
        self.subtract_half_turn_button = self._create_turns_button(
            "-0.5", self._subtract_half_turn_callback
        )
        self.add_half_turn_button = self._create_turns_button(
            "+0.5", self._add_half_turn_callback
        )
        self.add_turn_button = self._create_turns_button("+1", self._add_turn_callback)

        subtract_button_frame = self._setup_button_frame(
            self.subtract_turn_button, self.subtract_half_turn_button
        )
        add_button_frame = self._setup_button_frame(
            self.add_turn_button, self.add_half_turn_button
        )

        button_frames["subtract_buttons"] = subtract_button_frame
        button_frames["add_buttons"] = add_button_frame

        return button_frames

    ### CALLBACKS ###

    def _add_turn_callback(self) -> None:
        motion = self.attr_box.pictograph.get_motion_by_color(self.attr_box.color)
        if motion:
            motion.add_turn()
            self.attr_box.update_attr_box(motion)

    def _subtract_turn_callback(self) -> None:
        motion = self.attr_box.pictograph.get_motion_by_color(self.attr_box.color)
        if motion:
            motion.subtract_turn()
            self.attr_box.update_attr_box(motion)

    def _add_half_turn_callback(self) -> None:
        motion = self.attr_box.pictograph.get_motion_by_color(self.attr_box.color)
        if motion:
            motion.add_half_turn()
            self.attr_box.update_attr_box(motion)

    def _subtract_half_turn_callback(self) -> None:
        motion = self.attr_box.pictograph.get_motion_by_color(self.attr_box.color)
        if motion:
            motion.subtract_half_turn()
            self.attr_box.update_attr_box(motion)

    ### UPDATERS ###

    def update_clocks(self, rotation_direction: str) -> None:
        """Update the visibility of clocks based on rotation direction."""
        if rotation_direction == "ccw":
            self.clock_left.setPixmap(self.counter_clockwise_pixmap)
            self.clock_right.clear()
        elif rotation_direction == "cw":
            self.clock_right.setPixmap(self.clockwise_pixmap)
            self.clock_left.clear()
        else:
            self.clock_left.clear()
            self.clock_right.clear()

    def clear_turns_label(self) -> None:
        self.turns_box.setText("")

    def update_turns_label_box(self, turns) -> None:
        if turns:
            self.turns_box.setText(str(turns))
        elif turns == 0:
            self.turns_box.setText("0")
        else:
            self.clear_turns_label()

    def resizeEvent(self, event) -> None:
        """Handle the resize event to update clock pixmaps."""
        super().resizeEvent(event)

    def _load_clock_pixmap(self, icon_path: str) -> QPixmap:
        """Load and scale a clock pixmap based on the initial size."""
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            print(f"Failed to load the icon from {icon_path}.")
            return QPixmap()
        return pixmap

    def update_turns_widget(self, motion: Motion) -> None:
        self.update_clocks(motion.rotation_direction)
        self.update_turns_label_box(
            self.attr_box.pictograph.get_motion_by_color(self.attr_box.color)
        )

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        border_radius = min(self.turns_box.width(), self.turns_box.height()) * 0.25
        self.turns_box.setMinimumWidth(int(self.attr_box.width() * 0.5))
        self.turns_box.setMinimumHeight(int(self.attr_box.width() / 5))
        self.turns_box.setMaximumHeight(int(self.attr_box.width() / 5))
        box_font_size = int(self.attr_box.width() / 10)

        self.turns_box.setFont(QFont("Arial", box_font_size, QFont.Weight.Bold, True))
        self.turns_box.setStyleSheet(
            f"""
            QComboBox {{
                border: {self.turns_box.combobox_border}px solid black;
                border-radius: {border_radius}px;
            }}

            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: {border_radius}px;
                border-bottom-right-radius: {border_radius}px;
            }}

            QComboBox::down-arrow {{
                image: url("{ICON_DIR}combobox_arrow.png");
                width: 10px;
                height: 10px;
            }}
            """
        )
