from PyQt6.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout
from typing import TYPE_CHECKING
from widgets.factories.button_factory.buttons.adjust_turns_button import (
    AdjustTurnsButton,
)

if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_ori_picker_widget import (
        GE_StartPosOriPickerWidget,
    )


class GE_StartPosOriPickerButtonManager:
    def __init__(self, start_pos_ori_picker: "GE_StartPosOriPickerWidget") -> None:
        self.ori_picker_widget = start_pos_ori_picker
        self.adjustments = [(-1, "-1"), (-0.5, "-0.5"), (0.5, "+0.5"), (1, "+1")]
        self.adjust_turns_buttons: list[AdjustTurnsButton] = []
        self.button_factory = (
            self.ori_picker_widget.ori_picker_box.graph_editor.main_widget.button_factory
        )

    def setup_adjust_turns_buttons(self) -> None:
        """Create and setup adjustment buttons."""
        self._setup_button_frames()


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

