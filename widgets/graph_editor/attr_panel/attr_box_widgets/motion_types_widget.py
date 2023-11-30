from PyQt6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QPushButton,
    QLabel,
)
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from widgets.graph_editor.attr_panel.attr_box import AttrBox


class MotionTypesWidget(QWidget):
    def __init__(self, attr_box: "AttrBox") -> None:
        super().__init__(attr_box)
        self.layout = QHBoxLayout(self)
        self.attr_box = attr_box
        self.motion_type = "Pro"
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.typeLabel = QLabel("Type:", self)
        self.typeButton = QPushButton(self.motion_type, self)
        self.typeButton.clicked.connect(self.toggle_motion_type)

        self.layout.addWidget(self.typeLabel)
        self.layout.addWidget(self.typeButton)

    def toggle_motion_type(self) -> None:
        if self.motion_type == "Pro":
            self.motion_type = "Anti"
        elif self.motion_type == "Anti":
            self.motion_type = "Pro"
        elif self.motion_type == "Static":
            pass

        self.typeButton.setText(self.motion_type)
        self.update_motion_type(self.motion_type)

    def update_motion_type(self, motion_type) -> None:
        print(f"Motion type set to: {motion_type}")

    def update_motion_type_widget_size(self) -> None:
        self.setFixedSize(
            self.attr_box.attr_box_width,
            int(self.attr_box.height() * 1 / 6),
        )
