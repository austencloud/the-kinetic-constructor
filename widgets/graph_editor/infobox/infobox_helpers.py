from objects.arrow.arrow import Arrow
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QHBoxLayout, QWidget, QVBoxLayout, QSizePolicy
from data.positions_map import positions_map
from resources.constants import GRAPHBOARD_SCALE
import logging


class InfoboxHelpers:
    def __init__(self, infobox, infobox_manager):
        self.infobox = infobox
        self.infobox_manager = infobox_manager

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

        turns_label = QLabel()
        turns_label.setStyleSheet("QLabel { margin-left: 3px; margin-right: 3px; }")

        turns_label.setObjectName("turns_label")
        turns_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        return motion_type_label, rotation_direction_label, start_end_label, turns_label

    ### LAYOUT METHODS ###

    def create_horizontal_layout_with_widgets(self, widgets=[]):
        """Create a horizontal layout and add provided widgets."""
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        for widget in widgets:
            layout.addWidget(widget)
        return layout

    def define_info_layouts(
        self, motion_type_label, rotation_direction_label, start_end_label, turns_label
    ):
        """Define layouts for the info widget."""
        motion_type_layout = QHBoxLayout()
        motion_type_layout.addWidget(motion_type_label)
        motion_type_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        start_end_layout = QHBoxLayout()
        start_end_layout.addWidget(start_end_label)
        start_end_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        rotation_direction_layout = QHBoxLayout()
        rotation_direction_layout.addWidget(rotation_direction_label)
        rotation_direction_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        turns_layout = QHBoxLayout()
        turns_layout.addWidget(turns_label)
        turns_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout = QVBoxLayout()
        main_layout.addLayout(motion_type_layout)
        main_layout.addLayout(start_end_layout)
        main_layout.addLayout(turns_layout)

        return main_layout

    def construct_info_widget(self, attributes, color):
        """Construct a widget displaying arrow information."""
        (
            motion_type_label,
            rotation_direction_label,
            start_end_label,
            turns_label,
        ) = self.create_labels_for_attributes(attributes)

        start_end_layout = QHBoxLayout()
        start_end_button = getattr(self.infobox, f"swap_start_end_{color}_button")
        start_end_layout.addWidget(start_end_button)
        start_end_layout.addWidget(start_end_label)

        # Create the turns layout
        turns_layout = QHBoxLayout()
        decrement_button = getattr(self.infobox, f"decrement_turns_{color}_button")
        increment_button = getattr(self.infobox, f"increment_turns_{color}_button")
        turns_layout.addWidget(decrement_button)
        turns_layout.addWidget(turns_label)
        turns_layout.addWidget(increment_button)

        # Define the main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(motion_type_label)
        main_layout.addWidget(rotation_direction_label)
        main_layout.addWidget(start_end_label)
        main_layout.addLayout(turns_layout)  # Add the turns layout here

        info_widget = QWidget()
        info_widget.setLayout(main_layout)
        return info_widget

    ### UTILITY METHODS ###

    def get_arrow_positions_on_graphboard(self, graphboard_view):
        """Retrieve the start and end positions of arrows on the graphboard."""
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
