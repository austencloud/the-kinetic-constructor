from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout
from typing import TYPE_CHECKING, List
from utilities.TypeChecking.TypeChecking import AdjustmentNums, AdjustmentStrs
from widgets.factories.button_factory.buttons.adjust_turns_button import (
    AdjustTurnsButton,
)

if TYPE_CHECKING:
    from widgets.turns_box.turns_box_widgets.turns_widget.turns_widget import (
        TurnsWidget,
    )


class TurnsButtonManager:
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        self.turns_widget = turns_widget
        self.adjustments = [(-1, "-1"), (-0.5, "-0.5"), (0.5, "+0.5"), (1, "+1")]
        self.adjust_turns_buttons: List[AdjustTurnsButton] = []

    def setup_adjust_turns_buttons(self) -> None:
        """Create and setup adjustment buttons."""
        self._setup_button_frames()
        self.adjust_turns_buttons = [
            self._create_and_add_button(adj, text) for adj, text in self.adjustments
        ]

    def _setup_button_frames(self) -> None:
        self.left_spacer_frame = QFrame()
        self.right_spacer_frame = QFrame()
        spacer_height = int(
            self.turns_widget.turns_box.turns_panel.filter_tab.section.width() / 28
        )
        self.left_spacer_frame.setMinimumHeight(spacer_height)
        self.right_spacer_frame.setMinimumHeight(spacer_height)

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
        button: AdjustTurnsButton = self.turns_widget.create_adjust_turns_button(text)
        button.setContentsMargins(0, 0, 0, 0)
        button.clicked.connect(
            lambda _, adj=adjustment: self.turns_widget.display_manager.adjust_turns(
                adj
            )
        )

        layout = (
            self.negative_buttons_hbox_layout
            if adjustment < 0
            else self.positive_buttons_hbox_layout
        )
        layout.addWidget(button)
        return button

    def unpress_vtg_buttons(self) -> None:
        """Unpress the vtg buttons."""
        if hasattr(self.turns_box, "same_button"):
            self.turns_widget.turns_box.turns_panel.filter_tab.section.rot_dir_button_manager.same_button.unpress()
            self.turns_widget.turns_box.turns_panel.filter_tab.section.rot_dir_button_manager.opp_button.unpress()

