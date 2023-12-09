from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QFrame,
    QSpacerItem,
    QSizePolicy,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from typing import TYPE_CHECKING, Dict, Literal
from settings.string_constants import CLOCKWISE_ICON, COUNTER_CLOCKWISE_ICON

from widgets.graph_editor.attr_panel.custom_button import CustomButton

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox

class TurnsWidget(QFrame):
    def __init__(self, attr_box: "AttrBox") -> None:
        super().__init__()
        self.pictograph = attr_box.pictograph
        self.color = attr_box.color
        self.attr_box = attr_box
        self._init_ui()

    def _init_ui(self) -> None:
        self.setFixedWidth(
            self.attr_box.attr_box_width - self.attr_box.border_width * 2
        )
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Create header and buttons layout
        self.header_layout = self._create_header_layout()
        self.buttons_layout = self._create_buttons_layout()

        # Wrap header and buttons layout in frames
        self.header_frame = QFrame()
        self.buttons_frame = QFrame()

        # Set layout for frames
        self.header_frame.setLayout(self.header_layout)
        self.buttons_frame.setLayout(self.buttons_layout)

        self.header_frame.setFixedSize(
            self.attr_box.attr_box_width, self.turnbox_frame.height()
        )
        self.buttons_frame.setFixedSize(
            self.attr_box.attr_box_width, self.buttons_frame.sizeHint().height()
        )

        # Add frames to main layout
        self.layout.addWidget(self.header_frame)
        self.layout.addWidget(self.buttons_frame)

    def _create_header_layout(self) -> QHBoxLayout:
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(0)

        self.clock_left = QLabel()
        self.clock_right = QLabel()

        # Ensure that clocks expand to fill available space and are centered
        self.clock_left.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.clock_right.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )

        self.clock_left.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clock_right.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.turnbox_frame = self._setup_turnbox_frame()

        self.clock_left.setFixedHeight(self.turnbox_frame.height())
        self.clock_right.setFixedHeight(self.turnbox_frame.height())

        # Load pixmaps for clocks
        self.clockwise_pixmap = self.load_clock_pixmap(CLOCKWISE_ICON)
        self.counter_clockwise_pixmap = self.load_clock_pixmap(COUNTER_CLOCKWISE_ICON)

        # Add widgets to the layout, the clocks will expand as needed
        header_layout.addWidget(self.clock_left)
        header_layout.addWidget(self.turnbox_frame, 1)
        header_layout.addWidget(self.clock_right)

        return header_layout

    def _create_buttons_layout(self) -> QHBoxLayout:
        # Create buttons layout
        buttons_layout = QHBoxLayout()
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

        buttons_layout.addWidget(self.subtract_turn_button)
        buttons_layout.addWidget(self.subtract_half_turn_button)
        buttons_layout.addWidget(self.add_half_turn_button)
        buttons_layout.addWidget(self.add_turn_button)

        return buttons_layout

    def _adjust_height(self) -> None:
        # Adjust the height of the widget based on the combined height of header and buttons frames
        total_height = (
            self.header_frame.sizeHint().height()
            + self.buttons_frame.sizeHint().height()
        )
        self.setFixedHeight(total_height)

    def load_clock_pixmap(self, icon_path: str) -> QPixmap:
        """Load and scale a clock pixmap."""
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            print(f"Failed to load the icon from {icon_path}.")
            return QPixmap()
        return pixmap.scaled(
            int(self.turnbox_frame.height() * 0.8),
            int(self.turnbox_frame.height() * 0.8),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

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

    def _add_borders(self) -> None:
        self.setStyleSheet("border: 1px solid black;")
        self.turnbox_frame.setStyleSheet("border: 1px solid black;")

    ### CREATE WIDGETS ###

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
        turns_label.setFont(QFont("Arial", int(self.width() / 8), QFont.Weight.Bold))
        self.border_width = 2
        turns_label.setStyleSheet(
            f"background-color: white; border: {self.border_width}px solid black; border-radius: 10px; letter-spacing: -2px;"
        )
        turns_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        turns_label.setFixedSize(
            int(self.attr_box.attr_box_width * 0.3),
            int(self.attr_box.attr_box_width * 0.2),
        )
        turns_label.setContentsMargins(0, 0, 0, 0)
        return turns_label

    def _create_turns_button(
        self, text: Literal["+1", "-1", "+0.5", "-0.5"], callback, is_full_turn: bool
    ) -> CustomButton:
        button_size = int(self.attr_box.attr_box_width * 0.2)
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
        self.turnbox_header.setFont(QFont("Arial", int(self.width() / 14)))
        self.turns_label = self._create_turns_label()
        turnbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        turnbox_layout.addWidget(self.turnbox_header)
        turnbox_layout.addWidget(self.turns_label)
        # set maximum width to width of box
        turnbox_frame.setMaximumWidth(self.turns_label.width() + self.border_width)
        turnbox_frame.setFixedHeight(
            self.turns_label.height() + self.turnbox_header.height()
        )
        return turnbox_frame

    def _setup_turns_header(self) -> QLabel:
        turnbox_header = QLabel("Turns", self)
        turnbox_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        turnbox_header.setFont(QFont("Arial", int(self.width() / 14)))
        turnbox_header.setFixedHeight(int(self.width() / 14))
        return turnbox_header

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
            self.attr_box.update_labels(motion)

    def _subtract_turn_callback(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.subtract_turn()
            self.attr_box.update_labels(motion)

    def _add_half_turn_callback(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.add_half_turn()
            self.attr_box.update_labels(motion)

    def _subtract_half_turn_callback(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            motion.subtract_half_turn()
            self.attr_box.update_labels(motion)

    ### UPDATERS ###

    def clear_turns_label(self) -> None:
        self.turns_label.setText("")

    def update_turns_label_box(self, motion) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion and motion.turns is not None:
            self.turns_label.setText(str(motion.turns))
        else:
            self.turns_label.setText("")

    def update_turns_widget_size(self) -> None:
        self.setFixedWidth(self.attr_box.attr_box_width)
