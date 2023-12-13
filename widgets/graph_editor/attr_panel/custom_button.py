from PyQt6.QtWidgets import QPushButton, QSizePolicy
from PyQt6.QtGui import QPalette
from PyQt6.QtCore import Qt, QSize
from typing import Union, TYPE_CHECKING

if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box_widgets.start_end_widget import (
        StartEndWidget,
    )
    from widgets.graph_editor.attr_panel.attr_box_widgets.turns_widget import (
        TurnsWidget,
    )
    from widgets.graph_editor.attr_panel.attr_box_widgets.motion_types_widget import (
        MotionTypesWidget,
    )


class CustomButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        if parent:
            self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.update_button_size(parent.width(), parent.height())

    def update_button_size(self, parent_width, parent_height):
        # Determine the button size based on parent dimensions
        button_size = QSize(int(parent_width * 0.2), int(parent_height * 0.2))
        self.setFixedSize(button_size)
