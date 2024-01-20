from PyQt6.QtWidgets import QFrame, QHBoxLayout
from typing import TYPE_CHECKING, List
from utilities.TypeChecking.TypeChecking import (
    AdjustmentNums,
    AdjustmentStrs,
)

if TYPE_CHECKING:
    from widgets.attr_box.attr_box_widgets.turns_widget.turns_widget import TurnsWidget
from widgets.factories.button_factory.buttons.adjust_turns_button import AdjustTurnsButton


class TurnsButtonManager:
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        self.turns_widget = turns_widget

    def setup_adjust_turns_buttons(self) -> None:
        """Create and setup adjustment buttons."""
        self._setup_button_frames()
        adjustments = [(-1, "-1"), (-0.5, "-0.5"), (0.5, "+0.5"), (1, "+1")]
        self.adjust_turns_buttons: List[AdjustTurnsButton] = [
            self._create_and_add_button(adj, text) for adj, text in adjustments
        ]

    def _setup_button_frames(self) -> None:
        self.negative_buttons_frame = QFrame()
        self.positive_buttons_frame = QFrame()
        self.negative_buttons_layout = QHBoxLayout(self.negative_buttons_frame)
        self.positive_buttons_layout = QHBoxLayout(self.positive_buttons_frame)

    def _create_and_add_button(
        self, adjustment: AdjustmentNums, text: AdjustmentStrs
    ) -> AdjustTurnsButton:
        """Create an adjust turns button and add it to the appropriate layout."""
        button: AdjustTurnsButton = self.turns_widget.create_adjust_turns_button(text)
        button.setContentsMargins(0, 0, 0, 0)
        button.clicked.connect(
            lambda _, adj=adjustment: self.turns_widget.display_manager.adjust_turns(
                adj
            )
        )

        layout = (
            self.negative_buttons_layout
            if adjustment < 0
            else self.positive_buttons_layout
        )
        layout.addWidget(button)
        return button
