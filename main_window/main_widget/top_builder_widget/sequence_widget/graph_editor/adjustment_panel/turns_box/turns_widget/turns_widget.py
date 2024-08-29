from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, Union

from data.constants import ANTI, FLOAT, PRO
from main_window.main_widget.top_builder_widget.sequence_widget.graph_editor.adjustment_panel.turns_box.turns_widget.motion_type_setter import MotionTypeSetter

from .direct_set_dialog.direct_set_turns_dialog import DirectSetTurnsDialog
from .turns_display_frame.turns_display_frame import TurnsDisplayFrame
from .turns_adjustment_manager import TurnsAdjustmentManager
from .turns_updater import TurnsUpdater
from .motion_type_button_widget import MotionTypeButtonWidget  # Import the new class

if TYPE_CHECKING:
    from ..turns_box import TurnsBox


class TurnsWidget(QWidget):
    def __init__(self, turns_box: "TurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box
        self._setup_components()
        self._setup_layout()

    def _setup_components(self) -> None:
        self.adjustment_manager = TurnsAdjustmentManager(self)
        self.turns_updater = TurnsUpdater(self)
        self.turns_display_frame = TurnsDisplayFrame(self)
        self.direct_set_dialog = DirectSetTurnsDialog(self)
        self._setup_turns_text()
        self.motion_type_buttons = MotionTypeButtonWidget(
            self
        )
        self.motion_type_setter = MotionTypeSetter(self)


    def _setup_layout(self) -> None:
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.turns_text)
        layout.addStretch(1)
        layout.addWidget(self.turns_display_frame)
        layout.addStretch(4)
        layout.addWidget(
            self.motion_type_buttons
        )  # Add the motion type buttons to the layout
        layout.addStretch(2)

    def _setup_turns_text(self) -> None:
        self.turns_text = QLabel("Turns")
        self.turns_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def on_turns_label_clicked(self) -> None:
        self.direct_set_dialog.show_direct_set_dialog()

    def update_turns_display(self, turns: Union[int, float, str]) -> None:
        display_value = "fl" if turns == "fl" else str(turns)
        self.turns_display_frame.turns_label.setText(display_value)
        if self.turns_box.matching_motion.motion_type in [PRO, ANTI, FLOAT]:
            self.turns_display_frame.decrement_button.setEnabled(turns not in ["fl"])
        else:
            self.turns_display_frame.decrement_button.setEnabled(turns != 0)

    def resize_turns_widget(self) -> None:
        self.turns_display_frame.resize_turns_display_frame()
        self._resize_dir_buttons()
        self._resize_turns_text()
        self.motion_type_buttons.resize_buttons()  # Resize the motion type buttons

    def _resize_dir_buttons(self) -> None:
        self.turns_box.prop_rot_dir_button_manager.resize_prop_rot_dir_buttons()
        self.turns_box.vtg_dir_button_manager.resize_vtg_dir_buttons()

    def _resize_turns_text(self) -> None:
        font_size = self.turns_box.graph_editor.width() // 50
        font = QFont("Cambria", font_size, QFont.Weight.Bold)
        font.setUnderline(True)
        self.turns_text.setFont(font)
