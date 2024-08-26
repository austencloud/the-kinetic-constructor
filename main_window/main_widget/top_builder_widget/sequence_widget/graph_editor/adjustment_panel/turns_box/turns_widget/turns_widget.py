from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, Union

from .direct_set_dialog.direct_set_turns_dialog import DirectSetTurnsDialog
from .turns_display_frame.turns_display_frame import TurnsDisplayFrame
from .turns_adjustment_manager import TurnsAdjustmentManager
from .turns_updater import TurnsUpdater


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
        self.updater = TurnsUpdater(self)
        self.turns_display_frame = TurnsDisplayFrame(self)
        self.direct_set_dialog = DirectSetTurnsDialog(self)
        self._setup_turns_text()

    def _setup_layout(self) -> None:
        layout: QVBoxLayout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.turns_text)
        layout.addStretch(1)
        layout.addWidget(self.turns_display_frame)
        layout.addStretch(4)

    def _setup_turns_text(self) -> None:
        self.turns_text = QLabel("Turns")
        self.turns_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def on_turns_label_clicked(self) -> None:
        self.direct_set_dialog.show_direct_set_dialog()

    def update_turns_display(self, turns: Union[int, float]) -> None:
        self.turns_display_frame.turns_label.setText(str(turns))
        self.turns_display_frame.decrement_button.setEnabled(float(turns) > 0)

    def resize_turns_widget(self) -> None:
        self.turns_display_frame.resize_turns_display_frame()
        self._resize_dir_buttons()
        self._resize_turns_text()

    def _resize_dir_buttons(self) -> None:
        self.turns_box.prop_rot_dir_button_manager.resize_prop_rot_dir_buttons()
        self.turns_box.vtg_dir_button_manager.resize_vtg_dir_buttons()

    def _resize_turns_text(self) -> None:
        font_size = self.turns_box.graph_editor.width() // 50
        font = QFont("Cambria", font_size, QFont.Weight.Bold)
        font.setUnderline(True)
        self.turns_text.setFont(font)
