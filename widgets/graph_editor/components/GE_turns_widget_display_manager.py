from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Union
from Enums.MotionAttributes import Color

from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
)
from constants import BLUE, RED

from widgets.graph_editor.components.GE_adjust_turns_button import (
    GE_AdjustTurnsButton,
)
from widgets.graph_editor.components.GE_turns_box_label import GE_TurnsBoxLabel
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
        self.turns_display_label = self._setup_turns_display_label()

        self.increment_button = GE_AdjustTurnsButton(
            "images/icons/plus.svg",
            self.turns_widget.turns_box,
        )
        self.decrement_button = GE_AdjustTurnsButton(
            "images/icons/minus.svg",
            self.turns_widget.turns_box,
        )

        self.increment_button.clicked.connect(
            lambda: self.turns_widget.adjustment_manager.adjust_turns(1)
        )
        self.decrement_button.clicked.connect(
            lambda: self.turns_widget.adjustment_manager.adjust_turns(-1)
        )
        turns_display_frame_layout.addWidget(self.decrement_button, 1)
        turns_display_frame_layout.addWidget(self.turns_display_label, 1)
        turns_display_frame_layout.addWidget(self.increment_button, 1)
        self.turns_display_label.clicked.connect(self.on_turns_label_clicked)
        return turns_display_frame

    def _setup_turns_display_label(self) -> GE_TurnsBoxLabel:
        turns_display_label = GE_TurnsBoxLabel("0", self.turns_widget)
        turns_display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        turns_display_label.setFont(QFont("Arial", 24))  # Larger font size
        return turns_display_label

    def on_turns_label_clicked(self) -> None:
        self.show_turns_selection_dialog()

    def show_turns_selection_dialog(self) -> None:
        self.turns_selection_dialog = GE_TurnsSelectionDialog(self.turns_widget)
        label_rect = self.turns_display_label.geometry()
        dialog_width = self.turns_selection_dialog.width()

        global_label_pos = self.turns_display_label.mapToGlobal(
            self.turns_display_label.pos()
        )
        dialog_x = global_label_pos.x() + (label_rect.width() - dialog_width) / 2
        dialog_y = global_label_pos.y() + label_rect.height()

        self.turns_selection_dialog.move(int(dialog_x), int(dialog_y))
        self.turns_selection_dialog.exec()

    def get_current_turns_value(self) -> int:
        return (
            int(self.turns_display_label.text())
            if self.turns_display_label.text() in ["0", "1", "2", "3"]
            else float(self.turns_display_label.text())
        )

    def set_turn_display_styles(self) -> None:
        self.turns_display_font_size = int(
            self.turns_box.turns_panel.graph_editor.width() / 20
        )
        self.turns_display_label.setFont(
            QFont("Arial", self.turns_display_font_size, QFont.Weight.Bold)
        )
        self.turns_display_label.setMinimumWidth(
            int(self.turns_box.turns_panel.width() / 6)
        )
        self.turns_display_label.setMaximumWidth(
            int(self.turns_box.turns_panel.width() / 6)
        )
        border_radius = self.turns_display_label.width() // 4

        turn_display_border = int(self.turns_display_label.width() / 20)
        self.turns_display_label.setMaximumHeight(
            int(self.turns_box.turns_panel.height() / 4)
        )
        # Determine the appropriate color based on the turns box color
        turns_box_color = self.turns_box.color
        if turns_box_color == RED:
            border_color = "#ED1C24"
        elif turns_box_color == BLUE:
            border_color = "#2E3192"
        else:
            border_color = "black"

        self.turns_display_label.setStyleSheet(
            f"""
            QLabel {{
                border: {turn_display_border}px solid {border_color};
                border-radius: {border_radius}px;
                background-color: white;
                padding-left: 2px; /* add some padding on the left for the text */
                padding-right: 2px; /* add some padding on the right for symmetry */
            }}
            """
        )

    def set_button_styles(self) -> None:
        button_size = int(self.turns_box.width() * 0.45)

        for button in [self.increment_button, self.decrement_button]:
            button.setMaximumWidth(button_size)
            button.setMaximumHeight(button_size)

    def update_turns_display(self, turns: Union[int, float]) -> None:
        self.turns_display_label.setText(str(turns))

    def resize_dir_buttons(self) -> None:
        """This method sets the button size to the same size as the header label."""
        self.turns_box.prop_rot_dir_button_manager.resize_prop_rot_dir_buttons()
        self.turns_box.vtg_dir_button_manager.resize_vtg_dir_buttons()
