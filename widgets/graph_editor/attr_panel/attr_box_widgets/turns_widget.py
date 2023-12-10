from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
    QPushButton,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from typing import Literal, Dict, TYPE_CHECKING, Tuple
from objects.motion import Motion
from settings.string_constants import CLOCKWISE_ICON, COUNTER_CLOCKWISE_ICON
from utilities.TypeChecking.TypeChecking import RotationDirections

from widgets.graph_editor.attr_panel.custom_button import CustomButton

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class TurnsWidget(QFrame):
    def __init__(self, attr_box: "AttrBox") -> None:
        super().__init__()
        self.pictograph = attr_box.pictograph
        self.color = attr_box.color
        self.attr_box: AttrBox = attr_box
        self.turnbox_frame_size = int(self.attr_box.width() * 0.3)
        self.turnbox_frame_height = int(self.attr_box.width() * 0.2)
        self.button_size = int(self.attr_box.width() * 0.2)
        # Load and scale pixmaps
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

        # Set clock labels to scale contents
        for clock in [self.clock_left, self.clock_right]:
            clock.setScaledContents(True)
        # hide the clocks
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
                * 0.8
            )
            clock.setFixedSize(clock_size, clock_size)  # Set fixed size
            clock.setScaledContents(True)  # Scale contents

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

        self.turns_label = self._create_turns_label()
        turnbox_layout.addWidget(self.turnbox_header)
        turnbox_layout.addWidget(self.turns_label)

        turnbox_frame.setMaximumWidth(self.turns_label.width() + 2)  # border width

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

    def _create_turns_label(self) -> QLabel:
        turns_label = QLabel("", self)
        turns_label.setFrameShape(QFrame.Shape.Box)
        turns_label.setLineWidth(1)
        turns_label.setFrameShadow(QFrame.Shadow.Plain)
        turns_label.setFont(
            QFont(
                "Arial", int(self.attr_box.attr_panel.width() / 16), QFont.Weight.Bold
            )
        )
        self.border_width = 2
        turns_label.setStyleSheet(
            f"background-color: white; border: {self.border_width}px solid black; border-radius: 10px; letter-spacing: -2px;"
        )
        turns_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        turns_label.setFixedSize(
            int(self.attr_box.width() * 0.3),
            int(self.attr_box.width() * 0.2),
        )
        turns_label.setContentsMargins(0, 0, 0, 0)
        return turns_label

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
        button.setFixedSize(button_size, button_size)
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

    def _setup_turnbox_frame(self) -> QFrame:
        turnbox_frame = QFrame(self)
        turnbox_layout = QVBoxLayout(turnbox_frame)
        turnbox_layout.setContentsMargins(0, 0, 0, 0)
        turnbox_frame.setContentsMargins(0, 0, 0, 0)
        turnbox_layout.setSpacing(0)
        self.turnbox_header = QLabel("Turns", self)
        self.turnbox_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.turnbox_header.setFont(
            QFont("Arial", int(self.attr_box.attr_panel.width() / 35))
        )
        self.turnbox_header.setContentsMargins(0, 0, 0, 0)
        self.turns_label = self._create_turns_label()
        turnbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        turnbox_layout.addWidget(self.turnbox_header)
        turnbox_layout.addWidget(self.turns_label)
        # set maximum width to width of box
        turnbox_frame.setMaximumWidth(self.turns_label.width() + self.border_width)
        turnbox_frame.setFixedHeight(
            self.turns_label.height()
            + self.turnbox_header.height()
            + self.border_width * 2
        )
        return turnbox_frame

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
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.add_turn()
            self.attr_box.update_attr_box(motion)

    def _subtract_turn_callback(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.subtract_turn()
            self.attr_box.update_attr_box(motion)

    def _add_half_turn_callback(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.add_half_turn()
            self.attr_box.update_attr_box(motion)

    def _subtract_half_turn_callback(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
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
        self.turns_label.setText("")

    def update_turns_label_box(self, turns) -> None:
        if turns:
            self.turns_label.setText(str(turns))
        elif turns == 0:
            self.turns_label.setText("0")
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
        self.update_turns_label_box(self.pictograph.get_motion_by_color(self.color))

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
