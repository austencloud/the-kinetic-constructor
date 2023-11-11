from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from settings.string_constants import *


class InfoboxButtons:
    BUTTON_SIZE = 30
    ICON_PATHS = {
        "swap": ICON_DIR + "swap.jpg",
        "decrement_turns": ICON_DIR + "decrement_turns.png",
        "increment_turns": ICON_DIR + "increment_turns.png",
        "swap_colors": None,
    }

    def __init__(self, infobox, manipulator, graphboard):
        self.infobox = infobox
        self.manipulator = manipulator
        self.graphboard = graphboard
        self.button_groups = {BLUE: [], RED: []}
        self.layouts = infobox.layouts

    def create_and_set_button(self, button_name, properties):
        icon = properties.get("icon", None)
        if icon:
            button = QPushButton(QIcon(icon), properties.get("text", ""))
        else:
            button = QPushButton(properties.get("text", ""))

        button.clicked.connect(properties["callback"])
        button.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)
        setattr(self, f"{button_name}_button", button)
        button.hide()

        # Add the button to the appropriate color group
        if "blue" in button_name:
            self.button_groups[BLUE].append(button)
        elif "red" in button_name:
            self.button_groups[RED].append(button)


    def show_buttons(self, attributes):
        color = attributes.get(COLOR, "")
        for button in self.button_groups[color]:
            button.show()
            
    def setup_buttons(self):
    
        self.button_properties = {
            "swap_colors": {
                "icon": self.ICON_PATHS["swap_colors"],
                "text": "↔",
                "callback": self.manipulator.swap_colors,
            },
            "swap_motion_type_blue": {
                "icon": self.ICON_PATHS["swap"],
                "callback": lambda: self.graphboard.get_arrow_by_color(BLUE).swap_motion_type(
                  
                ),
            },
            "swap_motion_type_red": {
                "icon": self.ICON_PATHS["swap"],
                "callback": lambda: self.graphboard.get_arrow_by_color(RED).swap_motion_type(
                    
                ),
            },
            "swap_start_end_blue": {
                "icon": self.ICON_PATHS["swap"],
                "callback": lambda: self.graphboard.get_arrow_by_color(BLUE).mirror_arrow(
                    
                ),
            },
            "swap_start_end_red": {
                "icon": self.ICON_PATHS["swap"],
                "callback": lambda: self.graphboard.get_arrow_by_color(RED).mirror_arrow(
                    
                ),
            },
            "decrement_turns_blue": {
                "icon": self.ICON_PATHS["decrement_turns"],
                "callback": lambda: self.graphboard.get_arrow_by_color(BLUE).decrement_turns(),
            },
            "increment_turns_blue": {
                "icon": self.ICON_PATHS["increment_turns"],
                "callback": lambda: self.graphboard.get_arrow_by_color(BLUE).increment_turns(),
            },
            "decrement_turns_red": {
                "icon": self.ICON_PATHS["decrement_turns"],
                "callback": lambda: self.graphboard.get_arrow_by_color(RED).decrement_turns(),
            },
            "increment_turns_red": {
                "icon": self.ICON_PATHS["increment_turns"],
                "callback": lambda: self.graphboard.get_arrow_by_color(RED).increment_turns(),
            },
        }

        self.create_infobox_buttons()

    def create_infobox_buttons(self):
        for button_name, properties in self.button_properties.items():
            self.create_and_set_button(button_name, properties)

        self.layouts.setup_button_layout()
