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
from widgets.graphboard.graphboard import Graphboard
from utilities.json_handler import JsonHandler
from widgets.sequence.sequence_scene import SequenceScene


class ActionButtonsFrame(QFrame):
    def __init__(
        self,
        graphboard: "Graphboard",
        json_handler: "JsonHandler",
    ):
        super().__init__()
        self.graphboard = graphboard
        self.json_handler = json_handler
        self.action_buttons_layout = QVBoxLayout()
        self.action_buttons_layout.setSpacing(3)
        coordinates = self.graphboard.get_current_arrow_coordinates()

        selected_item = (
            self.graphboard.selectedItems()[0]
            if self.graphboard.selectedItems()
            else None
        )
        arrow = selected_item if isinstance(selected_item, Arrow) else None

        buttons_settings = [
            (
                "update_locations.png",
                "Update Optimal Locations",
                lambda: self.json_handler.update_optimal_locations_in_json(coordinates),
            ),
            (
                "delete.png",
                "Delete",
                lambda: arrow.delete(),
            ),
            ("rotate_right.png", "Rotate Right", lambda: arrow.rotate(RIGHT)),
            ("rotate_left.png", "Rotate Left", lambda: arrow.rotate(LEFT)),
            (
                "mirror.png",
                "Mirror",
                lambda: arrow.mirror(),
            ),
            ("swap_colors.png", "Swap Colors", lambda: self.graphboard.swap_colors()),
            (
                "add_to_sequence.png",
                "Add to Sequence",
                lambda: self.graphboard.add_to_sequence(
                    self.graphboard
                ),  # Need to implement this method
            ),
        ]

        # Function to create a congigured button
        def create_and_configure_button(icon_filename, tooltip, on_click):
            icon_path = ICON_DIR + icon_filename
            button = QPushButton(QIcon(icon_path), "")
            button.setToolTip(tooltip)
            button.setFont(ACTION_BUTTON_FONT)
            button.setFixedSize(ACTION_BUTTON_SIZE, ACTION_BUTTON_SIZE)
            button.setIconSize(ACTION_BUTTON_ICON_SIZE)
            button.clicked.connect(on_click)
            return button

        # Create and add buttons to the layout
        for icon_filename, tooltip, action in buttons_settings:
            button = create_and_configure_button(icon_filename, tooltip, action)
            self.action_buttons_layout.addWidget(button)

        self.setLayout(self.action_buttons_layout)

    def get_selected_arrow_color(self):
        selected_items = self.graphboard.selectedItems()
        if selected_items and isinstance(selected_items[0], Arrow):
            return selected_items[0].color
        return None
