from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
    QWidget,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from typing import TYPE_CHECKING, List, Tuple
from objects.motion import Motion
from settings.string_constants import CLOCKWISE_ICON, COUNTER_CLOCKWISE_ICON, ICON_DIR
from widgets.graph_editor.attr_panel.attr_box_widgets.attr_box_widget import (
    AttrBoxWidget,
)
from widgets.graph_editor.attr_panel.attr_box_widgets.custom_combo_box import (
    CustomComboBox,
)
from widgets.graph_editor.attr_panel.custom_button import CustomButton

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class TurnsWidget(AttrBoxWidget):
    def __init__(self, attr_box: "AttrBox") -> None:
        super().__init__(attr_box)
        self.clockwise_pixmap = self._create_clock_pixmap(CLOCKWISE_ICON)
        self.counter_clockwise_pixmap = self._create_clock_pixmap(
            COUNTER_CLOCKWISE_ICON
        )
        self._initialize_ui()

    def _initialize_ui(self) -> None:
        """Initializes the user interface components and their layout."""
        self._setup_layouts()
        self._create_clock_labels()
        self.turnbox_vbox_frame: QFrame = self._create_turnbox_vbox_frame()
        self._setup_layout_frames()
        self._apply_layout_settings()
        # Create the 'Turns' header label

    ### LAYOUTS ###

    def _setup_layouts(self) -> None:
        """Sets up the main and auxiliary layouts for the widget."""
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_layout = QHBoxLayout()
        self.buttons_layout = QHBoxLayout()

    def _setup_layout_frames(self) -> None:
        """Adds the header and buttons to their respective frames."""
        self._add_widgets_to_layout(
            [self.clock_left, self.turnbox_vbox_frame, self.clock_right],
            self.header_layout,
        )
        self._add_widgets_to_layout(self.buttons, self.buttons_layout)

        self.header_frame = self._create_frame(self.header_layout)
        self.button_frame = self._create_frame(self.buttons_layout)

        self.layout.addWidget(self.header_frame)
        self.layout.addWidget(self.button_frame)

    def _apply_layout_settings(self) -> None:
        """Applies settings to the layout and initializes the clocks."""
        self.setLayout(self.layout)
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        for clock in [self.clock_left, self.clock_right]:
            clock.setScaledContents(True)
            clock.clear()

    def _add_widgets_to_layout(
        self, widgets: List[QWidget], layout: QHBoxLayout | QVBoxLayout
    ) -> None:
        """Adds the given widgets to the specified layout."""
        for widget in widgets:
            layout.addWidget(widget)

    ### WIDGETS ###

    def _create_clock_labels(self) -> None:
        """Creates and configures the clock labels for rotation direction."""
        self.clock_left, self.clock_right = QLabel(), QLabel()
        for clock in [self.clock_left, self.clock_right]:
            clock.setLayout(QVBoxLayout())
            clock.setAlignment(Qt.AlignmentFlag.AlignCenter)
            clock.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )

    def _create_turnbox_vbox_frame(self) -> None:
        """Creates the turns box and buttons for turn adjustments."""
        self.turnbox = CustomComboBox(self)
        self.turnbox.addItems(["0", "0.5", "1", "1.5", "2", "2.5", "3"])
        self.turnbox.currentTextChanged.connect(self._update_turns)

        self.turnbox.setCurrentIndex(-1)
        self.buttons = [
            self._create_turns_button(text) for text in ["-1", "-0.5", "+0.5", "+1"]
        ]
        turnbox_frame = QFrame(self)
        turnbox_frame.setLayout(QVBoxLayout())

        self.header_label = QLabel("Turns")
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        turnbox_frame.layout().addWidget(self.header_label)
        turnbox_frame.layout().addWidget(self.turnbox)
        turnbox_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        turnbox_frame.layout().setContentsMargins(0, 0, 0, 0)
        turnbox_frame.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        turnbox_frame.layout().setSpacing(0)
        return turnbox_frame

    def _create_frame(self, layout: QHBoxLayout | QVBoxLayout) -> QFrame:
        """Creates a frame with the given layout."""
        frame = QFrame()
        frame.setLayout(layout)
        frame.setContentsMargins(0, 0, 0, 0)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        return frame

    def _create_clock_pixmap(self, icon_path: str) -> QPixmap:
        """Load and scale a clock pixmap based on the initial size."""
        pixmap = QPixmap(icon_path)
        if pixmap.isNull():
            print(f"Failed to load the icon from {icon_path}.")
            return QPixmap()
        return pixmap

    def _create_turns_button(self, text: str) -> CustomButton:
        """Creates a turn adjustment button with specified text."""
        button_size = int(self.attr_box.width() * 0.2)
        if text in ["-1", "+1"]:
            button_size = int(button_size * 0.75)  # Half turn buttons are smaller

        button = CustomButton(self)
        button.setText(text)
        button.setFont(QFont("Arial", int(button_size / 3)))
        # Set the appropriate callback based on the button text
        if text == "-1":
            button.clicked.connect(self._subtract_turn_callback)
        elif text == "-0.5":
            button.clicked.connect(self._subtract_half_turn_callback)
        elif text == "+0.5":
            button.clicked.connect(self._add_half_turn_callback)
        elif text == "+1":
            button.clicked.connect(self._add_turn_callback)
        return button

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

    ### UPDATE METHODS ###

    def update_clocks(self, rotation_direction: str) -> None:
        # Clear both clock labels
        self.clock_left.clear()
        self.clock_right.clear()

        # Depending on the rotation direction, display the correct clock
        if rotation_direction == "ccw":
            self.clock_left.setPixmap(self.counter_clockwise_pixmap)
        elif rotation_direction == "cw":
            self.clock_right.setPixmap(self.clockwise_pixmap)

    def update_turnbox(self, turns) -> None:
        turns_str = str(turns)
        for i in range(self.turnbox.count()):
            if self.turnbox.itemText(i) == turns_str:
                self.turnbox.setCurrentIndex(i)
                return
            elif turns == None:
                self.turnbox.setCurrentIndex(-1)

    def _update_turns(self, index: int) -> None:
        turns = str(index)
        if turns == "0" or turns == "1" or turns == "2" or turns == "3":
            motion: Motion = self.attr_box.pictograph.get_motion_by_color(
                self.attr_box.color
            )
            if motion:
                motion.update_turns(int(turns))
                self.attr_box.update_attr_box(motion)
                self.attr_box.pictograph.update()
        elif turns == "0.5" or turns == "1.5" or turns == "2.5":
            motion: Motion = self.attr_box.pictograph.get_motion_by_color(
                self.attr_box.color
            )
            if motion:
                motion.update_turns(float(turns))
                self.attr_box.update_attr_box(motion)
                self.attr_box.pictograph.update()
        else:
            self.turnbox.setCurrentIndex(-1)

    ### EVENT HANDLERS ###

    def resizeEvent(self, event) -> None:
        """Handles the resizing event of the widget."""
        self.spacing = self.attr_box.pictograph.view.width() // 250

        super().resizeEvent(event)
        self._update_button_size()
        self._update_widget_sizes()
        self._update_clock_size()
        self._update_turnbox_size()

    def _update_widget_sizes(self) -> None:
        """Updates the sizes of the widgets based on the widget's size."""
        available_height = self.height()
        header_height = int(available_height * 2 / 3)
        turns_widget_height = int(available_height * 1 / 3)
        self.header_frame.setMaximumHeight(header_height)
        self.button_frame.setMaximumHeight(turns_widget_height)

    def _update_clock_size(self) -> None:
        """Updates the sizes of the clock labels based on the widget's size."""
        clock_size = int(self.height() / 2 * 0.8)
        for clock in [self.clock_left, self.clock_right]:
            clock.setMinimumSize(clock_size, clock_size)
            clock.setMaximumSize(clock_size, clock_size)

    def _update_turnbox_size(self) -> None:
        border_radius = min(self.turnbox.width(), self.turnbox.height()) * 0.25
        self.turnbox.setMinimumWidth(int(self.attr_box.width() / 3.25))
        self.turnbox.setMaximumWidth(int(self.attr_box.width() / 3.25))
        self.turnbox.setMinimumHeight(int(self.attr_box.width() / 5))
        self.turnbox.setMaximumHeight(int(self.attr_box.width() / 5))
        box_font_size = int(self.attr_box.width() / 10)

        self.header_label.setContentsMargins(0, 0, self.spacing, 0)
        self.header_label.setFont(QFont("Arial", int(self.attr_box.width() / 18)))

        self.turnbox.setFont(QFont("Arial", box_font_size, QFont.Weight.Bold))
        self.turnbox.setStyleSheet(
            f"""
            QComboBox {{
                border: {self.turnbox.combobox_border}px solid black;
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
        self.turnbox_vbox_frame.setMinimumWidth(int(self.attr_box.width() / 3.25))
        self.turnbox_vbox_frame.setMaximumWidth(int(self.attr_box.width() / 3.25))

        self.turnbox_vbox_frame.setMinimumHeight(int(self.height() / 2))
        self.turnbox_vbox_frame.setMaximumHeight(int(self.height() / 2))

    def _update_button_size(self) -> None:
        """Updates the sizes of the buttons based on the widget's size."""
        for button in self.buttons:
            button.update_button_size()
            button.setFont(QFont("Arial", int(button.height() / 3)))
