from PyQt6.QtWidgets import QFrame, QHBoxLayout
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, Union

from .GE_adjust_turns_button import GE_AdjustTurnsButton
from .GE_turns_display import GE_TurnsDisplay
from widgets.path_helpers.path_helpers import get_images_and_data_path

if TYPE_CHECKING:
    from .GE_turns_widget import GE_TurnsWidget


class GETurnsDisplayFrame(QFrame):
    """This class is the frame that contains the turns display and the buttons to adjust the turns."""

    def __init__(self, turns_widget: "GE_TurnsWidget") -> None:
        super().__init__(turns_widget)
        self.turns_widget = turns_widget
        self.turns_box = turns_widget.turns_box
        self.adjustment_manager = turns_widget.adjustment_manager
        self._setup_components()
        self._setup_layout()

    def _setup_components(self) -> None:
        plus_path = get_images_and_data_path("images/icons/plus.svg")
        minus_path = get_images_and_data_path("images/icons/minus.svg")
        self.increment_button = GE_AdjustTurnsButton(plus_path, self)
        self.decrement_button = GE_AdjustTurnsButton(minus_path, self)
        self.turns_label = GE_TurnsDisplay(self)

    def _setup_layout(self) -> None:
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.increment_button.clicked.connect(
            lambda: self.adjustment_manager.adjust_turns(1)
        )
        self.decrement_button.clicked.connect(
            lambda: self.adjustment_manager.adjust_turns(-1)
        )
        self.decrement_button.customContextMenuRequested.connect(
            self.turns_widget.on_decrement_button_right_click
        )
        policy = Qt.ContextMenuPolicy.CustomContextMenu
        self.decrement_button.setContextMenuPolicy(policy)
        self.increment_button.setContextMenuPolicy(policy)
        self.increment_button.customContextMenuRequested.connect(
            self.turns_widget.on_increment_button_right_click
        )

        layout.addWidget(self.decrement_button, 1)
        layout.addWidget(self.turns_label, 1)
        layout.addWidget(self.increment_button, 1)
        self.turns_label.clicked.connect(self.turns_widget.on_turns_label_clicked)

    def resize_turns_display_frame(self) -> None:
        self.turns_label.set_turn_display_styles()
        self.set_button_styles()

    def set_button_styles(self) -> None:
        button_size = int(self.turns_box.width() * 0.45)
        for button in [self.increment_button, self.decrement_button]:
            button.setMaximumWidth(button_size)
            button.setMaximumHeight(button_size)
