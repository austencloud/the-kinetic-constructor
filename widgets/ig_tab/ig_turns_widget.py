from PyQt6.QtWidgets import QLabel, QFrame, QVBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING
from constants import (
    ANTI,
    BLUE,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    DASH,
    ICON_DIR,
    NO_ROT,
    PRO,
    RED,
    STATIC,
)
from widgets.attr_box_widgets.base_turns_widget import (
    BaseTurnsWidget,
)


if TYPE_CHECKING:
    from widgets.ig_tab.ig_attr_box import IGAttrBox


class IGTurnsWidget(BaseTurnsWidget):
    def __init__(self, attr_box: "IGAttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box: "IGAttrBox" = attr_box

        self._initialize_ui()
        # self.add_black_borders()

    def _initialize_ui(self) -> None:
        super()._initialize_ui()
        self.turnbox_vbox_frame: QFrame = self._create_turnbox_vbox_frame()
        self._setup_layout_frames()
        self.turnbox.currentIndexChanged.connect(self._update_turns_directly)

    def add_black_borders(self) -> None:
        """Adds black borders around the turns widget."""
        self.setStyleSheet(
            f"""
            QFrame {{
                border: {self.attr_box.border_width}px solid black;
            }}
        """
        )

    def _setup_layout(self) -> None:
        super()._setup_layout()

        self.decrement_button_frame = self._create_frame(QVBoxLayout())
        self.increment_button_frame = self._create_frame(QVBoxLayout())
        self.decrement_button_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.increment_button_frame.layout().setContentsMargins(0, 0, 0, 0)
        self.decrement_button_frame.layout().setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.increment_button_frame.layout().setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.decrement_button_frame.layout().addWidget(self.decrement_buttons[0])
        self.decrement_button_frame.layout().addWidget(self.decrement_buttons[1])
        # for button in self.decrement_buttons:
        #     self.decrement_button_frame.layout().addWidget(button)
        for button in self.increment_buttons:
            self.increment_button_frame.layout().addWidget(button)

    ### LAYOUTS ###

    def _setup_layout_frames(self) -> None:
        """Adds the header and buttons to their respective frames."""
        self.main_hbox_layout.addWidget(self.decrement_button_frame)
        self.main_hbox_layout.addWidget(self.turnbox_vbox_frame)
        self.main_hbox_layout.addWidget(self.increment_button_frame)
        self.header_frame = self._create_frame(self.main_hbox_layout)
        self.layout.addWidget(self.header_frame)

    ### WIDGETS ###

    def _create_turnbox_vbox_frame(self) -> None:
        """Creates the turns box and buttons for turn adjustments."""
        turnbox_frame = QFrame(self)
        turnbox_frame.setLayout(QVBoxLayout())

        self.turns_label = QLabel("Turns")
        self.turns_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        turnbox_frame.layout().addWidget(self.turns_label)
        turnbox_frame.layout().addWidget(self.turnbox)
        turnbox_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        turnbox_frame.layout().setContentsMargins(0, 0, 0, 0)
        turnbox_frame.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        turnbox_frame.layout().setSpacing(0)
        return turnbox_frame

    ### CALLBACKS ###

    def _adjust_turns_callback(self, turn_adjustment: float) -> None:
        self._update_turns_incrementally(turn_adjustment)

    ### UPDATE METHODS ###

    def _update_turns_incrementally(self, adjustment: float) -> None:
        self.turnbox.currentIndexChanged.disconnect(
            self._update_turns_directly
        )  # Disconnect the signal
        for (
            pictograph
        ) in self.attr_box.attr_panel.ig_tab.ig_scroll_area.pictographs.values():
            for motion in pictograph.motions.values():
                if (
                    motion.color in [BLUE, RED]
                    and motion.motion_type == self.attr_box.motion_type
                ):
                    initial_turns = motion.turns
                    new_turns = max(0, min(3, motion.turns + adjustment))
                    if new_turns in [0.0, 1.0, 2.0, 3.0]:
                        self.turnbox.setCurrentText(str(int(new_turns)))
                    elif new_turns in [0.5, 1.5, 2.5]:
                        self.turnbox.setCurrentText(str(new_turns))

                    motion.turns = new_turns
                    motion.arrow.turns = new_turns

                    if self.attr_box.motion_type in [DASH, STATIC]:
                        if initial_turns == 0 and new_turns > 0:
                            header_widget = self.attr_box.header_widget
                            header_widget.cw_button.setChecked(True)
                            header_widget.cw_button.click()

                    if self.attr_box.motion_type in [PRO, ANTI]:
                        pictograph_dict = {
                            f"{motion.color}_turns": new_turns,
                        }
                        motion.scene.update_pictograph(pictograph_dict)
                    elif self.attr_box.motion_type in [STATIC, DASH]:
                        if motion.turns == 0:
                            pictograph_dict = {
                                f"{motion.color}_turns": new_turns,
                                f"{motion.color}_prop_rot_dir": NO_ROT,
                            }
                            motion.scene.update_pictograph(pictograph_dict)
                        elif motion.turns > 0:
                            prop_rot_dir = self._get_current_prop_rot_dir()
                            pictograph_dict = {
                                f"{motion.color}_turns": new_turns,
                                f"{motion.color}_prop_rot_dir": prop_rot_dir,
                            }
                        motion.scene.update_pictograph(pictograph_dict)

        self.turnbox.currentIndexChanged.connect(
            self._update_turns_directly
        )  # Reconnect the signal

    def _get_current_prop_rot_dir(self) -> str:
        # Retrieve the current prop_rot_dir from the IG Header Widget
        # This method needs to access the state of the buttons in the IG Header Widget
        # and return the current prop_rot_dir (CLOCKWISE or COUNTER_CLOCKWISE)
        # Depending on your implementation, this might look different
        header_widget = self.attr_box.header_widget
        if header_widget.cw_button.isChecked():
            return CLOCKWISE
        elif header_widget.ccw_button.isChecked():
            return COUNTER_CLOCKWISE
        else:
            return NO_ROT

    def _update_turns_directly(self) -> None:
        selected_turns_str = self.turnbox.currentText()
        if selected_turns_str:
            new_turns = float(selected_turns_str)
            for pictograph in self.attr_box.pictographs.values():
                for motion in pictograph.motions.values():
                    if motion.motion_type != self.attr_box.motion_type:
                        continue
                    else:
                        if new_turns >= 0 and new_turns <= 3:
                            pictograph_dict = {f"{motion.color}_turns": new_turns}
                            motion.scene.update_pictograph(pictograph_dict)
                self.turnbox.setCurrentText(str(new_turns))

    def _update_turnbox(self, turns) -> None:
        if turns in [0.0, 1.0, 2.0, 3.0]:
            turns = int(turns)
        turns_str = str(turns)
        for i in range(self.turnbox.count()):
            if self.turnbox.itemText(i) == turns_str:
                self.turnbox.setCurrentIndex(i)
                return
            elif turns == None:
                self.turnbox.setCurrentIndex(-1)

    ### EVENT HANDLERS ###

    def _update_widget_sizes(self) -> None:
        """Updates the sizes of the widgets based on the widget's size."""
        available_height = self.height()
        header_height = int(available_height * 2 / 3)
        self.header_frame.setMaximumHeight(header_height)

    def _update_turnbox_size(self) -> None:
        self.spacing = self.attr_box.attr_panel.width() // 250
        border_radius = min(self.turnbox.width(), self.turnbox.height()) * 0.25
        box_font_size = int(self.attr_box.width() / 10)
        dropdown_arrow_width = int(self.width() * 0.075)  # Width of the dropdown arrow
        border_radius = min(self.turnbox.width(), self.turnbox.height()) * 0.25

        self.setMinimumWidth(self.attr_box.width() - self.attr_box.border_width * 2)
        self.setMaximumWidth(self.attr_box.width() - self.attr_box.border_width * 2)

        self.turnbox.setMinimumHeight(int(self.attr_box.height() / 4))
        self.turnbox.setMaximumHeight(int(self.attr_box.height() / 4))
        self.turnbox.setMinimumWidth(int(self.attr_box.width() / 3))
        self.turnbox.setMaximumWidth(int(self.attr_box.width() / 3))
        self.turnbox.setFont(QFont("Arial", box_font_size, QFont.Weight.Bold))

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

    def _update_button_size(self) -> None:
        for button in self.buttons:
            button_size = int(self.attr_box.width() / 5)
            button.update_attr_box_button_size(button_size)

    def resize_turns_widget(self) -> None:
        self._update_turnbox_size()
        self._update_button_size()
