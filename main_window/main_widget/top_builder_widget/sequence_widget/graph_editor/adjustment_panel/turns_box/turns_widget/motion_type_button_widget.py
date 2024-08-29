from PyQt6.QtWidgets import QWidget, QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING
from data.constants import PRO, ANTI, FLOAT
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

    def _setup_layout(self) -> None:
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(1)
        for button in self.buttons.values():
            layout.addWidget(button)
            layout.addStretch(1)
        self.setLayout(layout)

    def set_motion_type(self, motion_type: str) -> None:
        """Delegate the motion type setting logic to the MotionTypeSetter."""
        motion = self.turns_widget.turns_box.matching_motion
        self.turns_widget.motion_type_setter.set_motion_type(motion, motion_type)

    def update_motion_type_buttons(self, selected_type: str) -> None:
        """Update the button states to reflect the selected motion type."""
        for button in self.buttons.values():
            button.update_state(selected_type)

    def toggle_visibility(self, motion: "Motion") -> None:
        """Toggle visibility of the motion type buttons."""
        if motion.motion_type in [PRO, ANTI, FLOAT]:
            self.show()
            self.update_motion_type_buttons(motion.motion_type)
        else:
            self.hide()

    def resize_buttons(self) -> None:
        """Resize the buttons based on the parent widget size."""
        font_size = self.turns_widget.turns_box.graph_editor.width() // 40
        font = QFont("Cambria", font_size, QFont.Weight.Bold)
        for button in self.buttons.values():
            button.setFont(font)
            button.setMaximumWidth(self.width() // 3)
