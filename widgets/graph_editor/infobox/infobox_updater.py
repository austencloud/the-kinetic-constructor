import logging
from objects.arrow.arrow import Arrow
from data.positions_map import positions_map
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt


class InfoboxUpdater:
    def __init__(self, infobox, infobox_manager, main_widget, graphboard_view):
        self.infobox = infobox
        self.graphboard_view = graphboard_view
        self.infobox_manager = infobox_manager

    def update_type_and_position_info(self):
        (
            current_letter,
            current_letter_type,
        ) = self.graphboard_view.info_handler.determine_current_letter_and_type()
        if current_letter and current_letter_type:
            start_end_positions = self.infobox_manager.updater.get_start_end_positions()
            if start_end_positions:
                start_position, end_position = start_end_positions

            info_text = f"<center><h1>{current_letter_type}</h1><p style='font-size: 18px; font-family:'Cambria;''>{start_position} → {end_position}</center></p>"
            self.infobox_manager.ui_setup.type_position_label.setText(info_text)
        else:
            # Handle cases where the letter or type is not identified
            self.infobox_manager.ui_setup.type_position_label.setText("")

    def update(self):
        self.ui_setup = self.infobox_manager.ui_setup
        for color in ["blue", "red"]:
            arrows = self.graphboard_view.get_arrows_by_color(color)
            if arrows:
                attributes = arrows[0].attributes.create_dict_from_arrow(arrows[0])
                widget = getattr(self.ui_setup, f"{color}_info_widget")
                self.update_info_widget_content(widget, attributes)
                widget.setVisible(True)
            else:
                widget = getattr(self.ui_setup, f"{color}_info_widget")
                widget.setVisible(False)

    def update_info_widget_content(self, widget, attributes):
        if widget.layout().count() == 0:
            new_content = self.construct_info_string_label(attributes)
            widget.setLayout(new_content.layout())
            return
        self.update_labels(widget, attributes)
        self.update_buttons(attributes)

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

    def update_labels(self, widget, attributes):
        motion_type = attributes.get("motion_type", "").capitalize()
        rotation_direction = attributes.get("rotation_direction", "")
        start_location = attributes.get("start_location", "")
        end_location = attributes.get("end_location", "")
        turns = attributes.get("turns", "")

        # Update labels
        motion_type_label = widget.findChild(QLabel, "motion_type_label")
        rotation_direction_label = widget.findChild(QLabel, "rotation_direction_label")
        start_end_label = widget.findChild(QLabel, "start_end_label")
        turns_label = widget.findChild(QLabel, "turns_label")

        motion_type_label.setText(f"<h1>{motion_type}</h1>")

        # Update rotation_direction_label based on rotation_direction value
        if rotation_direction == "r":
            pixmap = QPixmap("resources/images/icons/clockwise.png")
            pixmap = pixmap.scaled(
                60,
                60,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            rotation_direction_label.setPixmap(pixmap)
        elif rotation_direction == "l":
            pixmap = QPixmap("resources/images/icons/anti-clockwise.png")
            pixmap = pixmap.scaled(
                60,
                60,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            rotation_direction_label.setPixmap(pixmap)
        else:
            rotation_direction_label.setText(f"<h1>{rotation_direction}</h1>")

        if motion_type in ["Pro", "Anti", "Static"]:
            start_end_label.setText(
                f"<span style='font-weight: bold; font-style: italic; font-size: 20px;'>{start_location.capitalize()} → {end_location.capitalize()}</span>"
            )
        elif motion_type == "":
            start_end_label.setText(f"")
        turns_label.setText(f"<span style='font-size: 20px;'>{turns}</span>")

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
