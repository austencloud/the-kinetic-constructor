from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from objects.arrow.arrow import Arrow


class InfoboxButtonManager:
    BUTTON_SIZE = 30 

    def __init__(self, infobox, arrow_manipulator, graphboard_view):
        self.infobox = infobox
        self.arrow_manipulator = arrow_manipulator
        self.graphboard_view = graphboard_view
        self.setup_buttons()

    def create_and_set_button(self, button_name, properties):
        """Create a button based on the provided properties and set it as a class attribute."""
        if properties["icon"]:
            button = QPushButton(QIcon(properties["icon"]), properties.get("text", ""))
        else:
            button = QPushButton(properties.get("text", ""))

        button.clicked.connect(properties["callback"])
        button.setFixedSize(self.BUTTON_SIZE, self.BUTTON_SIZE)

        setattr(self.infobox, f"{button_name}_button", button)

    def setup_buttons(self):
        button_properties = {
            "swap_colors": {
                "icon": None,
                "text": "↔",
                "callback": self.arrow_manipulator.swap_colors,
            },
            "swap_motion_type_blue": {
                "icon": "resources/images/icons/swap.jpg",
                "callback": lambda: self.arrow_manipulator.swap_motion_type(
                    self.get_arrows_by_color("blue"), "blue"
                ),
            },
            "swap_motion_type_red": {
                "icon": "resources/images/icons/swap.jpg",
                "callback": lambda: self.arrow_manipulator.swap_motion_type(
                    self.get_arrows_by_color("red"), "red"
                ),
            },
            "swap_start_end_blue": {
                "icon": "resources/images/icons/swap.jpg",
                "callback": lambda: self.arrow_manipulator.mirror_arrow(
                    self.get_arrows_by_color("blue"), "blue"
                ),
            },
            "swap_start_end_red": {
                "icon": "resources/images/icons/swap.jpg",
                "callback": lambda: self.arrow_manipulator.mirror_arrow(
                    self.get_arrows_by_color("red"), "red"
                ),
            },
            "decrement_turns_blue": {
                "icon": None,
                "text": "-",
                "callback": lambda: self.arrow_manipulator.decrement_turns(
                    self.get_arrows_by_color("blue"), "blue"
                ),
            },
            "decrement_turns_red": {
                "icon": None,
                "text": "-",
                "callback": lambda: self.arrow_manipulator.decrement_turns(
                    self.get_arrows_by_color("red"), "red"
                ),
            },
            "increment_turns_blue": {
                "icon": None,
                "text": "+",
                "callback": lambda: self.arrow_manipulator.increment_turns(
                    self.get_arrows_by_color("blue"), "blue"
                ),
            },
            "increment_turns_red": {
                "icon": None,
                "text": "+",
                "callback": lambda: self.arrow_manipulator.increment_turns(
                    self.get_arrows_by_color("red"), "red"
                ),
            },
        }

        for button_name, properties in button_properties.items():
            self.create_and_set_button(button_name, properties)
            button = getattr(self.infobox, f"{button_name}_button")
            button.setVisible(False)  # Set initial visibility to False

    def get_arrows_by_color(self, color):
        return [
            item
            for item in self.graphboard_view.items()
            if isinstance(item, Arrow) and item.color == color
        ]
