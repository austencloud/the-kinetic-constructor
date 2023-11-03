import logging
from objects.arrow.arrow import Arrow
from data.positions_map import positions_map
from PyQt6.QtWidgets import QLabel


class InfoboxUpdater:
    def __init__(self, infobox_manager, main_widget, graphboard_view):
        self.graphboard_view = graphboard_view
        self.infobox_manager = infobox_manager

        self.setup_variables(main_widget, graphboard_view)

    def update_type_and_position_info(self):
        (
            current_letter,
            current_letter_type,
        ) = self.graphboard_view.info_handler.determine_current_letter_and_type()
        if current_letter and current_letter_type:
            start_end_positions = self.infobox_manager.helpers.get_start_end_positions(
                self.graphboard_view
            )
            if start_end_positions:
                start_position, end_position = start_end_positions

            info_text = f"<center><h1>{current_letter_type}</h1><p style='font-size: 18px; font-family:'Cambria;''>{start_position} → {end_position}</center></p>"
            self.infobox_manager.setup.type_position_label.setText(info_text)
        else:
            # Handle cases where the letter or type is not identified
            self.infobox_manager.setup.type_position_label.setText("")

    def update(self):
        blue_attributes = {}
        red_attributes = {}

        blue_arrows = self.infobox_manager.button_manager.get_arrows_by_color("blue")
        red_arrows = self.infobox_manager.button_manager.get_arrows_by_color("red")

        # Check if there are blue arrows on the board
        if blue_arrows:
            blue_attributes = blue_arrows[0].attributes.create_dict_from_arrow(
                blue_arrows[0]
            )
            self.update_info_widget_content(self.blue_info_widget, blue_attributes)
            self.blue_info_widget.setVisible(True)
        else:
            self.blue_info_widget.setVisible(False)

        # Check if there are red arrows on the board
        if red_arrows:
            red_attributes = red_arrows[0].attributes.create_dict_from_arrow(
                red_arrows[0]
            )
            self.update_info_widget_content(self.red_info_widget, red_attributes)
            self.red_info_widget.setVisible(True)
        else:
            self.red_info_widget.setVisible(False)

    def update_info_widget_content(self, widget, attributes):
        # If the widget doesn't have any children, initialize it
        if widget.layout().count() == 0:
            new_content = self.construct_info_string_label(attributes)
            widget.setLayout(new_content.layout())
            return

        # Otherwise, update the existing content
        motion_type_label = widget.findChild(QLabel, "motion_type_label")
        start_end_label = widget.findChild(QLabel, "start_end_label")
        turns_label = widget.findChild(QLabel, "turns_label")

        # Extract the required values
        motion_type = attributes.get("motion_type", "").capitalize()
        start_location = attributes.get("start_location", "")
        end_location = attributes.get("end_location", "")
        turns = attributes.get("turns", "")

        # Update labels
        motion_type_label.setText(f"<h1>{motion_type}</h1>")
        if motion_type in ["Pro", "Anti", "Static"]:
            start_end_label.setText(
                f"<span style='font-weight: bold; font-style: italic; font-size: 20px;'>{start_location.capitalize()} → {end_location.capitalize()}</span>"
            )
        elif motion_type == "":
            start_end_label.setText(f"")
        turns_label.setText(f"<span style='font-size: 20px;'>{turns}</span>")

        # Determine which buttons to use based on the color
        color = attributes.get("color", "")
        swap_motion_type_button = (
            self.swap_motion_type_blue_button
            if color == "blue"
            else self.swap_motion_type_red_button
        )
        swap_start_end_button = (
            self.swap_start_end_blue_button
            if color == "blue"
            else self.swap_start_end_red_button
        )
        decrement_turns_button = (
            self.decrement_turns_blue_button
            if color == "blue"
            else self.decrement_turns_red_button
        )
        increment_turns_button = (
            self.increment_turns_blue_button
            if color == "blue"
            else self.increment_turns_red_button
        )

        # Make the buttons visible
        swap_motion_type_button.setVisible(True)
        swap_start_end_button.setVisible(True)
        decrement_turns_button.setVisible(True)
        increment_turns_button.setVisible(True)

    def setup_variables(self, main_widget, graphboard_view):
        self.remaining_staff = {}
        self.previous_state = None
        self.staff_handler = graphboard_view.staff_handler
        self.letters = main_widget.letters
        self.arrow_manager = main_widget.arrow_manager
        self.arrow_manipulator = self.arrow_manager.manipulator

    def get_start_end_positions(self):
        positions = []
        arrow_items = [
            item for item in self.graphboard_view.items() if isinstance(item, Arrow)
        ]

        arrow_colors = {"red": None, "blue": None}
        for arrow in arrow_items:
            arrow_colors[arrow.color] = (arrow.start_location, arrow.end_location)

        start_location_red, end_location_red = arrow_colors["red"]
        start_location_blue, end_location_blue = arrow_colors["blue"]

        if all(
            [
                start_location_red,
                end_location_red,
                start_location_blue,
                end_location_blue,
            ]
        ):
            start_key = (start_location_red, "red", start_location_blue, "blue")
            end_key = (end_location_red, "red", end_location_blue, "blue")
            start_location = positions_map.get(start_key)
            end_location = positions_map.get(end_key)
            if start_location and end_location:
                positions.extend([start_location, end_location])
                return positions
            else:
                logging.warning("No positions returned by get_start_end_positions")
                return None
