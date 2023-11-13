from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from settings.string_constants import BLUE, RED, COLOR, ICON_PATHS
from settings.numerical_constants import BUTTON_SIZE
from typing import TYPE_CHECKING, Dict, Callable, List
if TYPE_CHECKING:
    from widgets.infobox.infobox import InfoBox
    from widgets.graphboard.graphboard import GraphBoard
    

class InfoBoxButtons:
    def __init__(self, infobox: 'InfoBox', graphboard: 'GraphBoard') -> None:
        self.infobox = infobox
        self.graphboard = graphboard
        self.button_groups: Dict[str, List[QPushButton]] = {BLUE: [], RED: []}
        self.layouts = infobox.layouts

    def create_and_set_button(self, button_name: str, properties: Dict[str, str | Callable]) -> None:
        icon = properties.get("icon", None)
        button = QPushButton(QIcon(icon), properties.get("text", ""))

        button.clicked.connect(properties["callback"])
        button.setFixedSize(BUTTON_SIZE, BUTTON_SIZE)
        setattr(self, f"{button_name}_button", button)
        button.hide()

        # Add the button to the appropriate color group
        if BLUE in button_name:
            self.button_groups[BLUE].append(button)
        elif RED in button_name:
            self.button_groups[RED].append(button)

    def show_buttons(self, attributes: Dict[str, str | int]) -> None:
        color = attributes.get(COLOR, "")
        for button in self.button_groups[color]:
            button.show()

    def setup_buttons(self) -> None:
        self.button_properties = {
            "swap_colors": {
                "icon": ICON_PATHS["swap_colors"],
                "callback": lambda: self.graphboard.swap_colors(),
            },
            "swap_motion_type_blue": {
                "icon": ICON_PATHS["swap"],
                "callback": lambda: self.graphboard.get_arrow_by_color(
                    BLUE
                ).swap_motion_type(),
            },
            "swap_motion_type_red": {
                "icon": ICON_PATHS["swap"],
                "callback": lambda: self.graphboard.get_arrow_by_color(
                    RED
                ).swap_motion_type(),
            },
            "swap_start_end_blue": {
                "icon": ICON_PATHS["swap"],
                "callback": lambda: self.graphboard.get_arrow_by_color(BLUE).mirror(),
            },
            "swap_start_end_red": {
                "icon": ICON_PATHS["swap"],
                "callback": lambda: self.graphboard.get_arrow_by_color(RED).mirror(),
            },
            "decrement_turns_blue": {
                "icon": ICON_PATHS["decrement_turns"],
                "callback": lambda: self.graphboard.get_arrow_by_color(
                    BLUE
                ).decrement_turns(),
            },
            "increment_turns_blue": {
                "icon": ICON_PATHS["increment_turns"],
                "callback": lambda: self.graphboard.get_arrow_by_color(
                    BLUE
                ).increment_turns(),
            },
            "decrement_turns_red": {
                "icon": ICON_PATHS["decrement_turns"],
                "callback": lambda: self.graphboard.get_arrow_by_color(
                    RED
                ).decrement_turns(),
            },
            "increment_turns_red": {
                "icon": ICON_PATHS["increment_turns"],
                "callback": lambda: self.graphboard.get_arrow_by_color(
                    RED
                ).increment_turns(),
            },
        }

        self.create_infobox_buttons()

    def create_infobox_buttons(self) -> None:
        for button_name, properties in self.button_properties.items():
            self.create_and_set_button(button_name, properties)

        self.layouts.setup_button_layout()
