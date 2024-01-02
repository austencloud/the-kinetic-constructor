from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QFrame,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING
from objects.motion.motion import Motion
from constants import ICON_DIR
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.base_turns_widget import (
    BaseTurnsWidget,
)


if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_attr_box import IGAttrBox


class IGTurnsWidget(BaseTurnsWidget):
    def __init__(self, attr_box: "IGAttrBox") -> None:
        super().__init__(attr_box)
        self.attr_box = attr_box
        self._initialize_ui()

    def _initialize_ui(self) -> None:
        super()._initialize_ui()
        self.turnbox_hbox_frame: QFrame = self._create_turnbox_hbox_frame()
        self._setup_layout_frames()

    ### LAYOUTS ###

    def _setup_layout_frames(self) -> None:
        """Adds the header and buttons to their respective frames."""
        self.header_layout.addWidget(self.turnbox_hbox_frame)

        self._add_widgets_to_layout(self.buttons, self.buttons_layout)

        self.header_frame = self._create_frame(self.header_layout)
        self.button_frame = self._create_frame(self.buttons_layout)

        self.layout.addWidget(self.header_frame)
        self.layout.addWidget(self.button_frame)

    ### WIDGETS ###

    def _create_turnbox_hbox_frame(self) -> None:
        """Creates the turns box and buttons for turn adjustments."""
        turnbox_frame = QFrame(self)
        turnbox_frame.setLayout(QHBoxLayout())

        self.turns_label = QLabel("Turns")

        turnbox_frame.layout().addWidget(self.turns_label)
        turnbox_frame.layout().addWidget(self.turnbox)

        turnbox_frame.layout().setContentsMargins(0, 0, 0, 0)
        turnbox_frame.layout().setAlignment(Qt.AlignmentFlag.AlignCenter)
        turnbox_frame.layout().setSpacing(0)
        return turnbox_frame

    ### CALLBACKS ###

    ## UPDATE THESE TO WORK ON ALL PICTOGRAPHS IN THE SCROLL AREA

    def _add_turn_callback(self) -> None:
        for pictograph in self.attr_box.pictographs.values():
            motion: Motion = pictograph.motions[self.attr_box.color]
            motion.add_turn()
            self._update_turnbox(motion.turns)
        self.attr_box.update_attr_box(motion)

    def _subtract_turn_callback(self) -> None:
        for pictograph in self.attr_box.pictographs.values():
            motion: Motion = pictograph.motions[self.attr_box.color]
            motion.subtract_turn()
            self._update_turnbox(motion.turns)
        self.attr_box.update_attr_box(motion)

    def _add_half_turn_callback(self) -> None:
        for pictograph in self.attr_box.pictographs.values():
            motion: Motion = pictograph.motions[self.attr_box.color]
            motion.add_half_turn()
            self._update_turnbox(motion.turns)
        self.attr_box.update_attr_box(motion)

    def _subtract_half_turn_callback(self) -> None:
        for pictograph in self.attr_box.pictographs.values():
            motion: Motion = pictograph.motions[self.attr_box.color]
            motion.subtract_half_turn()
            self._update_turnbox(motion.turns)
        self.attr_box.update_attr_box(motion)

    ### UPDATE METHODS ###

    def _update_turnbox(self, turns) -> None:
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
            for pictograph in self.attr_box.pictographs.values():
                motion: Motion = pictograph.motions[self.attr_box.color]
                if int(turns) != motion.turns:
                    motion.turns = int(turns)
                    dict = {f"{motion.color}_turns": motion.turns}
                    self._update_turnbox(motion.turns)
                    pictograph.update_pictograph(dict)

        elif turns == "0.5" or turns == "1.5" or turns == "2.5":
            for pictograph in self.attr_box.pictographs.values():
                motion: Motion = pictograph.motions[self.attr_box.color]
                if float(turns) != motion.turns:
                    motion.turns = float(turns)
                    dict = {f"{motion.color}_turns": motion.turns}
                    self._update_turnbox(motion.turns)
                    pictograph.update_pictograph(dict)
        else:
            self.turnbox.setCurrentIndex(-1)

    ### EVENT HANDLERS ###

    def _update_widget_sizes(self) -> None:
        """Updates the sizes of the widgets based on the widget's size."""
        available_height = self.height()
        header_height = int(available_height * 2 / 3)
        turns_widget_height = int(available_height * 1 / 3)
        self.header_frame.setMaximumHeight(header_height)
        # self.button_frame.setMaximumHeight(self.button_frame.height())

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
        self.turnbox.setMinimumWidth(int(self.attr_box.width() / 4))
        self.turnbox.setMaximumWidth(int(self.attr_box.width() / 4))
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
        # self.turnbox_hbox_frame.setMinimumWidth(int(self.attr_box.width() / 3.25))
        # self.turnbox_hbox_frame.setMaximumWidth(int(self.attr_box.width() / 3.25))

    def _update_button_size(self) -> None:
        for button in self.buttons:
            button_size = int(self.attr_box.width() / 8)
            if button.text() == "-0.5" or button.text() == "+0.5":
                button_size = int(button_size * 0.85)
            else:  # button.text() == "-1" or button.text() == "+1":
                button_size = int(self.attr_box.width() / 7)
            button.update_custom_button_size(button_size)

    def resize_turns_widget(self):
        self._update_turnbox_size()
        self._update_button_size()
