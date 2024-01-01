from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QFrame,
    QSizePolicy,
    QWidget,
    QComboBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from typing import TYPE_CHECKING, List, Union
from objects.motion.motion import Motion
from constants import CLOCKWISE_ICON, COUNTER_CLOCKWISE_ICON, ICON_DIR
from widgets.graph_editor_tab.attr_panel.attr_box_widgets.attr_box_widget import (
    AttrBoxWidget,
)

from widgets.graph_editor_tab.attr_panel.custom_button import CustomButton

if TYPE_CHECKING:
    from widgets.image_generator_tab.ig_turns_widget import IGTurnsWidget
    from widgets.graph_editor_tab.attr_panel.attr_box_widgets.graph_editor_turns_widget import (
        GraphEditorTurnsWidget,
    )
    from widgets.graph_editor_tab.attr_panel.bast_attr_box import BaseAttrBox
    from widgets.graph_editor_tab.attr_panel.graph_editor_attr_box import (
        GraphEditorAttrBox,
    )


class BaseTurnsWidget(AttrBoxWidget):
    def __init__(self, attr_box: "BaseAttrBox") -> None:
        super().__init__(attr_box)

    def _initialize_ui(self) -> None:
        """Initializes the user interface components and their layout."""
        self._setup_layouts()
        self.turnbox = self.create_turnbox()

    def create_turnbox(self) -> QComboBox:
        turnbox: QComboBox = QComboBox(self)
        turnbox.addItems(["0", "0.5", "1", "1.5", "2", "2.5", "3"])
        turnbox.setCurrentIndex(-1)
        return turnbox

    ### LAYOUTS ###

    def _setup_layouts(self) -> None:
        """Sets up the main and auxiliary layouts for the widget."""
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.header_layout = QHBoxLayout()
        self.buttons_layout = QHBoxLayout()

    def _add_widgets_to_layout(
        self, widgets: List[QWidget], layout: QHBoxLayout | QVBoxLayout
    ) -> None:
        """Adds the given widgets to the specified layout."""
        for widget in widgets:
            layout.addWidget(widget)

    ### WIDGETS ###

    def _create_frame(self, layout: QHBoxLayout | QVBoxLayout) -> QFrame:
        """Creates a frame with the given layout."""
        frame = QFrame()
        frame.setLayout(layout)
        frame.setContentsMargins(0, 0, 0, 0)
        frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        return frame

    def _create_turns_button(
        self: Union["GraphEditorTurnsWidget", "IGTurnsWidget"], text: str
    ) -> CustomButton:
        """Creates a turn adjustment button with specified text."""
        button = CustomButton(self)
        button.setText(text)
        if text == "-1":
            button.clicked.connect(self._subtract_turn_callback)
        elif text == "-0.5":
            button.clicked.connect(self._subtract_half_turn_callback)
        elif text == "+0.5":
            button.clicked.connect(self._add_half_turn_callback)
        elif text == "+1":
            button.clicked.connect(self._add_turn_callback)
        return button

    ### UPDATE METHODS ###

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
            motion: Motion = self.attr_box.pictograph.motions[self.attr_box.color]
            if motion and motion.arrow:
                if int(turns) != motion.turns:
                    motion.update_turns(int(turns))
                    self.attr_box.update_attr_box(motion)
                    self.attr_box.pictograph.update()
        elif turns == "0.5" or turns == "1.5" or turns == "2.5":
            motion: Motion = self.attr_box.pictograph.motions[self.attr_box.color]
            if motion:
                if float(turns) != motion.turns:
                    motion.update_turns(float(turns))
                    self.attr_box.update_attr_box(motion)
                    self.attr_box.pictograph.update()
        else:
            self.turnbox.setCurrentIndex(-1)

    ### EVENT HANDLERS ###

    def _update_turnbox_size(self) -> None:
        self.setMinimumWidth(self.attr_box.width() - self.attr_box.border_width * 2)
        self.setMaximumWidth(self.attr_box.width() - self.attr_box.border_width * 2)

        self.spacing = self.attr_box.attr_panel.width() // 250

        border_radius = min(self.turnbox.width(), self.turnbox.height()) * 0.25
        self.turnbox.setMaximumWidth(int(self.attr_box.width() / 3.25))

        self.turnbox.setMinimumHeight(int(self.attr_box.height() / 8))
        self.turnbox.setMaximumHeight(int(self.attr_box.height() / 8))
        box_font_size = int(self.attr_box.width() / 10)

        self.header_label.setContentsMargins(0, 0, self.spacing, 0)
        self.header_label.setFont(QFont("Arial", int(self.width() / 22)))

        self.turnbox.setFont(QFont("Arial", box_font_size, QFont.Weight.Bold))
        dropdown_arrow_width = int(self.width() * 0.075)  # Width of the dropdown arrow

        # Calculate the border radius as a fraction of the width or height
        border_radius = min(self.turnbox.width(), self.turnbox.height()) * 0.25

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
        self.turnbox_vbox_frame.setMinimumWidth(int(self.attr_box.width() / 3.25))
        self.turnbox_vbox_frame.setMaximumWidth(int(self.attr_box.width() / 3.25))

    def _update_button_size(self) -> None:
        for button in self.buttons:
            button_size = int(self.attr_box.width() / 7)
            if button.text() == "-0.5" or button.text() == "+0.5":
                button_size = int(button_size * 0.85)
            else:
                button_size = int(self.attr_box.width() / 6)
            button.update_custom_button_size(button_size)

    def resize_turns_widget(self):
        self._update_clock_size()
        self._update_turnbox_size()
        self._update_button_size()
        self._update_widget_sizes()
