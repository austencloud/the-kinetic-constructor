from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QFrame,
    QHBoxLayout,
)
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING, Union

from widgets.graph_editor.adjustment_panel.turns_box.turns_widget.GE_turns_display_frame import (
    GETurnsDisplayFrame,
)


from .GE_adjust_turns_button import GE_AdjustTurnsButton
from .GE_turns_display import GE_TurnsDisplay
from .GE_direct_set_dialog.GE_direct_set_dialog import GE_DirectSetDialog
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
        self.adjustment_manager = GE_TurnsAdjustmentManager(self)
        self.updater = GE_TurnsUpdater(self)
        self.direct_set_dialog = GE_DirectSetDialog(self)
        self.turns_display_frame = GETurnsDisplayFrame(self)

    def _setup_ui(self) -> None:
        self.layout.addWidget(self.turns_display_frame)
        self.layout.addStretch(1)

    def show_turns_selection_dialog(self) -> None:
        self.direct_set_dialog.resize_direct_set_buttons()
        turns_label_rect = self.turns_display_frame.turns_label.geometry()
        global_turns_label_pos = self.turns_display_frame.turns_label.mapToGlobal(
            self.turns_display_frame.turns_label.pos()
        )        
        dialog_width = self.direct_set_dialog.width()
        dialog_x = global_turns_label_pos.x() + (turns_label_rect.width() - dialog_width) / 2
        dialog_y = global_turns_label_pos.y() + turns_label_rect.height()
        self.direct_set_dialog.move(int(dialog_x), int(dialog_y))
        self.direct_set_dialog.exec()

    def on_turns_label_clicked(self) -> None:
        self.show_turns_selection_dialog()

    def on_increment_button_right_click(self, pos) -> None:
        self.adjustment_manager.adjust_turns(0.5)

    def on_decrement_button_right_click(self, pos) -> None:
        self.adjustment_manager.adjust_turns(-0.5)

    def get_current_turns_value(self) -> int:
        return (
            int(self.turns_display_frame.turns_label.text())
            if self.turns_display_frame.turns_label.text() in ["0", "1", "2", "3"]
            else float(self.turns_display_frame.turns_label.text())
        )

    def update_turns_display(self, turns: Union[int, float]) -> None:
        self.turns_display_frame.turns_label.setText(str(turns))
        self.turns_display_frame.decrement_button.setEnabled(float(turns) > 0)

    def resize_GE_turns_widget(self) -> None:
        self.turns_display_frame.resize_turns_display_frame()
        self.resize_dir_buttons()

    def resize_dir_buttons(self) -> None:
        """This method sets the button size to the same size as the header label."""
        self.turns_box.prop_rot_dir_button_manager.resize_prop_rot_dir_buttons()
        self.turns_box.vtg_dir_button_manager.resize_vtg_dir_buttons()
