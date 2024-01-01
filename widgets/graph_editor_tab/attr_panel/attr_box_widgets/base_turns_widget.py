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
    from widgets.graph_editor_tab.attr_panel.attr_box_widgets.graph_editor_turns_widget import (
        GraphEditorTurnsWidget,
    )
    from widgets.image_generator_tab.ig_turns_widget import IGTurnsWidget

    from widgets.graph_editor_tab.attr_panel.bast_attr_box import BaseAttrBox
    from widgets.graph_editor_tab.attr_panel.graph_editor_attr_box import (
        GraphEditorAttrBox,
    )


class BaseTurnsWidget(AttrBoxWidget):
    def __init__(self, attr_box: "BaseAttrBox") -> None:
        super().__init__(attr_box)

    def _initialize_ui(self) -> None:
        """Initializes the user interface components and their layout."""
        self.turnbox = self.create_turnbox()
        self.buttons: List[CustomButton] = [
            self._create_turns_button(text) for text in ["-1", "-0.5", "+0.5", "+1"]
        ]
        self._setup_layout()

    def create_turnbox(self) -> QComboBox:
        turnbox: QComboBox = QComboBox(self)
        turnbox.addItems(["0", "0.5", "1", "1.5", "2", "2.5", "3"])
        turnbox.setCurrentIndex(-1)
        turnbox.currentTextChanged.connect(self._update_turns)
        return turnbox

    ### LAYOUTS ###

    def _setup_layout(self) -> None:
        """Sets up the main and auxiliary layouts for the widget."""
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.header_layout = QHBoxLayout()
        self.buttons_layout = QHBoxLayout()
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

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

    def _update_turnbox(self, turns) -> None:
        turns_str = str(turns)
        for i in range(self.turnbox.count()):
            if self.turnbox.itemText(i) == turns_str:
                self.turnbox.setCurrentIndex(i)
                return
            elif turns == None:
                self.turnbox.setCurrentIndex(-1)
