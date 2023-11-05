from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QSizePolicy
from objects.arrow.arrow import Arrow
from data.positions_map import positions_map
import logging
from settings.string_constants import *


class InfoboxLabels:
    def __init__(self, infobox, infobox_manager, graphboard_view):
        self.infobox = infobox
        self.infobox_manager = infobox_manager
        self.graphboard_view = graphboard_view

    def setup_labels(self):
        self.setup_color_label(LEFT.capitalize(), BLUE)
        self.setup_color_label(RIGHT.capitalize(), RED)
        self.type_position_label = self.create_label()

    def setup_color_label(self, text, color):
        label = self.create_label(text, color)
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        setattr(self, f"{color}_details_label", label)

    def update_labels(self, widget, attributes):
        motion_type = attributes.get(MOTION_TYPE, "")
        rotation_direction = attributes.get(ROT_DIR, "")
        start_location = attributes.get(START, "")
        end_location = attributes.get(END, "")
        turns = attributes.get(TURNS, "")

        # Update labels
        motion_type_label = widget.findChild(QLabel, "motion_type_label")
        rotation_direction_label = widget.findChild(QLabel, "rotation_direction_label")
        start_end_label = widget.findChild(QLabel, "start_end_label")
        turns_label = widget.findChild(QLabel, "turns_label")

        motion_type_label.setText(f"<h1>{motion_type.capitalize()}</h1>")

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

        if motion_type in [PRO, ANTI, STATIC]:
            start_end_label.setText(
                f"<span style='font-weight: bold; font-style: italic; font-size: 20px;'>{start_location.capitalize()} → {end_location.capitalize()}</span>"
            )
        elif motion_type == "":
            start_end_label.setText(f"")
        turns_label.setText(f"<span style='font-size: 20px;'>{turns}</span>")

    ### LABEL CREATION METHODS ###

    def create_label(self, text="", color=None):
        """Create a generic label."""
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        if color:
            label.setStyleSheet(f"color: {color}; font-size: 25px; font-weight: bold;")
        return label

    def create_labels_for_attributes(self, attributes):
        """Create labels for motion type, start-end locations, and turns."""
        motion_type = attributes.get(MOTION_TYPE, "").capitalize()
        rotation_direction = attributes.get(ROT_DIR, "")
        start_location = attributes.get(START, "")
        end_location = attributes.get(END, "")
        turns = attributes.get(TURNS, "")

        motion_type_label = QLabel(f"<h1>{motion_type}</h1>")
        motion_type_label.setObjectName("motion_type_label")

        rotation_direction_label = QLabel(f"<h1>{rotation_direction}</h1>")
        rotation_direction_label.setObjectName("rotation_direction_label")
        # if rotation direction is "r", set it to Clockwise
        # if rotation direction is "l", set it to Counter-Clockwise
        if rotation_direction == "r":
            rotation_direction_label.setText("Clockwise")
        elif rotation_direction == "l":
            rotation_direction_label.setText("Anti-Clockwise")

        if motion_type in [PRO, ANTI, "Static"]:
            start_end_label = QLabel(
                f"<span style='font-weight: bold; font-style: italic; font-size: 20px;'>{start_location.capitalize()} → {end_location.capitalize()}</span>"
            )
            start_end_label.setObjectName("start_end_label")
        else:
            start_end_label = QLabel(f"")
            start_end_label.setObjectName("start_end_label")

        turns_label = QLabel(f"<span style='font-size: 20px;'>{turns}</span>")
        turns_label.setObjectName("turns_label")
        turns_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )  # Ensure the label is center-aligned
        turns_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        return motion_type_label, rotation_direction_label, start_end_label, turns_label

    def get_start_end_positions(self):
        positions = []
        arrow_items = [
            item for item in self.graphboard_view.items() if isinstance(item, Arrow)
        ]

        arrow_colors = {RED: None, BLUE: None}
        for arrow in arrow_items:
            arrow_colors[arrow.color] = (arrow.start_location, arrow.end_location)

        start_location_red, end_location_red = arrow_colors[RED]
        start_location_blue, end_location_blue = arrow_colors[BLUE]

        if all(
            [
                start_location_red,
                end_location_red,
                start_location_blue,
                end_location_blue,
            ]
        ):
            start_key = (start_location_red, RED, start_location_blue, BLUE)
            end_key = (end_location_red, RED, end_location_blue, BLUE)
            start_location = positions_map.get(start_key)
            end_location = positions_map.get(end_key)
            if start_location and end_location:
                positions.extend([start_location, end_location])
                return positions
            else:
                logging.warning("No positions returned by get_start_end_positions")
                return None

    def update_type_and_position_labels(self):
        (
            current_letter,
            current_letter_type,
        ) = self.graphboard_view.info_handler.determine_current_letter_and_type()
        if current_letter and current_letter_type:
            start_end_positions = self.get_start_end_positions()
            if start_end_positions:
                start_position, end_position = start_end_positions

            info_text = f"<center><h1>{current_letter_type}</h1><p style='font-size: 18px; font-family:'Cambria;''>{start_position} → {end_position}</center></p>"
            self.type_position_label.setText(info_text)
        else:
            # Handle cases where the letter or type is not identified
            self.type_position_label.setText("")
