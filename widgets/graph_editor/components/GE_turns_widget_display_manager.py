from PyQt6.QtWidgets import QFrame, QLabel, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from typing import TYPE_CHECKING, Union


if TYPE_CHECKING:
    from widgets.graph_editor.components.GE_turns_widget import GE_TurnsWidget
    from widgets.graph_editor.components.GE_turns_box import GE_TurnsBox

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QPushButton, QHBoxLayout, QFrame
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QAbstractButton


class GE_TurnsWidgetDisplayManager:
    def __init__(self, turns_widget: "GE_TurnsWidget") -> None:
        self.turns_widget = turns_widget
        self.turns_box = turns_widget.turns_box
        self.setup_display_components()

    def setup_display_components(self) -> None:
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.turns_widget.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.turns_display_frame = self.setup_turns_display_frame()
        self.adjust_buttons_frame = self.setup_adjust_buttons_frame()
        self.toggle_switch = self.setup_toggle_switch()

        self.layout.addWidget(self.turns_display_frame)
        self.layout.addWidget(self.toggle_switch)
        self.layout.addWidget(self.adjust_buttons_frame)

    def setup_turns_display_frame(self):
        turns_display_frame = QFrame(self.turns_widget)
        turns_display_frame_layout = QHBoxLayout(turns_display_frame)
        self.turns_display_label = self._setup_turns_display_label()
        turns_display_frame_layout.addWidget(self.turns_display_label)
        return turns_display_frame

    def _setup_turns_display_label(self):
        turns_display_label = QLabel("0", self.turns_widget)
        turns_display_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        turns_display_label.setFont(QFont("Arial", 24))  # Larger font size
        turns_display_label.setStyleSheet(
            """
            QLabel {
                background-color: #ffffff;
                border: 2px solid #000000;
                border-radius: 10px;
                padding: 10px;
                font-weight: bold;
            }
        """
        )
        return turns_display_label

    def setup_adjust_buttons_frame(self):
        adjust_buttons_frame = QFrame(self.turns_widget)
        self.adjust_buttons_hbox_layout = QHBoxLayout(adjust_buttons_frame)
        self.adjust_buttons_hbox_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.adjust_buttons_hbox_layout.setContentsMargins(0, 0, 0, 0)
        self.increment_button = RoundButton("+1 Turn", self.turns_widget)
        self.decrement_button = RoundButton("-1 Turn", self.turns_widget)

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
        self.increment_button.setText("+0.5 Turn" if is_half_turns else "+1 Turn")
        self.decrement_button.setText("-0.5 Turn" if is_half_turns else "-1 Turn")

    def get_current_turns_value(self) -> int:
        return (
            int(self.turns_display_label.text())
            if self.turns_display_label.text() in ["0", "1", "2", "3"]
            else float(self.turns_display_label.text())
        )

    def set_turn_display_styles(self) -> None:
        self.turns_display_font_size = int(
            self.turns_box.turns_panel.graph_editor.width() / 26
        )
        self.turns_display_label.setFont(
            QFont("Arial", self.turns_display_font_size, QFont.Weight.Bold)
        )
        border_radius = (
            min(self.turns_display_label.width(), self.turns_display_label.height()) / 4
        )
        turn_display_border = int(self.turns_display_label.width() / 26)
        self.turns_display_label.setStyleSheet(
            f"""
            QLabel {{
                border: {turn_display_border}px solid black;
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
        # each button should be 40% of the width of the turns box and equal height
        button_size = int(self.turns_box.turns_panel.width() / 4)

        for button in self.adjust_buttons:
            button.setMinimumHeight(button_size)
            button.setMinimumWidth(button_size)
            button.setMaximumWidth(button_size)
            button.setMaximumHeight(button_size)

    def update_turns_display(self, turns: Union[int, float]) -> None:
        self.turns_display_label.setText(str(turns))


from PyQt6.QtWidgets import QAbstractButton
from PyQt6.QtGui import QPainter, QColor, QBrush, QPen, QFont
from PyQt6.QtCore import Qt, QRectF


class RoundButton(QAbstractButton):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.text = text
        self.hovered = False  # Track hover state

    def set_hovered(self, state):
        self.hovered = state
        self.update()  # Trigger a repaint when the hover state changes

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Set the button color based on hover state
        button_color = QColor(220, 220, 220) if self.hovered else QColor(255, 255, 255)
        border_color = QColor(0, 0, 0)
        painter.setBrush(button_color)
        painter.setPen(QPen(border_color, 2))  # Border thickness

        # Draw the button as a circle
        painter.drawEllipse(
            0, 0, self.width() - 1, self.height() - 1
        )  # Subtract 1 to ensure the border is fully visible

        # Set text color and font
        painter.setPen(Qt.GlobalColor.black)
        painter.setFont(QFont("Arial", 12))

        # Draw text in the center
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text)

    def sizeHint(self):
        return QSize(40, 40)  # Provide a default size hint for layout purposes

    def enterEvent(self, event):
        self.hovered = True
        self.update()  # Trigger repaint

    def leaveEvent(self, event):
        self.hovered = False
        self.update()  # Trigger repaint
