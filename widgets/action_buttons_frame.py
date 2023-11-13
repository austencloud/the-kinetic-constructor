from PyQt6.QtWidgets import QPushButton, QFrame
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QVBoxLayout
from objects.arrow import Arrow
from settings.string_constants import ICON_DIR, RIGHT, LEFT
from settings.styles import (
    ACTION_BUTTON_FONT,
    ACTION_BUTTON_SIZE,
    ACTION_BUTTON_ICON_SIZE,
)
from widgets.graphboard.graphboard import GraphBoard
from utilities.json_handler import JsonHandler


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
        coordinates = self.graphboard.get_current_arrow_coordinates()

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
            ("swap_colors.png", "Swap Colors", lambda: self.graphboard.swap_colors()),
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

    def create_and_configure_button(self, icon_filename, tooltip, on_click, *args) -> QPushButton:
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
            arrow.mirror()
