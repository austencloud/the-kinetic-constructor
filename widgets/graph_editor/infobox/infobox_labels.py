from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QSizePolicy
from objects.arrow.arrow import Arrow
from data.positions_map import positions_map
import logging

class InfoboxLabels:
    def __init__(self, infobox, infobox_manager):
        self.infobox = infobox
        self.infobox_manager = infobox_manager

    @staticmethod
    def update_labels(widget, attributes):
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


    ### LABEL CREATION METHODS ###

    @staticmethod

    def create_label(text="", color=None):
        """Create a generic label."""
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        if color:
            label.setStyleSheet(f"color: {color}; font-size: 25px; font-weight: bold;")
        return label

    @staticmethod
    def create_labels_for_attributes(attributes):
        """Create labels for motion type, start-end locations, and turns."""
        motion_type = attributes.get("motion_type", "").capitalize()
        rotation_direction = attributes.get("rotation_direction", "")
        start_location = attributes.get("start_location", "")
        end_location = attributes.get("end_location", "")
        turns = attributes.get("turns", "")

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

        if motion_type in ["Pro", "Anti", "Static"]:
            start_end_label = QLabel(
                f"<span style='font-weight: bold; font-style: italic; font-size: 20px;'>{start_location.capitalize()} → {end_location.capitalize()}</span>"
            )
            start_end_label.setObjectName("start_end_label")
        else:
            start_end_label = QLabel(f"")
            start_end_label.setObjectName("start_end_label")

        turns_label = QLabel(f"<span style='font-size: 20px;'>{turns}</span>")
        turns_label.setObjectName("turns_label")
        turns_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Ensure the label is center-aligned
        turns_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        return motion_type_label, rotation_direction_label, start_end_label, turns_label
    
    @staticmethod
    def get_start_end_positions(graphboard_view):
        positions = []
        arrow_items = [
            item for item in graphboard_view.items() if isinstance(item, Arrow)
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
