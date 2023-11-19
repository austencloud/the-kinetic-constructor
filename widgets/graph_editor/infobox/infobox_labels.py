import logging
from typing import TYPE_CHECKING, Dict

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QSizePolicy, QHBoxLayout

from data.positions_map import positions_map
from objects.arrow import Arrow
from objects.ghosts.ghost_arrow import GhostArrow
from settings.string_constants import (
    LEFT,
    RIGHT,
    BLUE,
    RED,
    CLOCKWISE,
    COUNTER_CLOCKWISE,
    CLOCK_ICON,
    CLOCKWISE_ICON,
    COUNTER_CLOCKWISE_ICON,
    PRO,
    ANTI,
    STATIC,
    CLOCKWISE_ICON,
    COUNTER_CLOCKWISE_ICON,
    CLOCK_ICON,
)
from utilities.TypeChecking.TypeChecking import Color

if TYPE_CHECKING:
    from widgets.graph_editor.graphboard.graphboard import GraphBoard
    from widgets.graph_editor.infobox.control_panel.control_panel import ControlPanel


class InfoBoxLabels:
    def __init__(self, control_panel: "ControlPanel", graphboard: "GraphBoard") -> None:
        """
        Initialize the InfoboxLabels class.

        Args:
            control_panel (ControlPanel): The control panel object.
            graphboard (GraphBoard): The graphboard object.
        """
        self.control_panel = control_panel
        self.graphboard = graphboard
        self.pixmap_cache: Dict[str] = {}
        self.blue_details_label: QLabel = None
        self.red_details_label: QLabel = None
        self.type_position_label: QLabel = None
        self.setup_labels()
        self.preload_pixmaps()

    ### LABEL CREATION ###

    def setup_labels(self) -> None:
        """
        Set up the labels for the infobox.

        This method initializes the attribute labels for the left and right sides,
        as well as creates the type position label.
        """
        self.setup_attribute_label(LEFT.capitalize(), BLUE)
        self.setup_attribute_label(RIGHT.capitalize(), RED)
        self.type_position_label = self.create_label()

    def create_attribute_labels(self) -> tuple[QLabel, QLabel, QLabel, QLabel]:
        motion_type_label = QLabel()
        motion_type_label.setObjectName("motion_type_label")

        rotation_direction_label = QLabel()
        rotation_direction_label.setObjectName("rotation_direction_label")

        start_end_label = QLabel()
        start_end_label.setObjectName("start_end_label")

        turns_label = QLabel()
        turns_label.setObjectName("turns_label")
        turns_label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        attribute_labels: Dict[str, QLabel] = {}

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

    def update_labels(self, widget: "QFrame", arrow: "Arrow") -> None:
            """
            Update the labels in the infobox widget based on the arrow object.

            Args:
                widget (QFrame): The infobox widget.
                arrow (Arrow): The arrow object containing the data.

            Returns:
                None
            """
            motion_type_label = widget.findChild(QLabel, "motion_type_label")
            rotation_direction_label = widget.findChild(QLabel, "rotation_direction_label")
            start_end_label = widget.findChild(QLabel, "start_end_label")
            turns_label = widget.findChild(QLabel, "turns_label")

            motion_type_label.setText(f"<h1>{arrow.motion_type.capitalize()}</h1>")

            if arrow.rotation_direction:
                if arrow.rotation_direction == CLOCKWISE:
                    clock_icon = CLOCKWISE_ICON
                elif arrow.rotation_direction == COUNTER_CLOCKWISE:
                    clock_icon = COUNTER_CLOCKWISE_ICON
                else:
                    clock_icon = CLOCK_ICON

                self.set_clock_pixmap(rotation_direction_label, clock_icon)
            else:
                rotation_direction_label.setText("")

            if arrow.motion_type in [PRO, ANTI, STATIC]:
                start_end_label.setText(
                    f"<span style='font-weight: bold; font-style: italic; font-size: 20px;'>{arrow.start_location.capitalize()} → {arrow.end_location.capitalize()}</span>"
                )
            elif arrow.motion_type == "":
                start_end_label.setText(f"")
            turns_label.setText(f"<span style='font-size: 20px;'>{arrow.turns}</span>")

    def update_type_and_position_label(self) -> None:
        """
        Update the type and position label based on the current letter and its type.
        """
        (
            current_letter,
            current_letter_type,
        ) = (
            self.graphboard.current_letter,
            self.graphboard.get_current_letter_type(),
        )
        if current_letter and current_letter_type:
            start_end_positions = self.get_start_end_positions()
            if start_end_positions:
                start_position, end_position = start_end_positions

            info_text = f"<center><h1>{current_letter_type}</h1><p style='font-size: 18px; font-family:'Cambria;''>{start_position} → {end_position}</center></p>"
            self.type_position_label.setText(info_text)
        else:
            self.type_position_label.setText("")

    ### HELPERS ###

    def preload_pixmaps(self) -> None:
        """
        Preload and cache the pixmaps.

        This method loads and caches the pixmaps for the infobox clock.
        It iterates over a list of icon names, loads each pixmap using QPixmap,
        scales it to a size of 60x60 pixels, and stores the scaled pixmap in the pixmap_cache dictionary.

        Returns:
            None
        """
        for icon_name in [CLOCKWISE_ICON, COUNTER_CLOCKWISE_ICON]:
            pixmap = QPixmap(icon_name)
            scaled_pixmap = pixmap.scaled(
                60,
                60,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.pixmap_cache[icon_name] = scaled_pixmap

    def set_clock_pixmap(self, label: "QLabel", icon_name: str) -> None:
        """
        Set the pixmap of a QLabel widget using the specified icon name.

        Args:
            label (QLabel): The QLabel widget to set the pixmap for.
            icon_name (str): The name of the icon to use for the pixmap.

        Returns:
            None
        """
        # Set the pixmap from the cache
        if icon_name in self.pixmap_cache:
            label.setPixmap(self.pixmap_cache[icon_name])

    def setup_attribute_label(self, text: str, color: Color) -> None:
        """
        Set up an attribute label with the given text and color.

        Args:
            text (str): The text to be displayed on the label.
            color (str): The color of the label.

        Returns:
            None
        """
        label = self.create_label(text, color)
        setattr(self, f"{color}_details_label", label)

    def create_label(self, text="", color=None) -> QLabel:
            """
            Create a QLabel widget with the specified text and color.

            Args:
                text (str): The text to be displayed on the label. Defaults to an empty string.
                color (str): The color of the label. Defaults to None.

            Returns:
                QLabel: The created label widget.
            """
            label = QLabel(text, self.control_panel)  # Set control_panel as parent
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            if color:
                label.setStyleSheet(f"color: {color}; font-size: 25px; font-weight: bold;")
            return label

    def get_start_end_positions(self) -> list[tuple[str, str] | None]:
        positions = []
        arrow_items = [
            item
            for item in self.graphboard.items()
            if isinstance(item, Arrow) or isinstance(item, GhostArrow)
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
