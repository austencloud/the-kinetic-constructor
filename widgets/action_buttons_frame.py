from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QFrame, QPushButton, QVBoxLayout

from objects.arrow import Arrow
from settings.string_constants import ICON_DIR, LEFT, RIGHT
from settings.styles import (
    ACTION_BUTTON_FONT,
    ACTION_BUTTON_ICON_SIZE,
    ACTION_BUTTON_SIZE,
)
from utilities.json_handler import JsonHandler
from widgets.graphboard.graphboard import GraphBoard


class ActionButtonsFrame(QFrame):
    def __init__(
        self,
        graphboard: "GraphBoard",
        json_handler: "JsonHandler",
    ) -> None:
        super().__init__()
        self.graphboard = graphboard
        self.json_handler = json_handler
        self.action_buttons_layout = QVBoxLayout()
        self.action_buttons_layout.setSpacing(3)
        self.action_buttons_layout.setContentsMargins(0, 0, 0, 0)
        coordinates = self.graphboard.get_current_arrow_coordinates()
        #remove the frame border
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setMinimumHeight(int(self.graphboard.view.height()))

        buttons_settings = [
            (
                "update_locations.png",
                "Update Optimal Locations",
                lambda: self.json_handler.update_optimal_locations_in_json(coordinates),
            ),
            (
                "delete.png",
                "Delete",
                self.delete_selected_arrow,
            ),
            ("rotate_right.png", "Rotate Right", self.rotate_selected_arrow, RIGHT),
            ("rotate_left.png", "Rotate Left", self.rotate_selected_arrow, LEFT),
            (
                "mirror.png",
                "Mirror",
                self.mirror_selected_arrow,
            ),
            (
                "add_to_sequence.png",
                "Add to Sequence",
                lambda: self.graphboard.add_to_sequence(),
            ),
        ]

        for icon_filename, tooltip, action, *args in buttons_settings:
            button = self.create_and_configure_button(
                icon_filename, tooltip, action, *args
            )
            self.action_buttons_layout.addWidget(button)

        self.setLayout(self.action_buttons_layout)
        button_count = len(buttons_settings)
        total_button_height = button_count * ACTION_BUTTON_SIZE
        total_spacing = (button_count - 1) * self.action_buttons_layout.spacing()
        total_height = total_button_height + total_spacing
        self.setMaximumHeight(min(total_height, int(self.graphboard.height())))
        self.setMaximumWidth(ACTION_BUTTON_SIZE)
        
    def create_and_configure_button(
        self, icon_filename, tooltip, on_click, *args
    ) -> QPushButton:
        icon_path = ICON_DIR + icon_filename
        button = QPushButton(QIcon(icon_path), "")
        button.setToolTip(tooltip)
        button.setFont(ACTION_BUTTON_FONT)
        button.setFixedSize(ACTION_BUTTON_SIZE, ACTION_BUTTON_SIZE)
        button.setIconSize(ACTION_BUTTON_ICON_SIZE)
        button.clicked.connect(lambda: on_click(*args))
        return button

    def delete_selected_arrow(self) -> None:
        arrow: Arrow = (
            self.graphboard.selectedItems()[0]
            if self.graphboard.selectedItems()
            and isinstance(self.graphboard.selectedItems()[0], Arrow)
            else None
        )
        if arrow:
            arrow.delete()

    def rotate_selected_arrow(self, direction) -> None:
        arrow: Arrow = (
            self.graphboard.selectedItems()[0]
            if self.graphboard.selectedItems()
            and isinstance(self.graphboard.selectedItems()[0], Arrow)
            else None
        )
        if arrow:
            arrow.rotate(direction)

    def mirror_selected_arrow(self) -> None:
        arrow: Arrow = (
            self.graphboard.selectedItems()[0]
            if self.graphboard.selectedItems()
            and isinstance(self.graphboard.selectedItems()[0], Arrow)
            else None
        )
        if arrow:
            arrow.swap_rot_dir()
