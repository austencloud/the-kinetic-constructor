from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from objects.arrow.arrow import Arrow


class InfoboxButtons:
    BUTTON_SIZE = 30

    def __init__(self, infobox, arrow_manipulator, graphboard_view):
        self.infobox = infobox
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
            self.infobox, f"{button_name}_button", button
        )  # sets each button to be a class attribute of the infobox


    def update_buttons(self, attributes):
        color = attributes.get("color", "")
        swap_motion_type_button = (
            self.infobox.swap_motion_type_blue_button
            if color == "blue"
            else self.infobox.swap_motion_type_red_button
        )
        swap_start_end_button = (
            self.infobox.swap_start_end_blue_button
            if color == "blue"
            else self.infobox.swap_start_end_red_button
        )
        decrement_turns_button = (
            self.infobox.decrement_turns_blue_button
            if color == "blue"
            else self.infobox.decrement_turns_red_button
        )
        increment_turns_button = (
            self.infobox.increment_turns_blue_button
            if color == "blue"
            else self.infobox.increment_turns_red_button
        )

        swap_motion_type_button.setVisible(True)
        swap_start_end_button.setVisible(True)
        decrement_turns_button.setVisible(True)
        increment_turns_button.setVisible(True)
