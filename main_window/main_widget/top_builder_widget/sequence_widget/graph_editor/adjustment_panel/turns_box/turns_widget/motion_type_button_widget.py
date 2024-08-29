from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from data.constants import PRO, ANTI, FLOAT, DASH, STATIC
from .motion_type_button import MotionTypeButton
from .motion_type_setter import MotionTypeSetter

if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from .turns_widget import TurnsWidget


class MotionTypeButtonWidget(QWidget):
    def __init__(self, turns_widget: "TurnsWidget") -> None:
        super().__init__(turns_widget)
        self.turns_widget = turns_widget
        self.buttons: dict[str, MotionTypeButton] = {}
        self.label = None
        self._setup_components()
        self._setup_layout()

    def _setup_components(self) -> None:
        # Define motion types and corresponding button labels
        motion_types = {
            "Pro": PRO,
            "Float": FLOAT,
            "Anti": ANTI,
        }

        # Create buttons systematically and store them in a dictionary
        for label, motion_type in motion_types.items():
            button = MotionTypeButton(label, motion_type, self)
            self.buttons[motion_type] = button

        # Create a label to display "Dash" or "Static" when appropriate
        self.label = QLabel("", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def _setup_layout(self) -> None:
        self.layout: QHBoxLayout = QHBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.layout)

    def update_display(self, motion_type: str) -> None:
        """Update the display based on the motion type."""
        # Clear the existing layout
        self.clear_layout()

        if motion_type in [PRO, ANTI, FLOAT]:
            self.show_buttons()
        elif motion_type in [DASH, STATIC]:
            self.show_label(motion_type)
        else:
            self.hide_all()

    def clear_layout(self) -> None:
        """Remove all widgets and stretches from the layout."""
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.hide()

    def show_buttons(self) -> None:
        """Show the motion type buttons and hide the label."""
        self.label.hide()
        self.layout.addStretch(1)
        for button in self.buttons.values():
            button.show()
            self.layout.addWidget(button)
            self.layout.addStretch(1)
        self.update_motion_type_buttons(self.turns_widget.turns_box.matching_motion.motion_type)

    def show_label(self, motion_type: str) -> None:
        """Show the label and hide the motion type buttons."""
        self.label.setText(motion_type.capitalize())
        self.layout.addStretch(1)
        self.layout.addWidget(self.label)
        self.layout.addStretch(1)
        self.label.show()
        for button in self.buttons.values():
            button.hide()

    def hide_all(self) -> None:
        """Hide all buttons and labels."""
        self.label.hide()
        for button in self.buttons.values():
            button.hide()

    def set_motion_type(self, motion_type: str) -> None:
        """Delegate the motion type setting logic to the MotionTypeSetter."""
        motion = self.turns_widget.turns_box.matching_motion
        self.turns_widget.motion_type_setter.set_motion_type(motion, motion_type)

    def update_motion_type_buttons(self, selected_type: str) -> None:
        """Update the button states to reflect the selected motion type."""
        for button in self.buttons.values():
            button.update_state(selected_type)

    def resize_buttons(self) -> None:
        """Resize the buttons and label based on the parent widget size."""
        font_size = self.turns_widget.turns_box.graph_editor.width() // 40
        font = QFont("Cambria", font_size, QFont.Weight.Bold)
        for button in self.buttons.values():
            button.setFont(font)
            button.setMaximumWidth(self.width() // 3)
        self.label.setFont(font)
