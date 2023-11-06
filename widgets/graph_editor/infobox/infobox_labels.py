from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QSizePolicy
from objects.arrow.arrow import Arrow
from data.positions_map import positions_map
import logging
from settings.string_constants import *


class InfoboxLabels:
    def __init__(self, infobox, graphboard):
        self.infobox = infobox
        self.graphboard = graphboard

    ### LABEL CREATION ###

    def setup_labels(self):
        self.setup_attribute_label(LEFT.capitalize(), BLUE)
        self.setup_attribute_label(RIGHT.capitalize(), RED)
        self.type_position_label = self.create_label()

    def create_attribute_labels(self):
        motion_type_label = QLabel()
        motion_type_label.setObjectName("motion_type_label")

        rotation_direction_label = QLabel()
        rotation_direction_label.setObjectName("rotation_direction_label")

        start_end_label = QLabel()
        start_end_label.setObjectName("start_end_label")

        turns_label = QLabel()
        turns_label.setObjectName("turns_label")

        turns_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        attribute_labels = {}

        attribute_labels[motion_type_label.objectName()] = motion_type_label
        attribute_labels[
            rotation_direction_label.objectName()
        ] = rotation_direction_label
        attribute_labels[start_end_label.objectName()] = start_end_label
        attribute_labels[turns_label.objectName()] = turns_label

        for label in attribute_labels.values():
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        return motion_type_label, rotation_direction_label, start_end_label, turns_label

    ### LABEL UPDATING ###

    def update_labels(self, widget, attributes):
        motion_type = attributes.get(MOTION_TYPE, "")
        rotation_direction = attributes.get(ROTATION_DIRECTION, "")
        start_location = attributes.get(START_LOCATION, "")
        end_location = attributes.get(END_LOCATION, "")
        turns = attributes.get(TURNS, "")

        motion_type_label = widget.findChild(QLabel, "motion_type_label")
        rotation_direction_label = widget.findChild(QLabel, "rotation_direction_label")
        start_end_label = widget.findChild(QLabel, "start_end_label")
        turns_label = widget.findChild(QLabel, "turns_label")

        motion_type_label.setText(f"<h1>{motion_type.capitalize()}</h1>")

        if rotation_direction:
            if rotation_direction == CLOCKWISE:
                clock_icon = CLOCKWISE_ICON
            elif rotation_direction == COUNTER_CLOCKWISE:
                clock_icon = COUNTER_CLOCKWISE_ICON
            else:
                clock_icon = CLOCK_ICON

            self.set_clock_pixmap(rotation_direction_label, clock_icon)
        else:
            rotation_direction_label.setText("")

        if motion_type in [PRO, ANTI, STATIC]:
            start_end_label.setText(
                f"<span style='font-weight: bold; font-style: italic; font-size: 20px;'>{start_location.capitalize()} → {end_location.capitalize()}</span>"
            )
        elif motion_type == "":
            start_end_label.setText(f"")
        turns_label.setText(f"<span style='font-size: 20px;'>{turns}</span>")

    def update_type_and_position_labels(self):
        (
            current_letter,
            current_letter_type,
        ) = self.graphboard.get_current_letter(), self.graphboard.get_current_letter_type()
        if current_letter and current_letter_type:
            start_end_positions = self.get_start_end_positions()
            if start_end_positions:
                start_position, end_position = start_end_positions

            info_text = f"<center><h1>{current_letter_type}</h1><p style='font-size: 18px; font-family:'Cambria;''>{start_position} → {end_position}</center></p>"
            self.type_position_label.setText(info_text)
        else:
            self.type_position_label.setText("")

    ### HELPERS ###

    def set_clock_pixmap(self, label, path):
        pixmap = QPixmap(path)
        pixmap = pixmap.scaled(
            60,
            60,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        label.setPixmap(pixmap)

    def setup_attribute_label(self, text, color):
        label = self.create_label(text, color)
        label.setAlignment(Qt.AlignmentFlag.AlignTop)
        setattr(self, f"{color}_details_label", label)

    def create_label(self, text="", color=None):
        """Create a generic label."""
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        if color:
            label.setStyleSheet(f"color: {color}; font-size: 25px; font-weight: bold;")
        return label

    def get_start_end_positions(self):
        positions = []
        arrow_items = [
            item for item in self.graphboard.items() if isinstance(item, Arrow)
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
