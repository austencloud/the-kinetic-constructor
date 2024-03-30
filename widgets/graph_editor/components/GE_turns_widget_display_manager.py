from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Union
from constants import BLUE, RED
from path_helpers import get_images_and_data_path
from widgets.graph_editor.components.GE_turns_box_label import GE_TurnsDisplay

from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QMenu,  # Import QMenu for right-click menu
)


from widgets.graph_editor.components.GE_adjust_turns_button import (
    GE_AdjustTurnsButton,
)
from widgets.graph_editor.components.GE_turns_widget_turns_selection_dialog import (
    GE_TurnsSelectionDialog,
)

if TYPE_CHECKING:

    from widgets.graph_editor.components.GE_turns_widget import GE_TurnsWidget


class GE_TurnsWidgetDisplayManager:
    def __init__(self, turns_widget: "GE_TurnsWidget") -> None:
        self.turns_widget = turns_widget
        self.turns_box = turns_widget.turns_box
        self.setup_display_components()

    def setup_display_components(self) -> None:
        self.turns_display_frame = self.setup_turns_display_frame()
        self.turns_widget.layout.addWidget(self.turns_display_frame)
        self.turns_widget.layout.addStretch(1)

    def setup_turns_display_frame(self) -> QFrame:
        turns_display_frame = QFrame(self.turns_widget)
        turns_display_frame_layout = QHBoxLayout(turns_display_frame)
        self.turns_display = self._setup_turns_display()

        plus_path = get_images_and_data_path("images/icons/plus.svg")
        self.increment_button = GE_AdjustTurnsButton(
            plus_path,
            self.turns_widget,
        )
        minus_path = get_images_and_data_path("images/icons/minus.svg")
        self.decrement_button = GE_AdjustTurnsButton(
            minus_path,
            self.turns_widget,
        )

        self.increment_button.clicked.connect(
            lambda: self.turns_widget.adjustment_manager.adjust_turns(1)
        )
        self.decrement_button.clicked.connect(
            lambda: self.turns_widget.adjustment_manager.adjust_turns(-1)
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

    def _setup_turns_display(self) -> GE_TurnsDisplay:
        turns_display_label = GE_TurnsDisplay(self.turns_widget)
        turns_display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        turns_display_label.setFont(QFont("Arial", 24))  # Larger font size
        return turns_display_label

    def on_turns_label_clicked(self) -> None:
        self.show_turns_selection_dialog()

    def show_turns_selection_dialog(self) -> None:
        self.turns_selection_dialog = GE_TurnsSelectionDialog(self.turns_widget)
        label_rect = self.turns_display.geometry()
        dialog_width = self.turns_selection_dialog.width()

        global_label_pos = self.turns_display.mapToGlobal(self.turns_display.pos())
        dialog_x = global_label_pos.x() + (label_rect.width() - dialog_width) / 2
        dialog_y = global_label_pos.y() + label_rect.height()

        self.turns_selection_dialog.move(int(dialog_x), int(dialog_y))
        self.turns_selection_dialog.exec()

    def get_current_turns_value(self) -> int:
        return (
            int(self.turns_display.text())
            if self.turns_display.text() in ["0", "1", "2", "3"]
            else float(self.turns_display.text())
        )

    def set_button_styles(self) -> None:
        button_size = int(self.turns_box.width() * 0.45)

        for button in [self.increment_button, self.decrement_button]:
            button.setMaximumWidth(button_size)
            button.setMaximumHeight(button_size)

    def update_turns_display(self, turns: Union[int, float]) -> None:
        self.turns_display.setText(str(turns))
        # Logic to enable or disable the decrement button
        self.decrement_button.setEnabled(float(turns) > 0)

    def resize_dir_buttons(self) -> None:
        """This method sets the button size to the same size as the header label."""
        self.turns_box.prop_rot_dir_button_manager.resize_prop_rot_dir_buttons()
        self.turns_box.vtg_dir_button_manager.resize_vtg_dir_buttons()

    def on_increment_button_right_click(self, pos) -> None:
        self.turns_widget.adjustment_manager.adjust_turns(0.5)

    def on_decrement_button_right_click(self, pos) -> None:
        self.turns_widget.adjustment_manager.adjust_turns(-0.5)
