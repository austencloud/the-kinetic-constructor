from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon, QFont
from settings.string_constants import *


class InfoboxButtons:
    BUTTON_SIZE = 30
    TURN_BUTTONS_FONT = QFont()
    TURN_BUTTONS_FONT.setPointSize(20)

    def __init__(self, infobox, infobox_manager, arrow_manipulator, graphboard_view):
        self.infobox = infobox
        self.infobox_manager = infobox_manager
        self.arrow_manipulator = arrow_manipulator
        self.graphboard_view = graphboard_view

    def create_and_set_button(self, button_name, properties):
        """Create a button based on the provided properties and set it as an infobox class attribute."""
        if properties["icon"]:
            button = QPushButton(QIcon(properties["icon"]), properties.get("text", ""))
        else:
            button = QPushButton(properties.get("text", ""))

        button.clicked.connect(properties["callback"])
        button.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
        setattr(
            self, f"{button_name}_button", button
        )  
        
        if properties.get("text") in ["+", "-"]:
            button.setFont(self.TURN_BUTTONS_FONT)

    def update_buttons(self, attributes):
        color = attributes.get(COLOR, "")
        swap_motion_type_button = (
            self.swap_motion_type_blue_button
            if color == BLUE
            else self.swap_motion_type_red_button
        )
        swap_start_end_button = (
            self.swap_start_end_blue_button
            if color == BLUE
            else self.swap_start_end_red_button
        )
        decrement_turns_button = (
            self.decrement_turns_blue_button
            if color == BLUE
            else self.decrement_turns_red_button
        )
        increment_turns_button = (
            self.increment_turns_blue_button
            if color == BLUE
            else self.increment_turns_red_button
        )

        swap_motion_type_button.setVisible(True)
        swap_start_end_button.setVisible(True)
        decrement_turns_button.setVisible(True)
        increment_turns_button.setVisible(True)

    def setup_buttons(self):
        self.button_properties = {
            "swap_colors": {
                "icon": None,
                "text": "↔",
                "callback": self.arrow_manipulator.swap_colors,
            },
            "swap_motion_type_blue": {
                "icon": ICON_DIR + "swap.jpg",
                "callback": lambda: self.arrow_manipulator.swap_motion_type(
                    self.graphboard_view.get_arrows_by_color(BLUE), BLUE
                ),
            },
            "swap_motion_type_red": {
                "icon": ICON_DIR + "swap.jpg",
                "callback": lambda: self.arrow_manipulator.swap_motion_type(
                    self.graphboard_view.get_arrows_by_color(RED), RED
                ),
            },
            "swap_start_end_blue": {
                "icon": ICON_DIR + "swap.jpg",
                "callback": lambda: self.arrow_manipulator.mirror_arrow(
                    self.graphboard_view.get_arrows_by_color(BLUE), BLUE
                ),
            },
            "swap_start_end_red": {
                "icon": ICON_DIR + "swap.jpg",
                "callback": lambda: self.arrow_manipulator.mirror_arrow(
                    self.graphboard_view.get_arrows_by_color(RED), RED
                ),
            },
            "decrement_turns_blue": {
                "icon": ICON_DIR + "decrement_turns.png",
                "callback": lambda: self.arrow_manipulator.decrement_turns(
                    self.graphboard_view.get_arrows_by_color(BLUE), BLUE
                ),
            },
            "increment_turns_blue": {
                "icon": ICON_DIR + "increment_turns.png",
                "callback": lambda: self.arrow_manipulator.increment_turns(
                    self.graphboard_view.get_arrows_by_color(BLUE), BLUE
                ),
            },
            "decrement_turns_red": {
                "icon": ICON_DIR + "decrement_turns.png",
                "callback": lambda: self.arrow_manipulator.decrement_turns(
                    self.graphboard_view.get_arrows_by_color(RED), RED
                ),
            },
            "increment_turns_red": {
                "icon": ICON_DIR + "increment_turns.png",
                "callback": lambda: self.arrow_manipulator.increment_turns(
                    self.graphboard_view.get_arrows_by_color(RED), RED
                ),
            },
        }

        self.create_infobox_buttons()

    def create_infobox_buttons(self):
        for button_name, properties in self.button_properties.items():
            self.create_and_set_button(button_name, properties)
            button = getattr(self, f"{button_name}_button")
            button.setVisible(False)  # Set initial visibility to False

        self.layouts = self.infobox_manager.layouts
        self.layouts.setup_button_layout()
