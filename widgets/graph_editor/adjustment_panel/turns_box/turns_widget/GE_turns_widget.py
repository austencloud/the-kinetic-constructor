from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QFrame,
    QHBoxLayout,
    QPushButton,
    QMenu,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Union


from.GE_adjust_turns_button import GE_AdjustTurnsButton
from.GE_turns_display import GE_TurnsDisplay
from.direct_set_dialog.GE_direct_set_dialog import GE_DirectSetDialog
from widgets.path_helpers.path_helpers import get_images_and_data_path
from .GE_turns_adjustment_manager import GE_TurnsAdjustmentManager
from .GE_turns_updater import GE_TurnsUpdater


if TYPE_CHECKING:
    from ..GE_turns_box import GE_TurnsBox


class GE_TurnsWidget(QWidget):
    def __init__(self, turns_box: "GE_TurnsBox") -> None:
        super().__init__(turns_box)
        self.turns_box = turns_box
        self._setup_layout()
        self._setup_components()
        self._setup_ui()

    def _setup_layout(self) -> None:
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

    def _setup_components(self) -> None:
        self.setup_adjust_turns_buttons()
        self.turns_display_frame = self.setup_turns_display_frame()
        self.adjustment_manager = GE_TurnsAdjustmentManager(self)
        self.updater = GE_TurnsUpdater(self)
        self.direct_set_dialog = GE_DirectSetDialog(self)

    def setup_adjust_turns_buttons(self):
        plus_path = get_images_and_data_path("images/icons/plus.svg")
        self.increment_button = GE_AdjustTurnsButton(
            plus_path,
            self,
        )
        minus_path = get_images_and_data_path("images/icons/minus.svg")
        self.decrement_button = GE_AdjustTurnsButton(
            minus_path,
            self,
        )

    def _setup_turns_display(self) -> GE_TurnsDisplay:
        turns_display_label = GE_TurnsDisplay(self)
        turns_display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return turns_display_label

    def setup_turns_display_frame(self) -> QFrame:
        turns_display_frame = QFrame(self)
        turns_display_frame_layout = QHBoxLayout(turns_display_frame)
        self.turns_display = self._setup_turns_display()

        self.increment_button.clicked.connect(
            lambda: self.adjustment_manager.adjust_turns(1)
        )
        self.decrement_button.clicked.connect(
            lambda: self.adjustment_manager.adjust_turns(-1)
        )
        self.decrement_button.customContextMenuRequested.connect(
            self.on_decrement_button_right_click
        )
        policy = Qt.ContextMenuPolicy.CustomContextMenu
        self.decrement_button.setContextMenuPolicy(policy)
        self.increment_button.setContextMenuPolicy(policy)
        self.increment_button.customContextMenuRequested.connect(
            self.on_increment_button_right_click
        )

        turns_display_frame_layout.addWidget(self.decrement_button, 1)
        turns_display_frame_layout.addWidget(self.turns_display, 1)
        turns_display_frame_layout.addWidget(self.increment_button, 1)
        self.turns_display.clicked.connect(self.on_turns_label_clicked)
        return turns_display_frame

    def _setup_ui(self) -> None:
        self.direct_set_dialog.setup_direct_set_buttons()
        self.setup_display_components()

    def setup_display_components(self) -> None:

        self.layout.addWidget(self.turns_display_frame)
        self.layout.addStretch(1)

    def show_turns_selection_dialog(self) -> None:
        self.direct_set_dialog = self.direct_set_dialog
        label_rect = self.turns_display.geometry()
        dialog_width = self.direct_set_dialog.width()

        global_label_pos = self.turns_display.mapToGlobal(self.turns_display.pos())
        dialog_x = global_label_pos.x() + (label_rect.width() - dialog_width) / 2
        dialog_y = global_label_pos.y() + label_rect.height()

        self.direct_set_dialog.move(int(dialog_x), int(dialog_y))
        self.direct_set_dialog.exec()
        self.direct_set_dialog.resize_direct_set_buttons()

    def on_turns_label_clicked(self) -> None:
        self.show_turns_selection_dialog()

    def resize_GE_turns_widget(self) -> None:
        self.turns_display.set_turn_display_styles()
        self.set_button_styles()
        self.resize_dir_buttons()

    def on_increment_button_right_click(self, pos) -> None:
        self.adjustment_manager.adjust_turns(0.5)

    def on_decrement_button_right_click(self, pos) -> None:
        self.adjustment_manager.adjust_turns(-0.5)

    def get_current_turns_value(self) -> int:
        return (
            int(self.turns_display.text())
            if self.turns_display.text() in ["0", "1", "2", "3"]
            else float(self.turns_display.text())
        )

    def update_turns_display(self, turns: Union[int, float]) -> None:
        self.turns_display.setText(str(turns))
        self.decrement_button.setEnabled(float(turns) > 0)

    def set_button_styles(self) -> None:
        button_size = int(self.turns_box.width() * 0.45)
        for button in [self.increment_button, self.decrement_button]:
            button.setMaximumWidth(button_size)
            button.setMaximumHeight(button_size)

    def resize_dir_buttons(self) -> None:
        """This method sets the button size to the same size as the header label."""
        self.turns_box.prop_rot_dir_button_manager.resize_prop_rot_dir_buttons()
        self.turns_box.vtg_dir_button_manager.resize_vtg_dir_buttons()
