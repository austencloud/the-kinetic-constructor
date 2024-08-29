from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QCursor
from PyQt6.QtCore import Qt
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from objects.motion.motion import Motion
    from .motion_type_button_widget import MotionTypeButtonWidget


class MotionTypeButton(QPushButton):
    def __init__(
        self, label: str, motion_type: str, button_widget: "MotionTypeButtonWidget"
    ) -> None:
        super().__init__(label, button_widget)
        self.motion_type = motion_type
        self.button_widget = button_widget
        self.setCheckable(True)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.clicked.connect(self.on_click)

    def on_click(self) -> None:
        """Handle the button click event and update the motion type."""
        self.button_widget.set_motion_type(self.motion_type)
        self.uncheck_other_buttons()

    def uncheck_other_buttons(self) -> None:
        """Uncheck all other buttons except the currently clicked one."""
        for button in self.button_widget.buttons.values():
            if button != self:
                button.setChecked(False)

    def update_state(self, selected_type: str) -> None:
        """Update the button's checked state based on the selected motion type."""
        self.setChecked(self.motion_type == selected_type)
