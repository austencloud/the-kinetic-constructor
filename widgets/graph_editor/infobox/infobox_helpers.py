from objects.arrow.arrow import Arrow
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QWidget,
    QVBoxLayout,
)
from data.positions_map import positions_map
from resources.constants import GRAPHBOARD_SCALE
from PyQt6.QtWidgets import QSizePolicy
import logging


class InfoboxHelpers:
    def __init__(self, infobox_manager):
        self.infobox_manager = infobox_manager

    def create_label(self, text="", color=None):
        label = QLabel(text)
        label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        if color:
            label.setStyleSheet(f"color: {color}; font-size: 25px; font-weight: bold;")
        return label

    def create_horizontal_layout(self, widgets=[]):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        for widget in widgets:
            layout.addWidget(widget)
        return layout

    def add_widgets_to_grid(self, grid_layout, layouts):
        for idx, layout in enumerate(layouts):
            widget = QWidget()
            widget.setLayout(layout)
            if idx == 0:
                widget.setFixedHeight(int(120 * GRAPHBOARD_SCALE))
            elif idx == 2:
                widget.setFixedHeight(int(240 * GRAPHBOARD_SCALE))
            grid_layout.addWidget(widget, idx, 0)
            grid_layout.setRowStretch(idx, 0 if idx == 0 else 1)

    def clear_layout(self, layout):
        """Hides all widgets from the given layout."""
        for i in range(layout.count()):
            child = layout.itemAt(i)
            if child.widget():
                child.widget().hide()

    def construct_info_string_label(self, attributes):
        """Constructs a widget with arrow information and associated buttons."""

        # Extract the required values
        motion_type = attributes.get("motion_type", "").capitalize()
        start_location = attributes.get("start_location", "")
        end_location = attributes.get("end_location", "")
        turns = attributes.get("turns", "")
        color = attributes.get("color", "")

        # Create labels
        motion_type_label = QLabel(f"<h1>{motion_type}</h1>")
        motion_type_label.setObjectName("motion_type_label")  # Assign object name
        if motion_type in ["Pro", "Anti"]:
            start_end_label = QLabel(
                f"<span style='font-weight: bold; font-style: italic; font-size: 20px;'>{start_location.capitalize()} → {end_location.capitalize()}</span>"
            )
            start_end_label.setObjectName("start_end_label")  # Assign object name

        elif motion_type == "Static":
            start_end_label = QLabel(
                f"<span style='font-weight: bold; font-style: italic; font-size: 20px;'>{start_location.capitalize()} → {end_location.capitalize()}</span>"
            )
            start_end_label.setObjectName("start_end_label")  # Assign object name

        elif motion_type == "":
            start_end_label = QLabel(f"")
            start_end_label.setObjectName("start_end_label")  # Assign object name

        turns_label = QLabel(f"<span style='font-size: 20px;'>{turns}</span>")
        turns_label.setObjectName("turns_label")  # Assign object name

        turns_label.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )  # Set size policy to Fixed

        # Define the layouts
        motion_type_layout = QHBoxLayout()
        motion_type_layout.addWidget(motion_type_label)
        motion_type_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        start_end_layout = QHBoxLayout()
        start_end_layout.addWidget(start_end_label)
        start_end_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        turns_layout = QHBoxLayout()
        turns_layout.addWidget(turns_label)
        turns_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(motion_type_layout)
        main_layout.addLayout(start_end_layout)
        main_layout.addLayout(turns_layout)

        # Create a widget to hold the main layout
        info_widget = QWidget()
        info_widget.setLayout(main_layout)

        return info_widget

    def get_start_end_positions(self, graphboard_view):
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
            
