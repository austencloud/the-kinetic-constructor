from PyQt6.QtCore import Qt, QRectF, QRect, QPoint
from PyQt6.QtGui import QFont, QPainter, QIcon, QPixmap, QScreen, QGuiApplication
from typing import TYPE_CHECKING, Union
from Enums.MotionAttributes import Color

from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QAbstractButton,
    QWidget,
    QApplication,
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
        self.turns_display_label.clicked.connect(self.on_turns_label_clicked)

    def setup_display_components(self) -> None:
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.turns_widget.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.turns_display_frame = self.setup_turns_display_frame()
        self.adjust_buttons_frame = self.setup_adjust_buttons_frame()
        self.toggle_switch = self.setup_toggle_switch()

        self.layout.addWidget(self.turns_display_frame)
        self.layout.addWidget(self.adjust_buttons_frame)
        self.layout.addWidget(self.toggle_switch)

    def setup_turns_display_frame(self):
        turns_display_frame = QFrame(self.turns_widget)
        turns_display_frame_layout = QHBoxLayout(turns_display_frame)
        self.turns_display_label = self._setup_turns_display_label()
        turns_display_frame_layout.addWidget(self.turns_display_label)
        return turns_display_frame

    def _setup_turns_display_label(self):
        turns_display_label = GE_TurnsBoxLabel("0", self.turns_widget)
        turns_display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        turns_display_label.setFont(QFont("Arial", 24))  # Larger font size

        return turns_display_label

    def on_turns_label_clicked(self):
        self.show_turns_selection_dialog()

    def show_turns_selection_dialog(self):
        dialog = GE_TurnsSelectionDialog(self.turns_widget)
        # Calculate and adjust the position to center the dialog under the turns label
        label_rect = self.turns_display_label.geometry()
        dialog_width = dialog.width()

        global_label_pos = self.turns_display_label.mapToGlobal(self.turns_display_label.pos())
        dialog_x = global_label_pos.x() + (label_rect.width() - dialog_width) / 2
        dialog_y = global_label_pos.y() + label_rect.height()

        dialog.move(int(dialog_x), int(dialog_y))
        dialog.exec()

    def setup_adjust_buttons_frame(self):
        adjust_buttons_frame = QFrame(self.turns_widget)
        self.adjust_buttons_hbox_layout = QHBoxLayout(adjust_buttons_frame)
        self.adjust_buttons_hbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.adjust_buttons_hbox_layout.setContentsMargins(0, 0, 0, 0)
        self.increment_button = SquareAdjustButton(
            "images/icons/plus.png",
            "images/icons/plus_disabled.png",
            self.turns_widget.turns_box,
        )
        self.decrement_button = SquareAdjustButton(
            "images/icons/minus.png",
            "images/icons/minus_disabled.png",
            self.turns_widget.turns_box,
        )

        self.adjust_buttons_hbox_layout.addWidget(self.decrement_button)
        self.adjust_buttons_hbox_layout.addWidget(self.increment_button)

        self.increment_button.clicked.connect(
            lambda: self.turns_widget.adjustment_manager.adjust_turns(1)
        )
        self.decrement_button.clicked.connect(
            lambda: self.turns_widget.adjustment_manager.adjust_turns(-1)
        )
        self.adjust_buttons = [self.increment_button, self.decrement_button]
        return adjust_buttons_frame

    def setup_toggle_switch(self):
        toggle_switch = QPushButton("Toggle to Half Turns", self.turns_widget)
        toggle_switch.setCheckable(True)
        toggle_switch.setChecked(False)
        toggle_switch.clicked.connect(self.on_toggle_switch_changed)
        return toggle_switch

    def on_toggle_switch_changed(self):
        is_half_turns = self.toggle_switch.isChecked()
        self.toggle_switch.setText(
            "Toggle to Whole Turns" if is_half_turns else "Toggle to Half Turns"
        )

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
        border_radius = (
            min(self.turns_display_label.width(), self.turns_display_label.height()) / 4
        )
        turn_display_border = int(self.turns_display_label.width() / 20)

        # Determine the appropriate color based on the turns box color
        turns_box_color = self.turns_box.color
        if turns_box_color == Color.RED:
            border_color = "#ED1C24"
        elif turns_box_color == Color.BLUE:
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
        self.turns_display_label.setMinimumWidth(
            int(self.turns_box.turns_panel.width() / 6)
        )
        self.turns_display_label.setMaximumWidth(
            int(self.turns_box.turns_panel.width() / 6)
        )

    def set_button_styles(self) -> None:
        button_size = int(self.turns_box.width() * 0.45)

        for button in self.adjust_buttons:
            button.setMinimumHeight(button_size)
            button.setMinimumWidth(button_size)
            button.setMaximumWidth(button_size)
            button.setMaximumHeight(button_size)

    def update_turns_display(self, turns: Union[int, float]) -> None:
        self.turns_display_label.setText(str(turns))


class SquareAdjustButton(QAbstractButton):
    def __init__(self, icon_path, disabled_icon_path, parent=None):
        super().__init__(parent)
        self.icon_pixmap = QPixmap(icon_path)
        self.disabled_icon_pixmap = QPixmap(disabled_icon_path)
        self.hovered = False
        self.enabled = True  # Initially enabled

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        current_pixmap = self.icon_pixmap if self.enabled else self.disabled_icon_pixmap

        button_color = (
            Qt.GlobalColor.gray
            if not self.enabled
            else (Qt.GlobalColor.lightGray if self.hovered else Qt.GlobalColor.white)
        )
        painter.setBrush(button_color)

        rect = QRect(0, 0, self.width(), self.height())
        painter.fillRect(rect, painter.brush())

        # Calculate the pixmap size and position
        icon_size = int(
            min(self.width(), self.height()) * 0.6
        )  # Assuming a square button for simplicity
        x = int((self.width() - icon_size) / 2)
        y = int((self.height() - icon_size) / 2)
        icon_rect = QRect(x, y, icon_size, icon_size)

        # Ensure using QRect for the target rectangle
        painter.drawPixmap(icon_rect, current_pixmap)

    def enterEvent(self, event):
        if self.enabled:
            self.hovered = True
            self.update()

    def leaveEvent(self, event):
        self.hovered = False
        self.update()

    def setEnabled(self, enabled):
        super().setEnabled(enabled)
        self.enabled = enabled
        self.update()
