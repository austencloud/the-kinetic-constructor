from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout
from typing import TYPE_CHECKING
from Enums.Enums import AdjustmentNums, AdjustmentStrs
from widgets.factories.button_factory.buttons.adjust_turns_button import (
    AdjustTurnsButton,
)

if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_turns_widget import GE_TurnsWidget


class GE_TurnsButtonManager:
    def __init__(self, turns_widget: "GE_TurnsWidget") -> None:
        self.turns_widget = turns_widget
        self.adjustments = [(-1, "-1"), (-0.5, "-0.5"), (0.5, "+0.5"), (1, "+1")]
        self.adjust_turns_buttons: list[AdjustTurnsButton] = []
        self.button_factory = (
            self.turns_widget.turns_box.graph_editor.main_widget.button_factory
        )

    def setup_adjust_turns_buttons(self) -> None:
        """Create and setup adjustment buttons."""
        self._setup_button_frames()
        self.adjust_turns_buttons = [
            self._create_and_add_button(adj, text) for adj, text in self.adjustments
        ]

    def _setup_button_frames(self) -> None:
        self.left_spacer_frame = QFrame()
        self.right_spacer_frame = QFrame()

        self.negative_buttons_frame = QFrame()
        self.negative_buttons_container = QVBoxLayout(self.negative_buttons_frame)
        self.negative_buttons_hbox_layout = QHBoxLayout()
        self.negative_buttons_container.addLayout(self.negative_buttons_hbox_layout)

        self.positive_buttons_frame = QFrame()
        self.positive_buttons_container = QVBoxLayout(self.positive_buttons_frame)
        self.positive_buttons_hbox_layout = QHBoxLayout()
        self.positive_buttons_container.addLayout(self.positive_buttons_hbox_layout)

    def _create_and_add_button(
        self, adjustment: AdjustmentNums, text: AdjustmentStrs
    ) -> AdjustTurnsButton:
        """Create an adjust turns button and add it to the appropriate layout."""
        button: AdjustTurnsButton = self.button_factory.create_adjust_turns_button(text)
        button.setContentsMargins(0, 0, 0, 0)
        button.clicked.connect(
            lambda _, adj=adjustment: self.turns_widget.adjustment_manager.adjust_turns(
                adj
            )
        )

        layout = (
            self.negative_buttons_hbox_layout
            if adjustment < 0
            else self.positive_buttons_hbox_layout
        )
        layout.addWidget(button)
        button.setMaximumWidth(int(self.turns_widget.turns_box.width() / 4))
        return button
