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
from PyQt6.QtCore import QSize


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
        self.action_buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.setFrameStyle(QFrame.Shape.NoFrame)
        self.setMaximumHeight(int(self.graphboard.view.height()))
        self.button_size = int(self.graphboard.main_widget.main_window.width() * 0.020)

        buttons_settings = [
            (
                "update_locations.png",
                "Update Optimal Locations",
                lambda: self.json_handler.update_optimal_locations_in_json(
                    self.graphboard.get_current_arrow_coordinates()
                ),
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
        self.setMaximumWidth(ACTION_BUTTON_SIZE)


    def create_and_configure_button(
        self, icon_filename, tooltip, on_click, *args
    ) -> QPushButton:
        icon_path = ICON_DIR + icon_filename
        button = QPushButton(QIcon(icon_path), "")
        button.setToolTip(tooltip)
        button.setFont(ACTION_BUTTON_FONT)
        button.setFixedSize(self.button_size, self.button_size)
        button.setIconSize(QSize(int(self.button_size * 0.8), int(self.button_size * 0.8)))
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
