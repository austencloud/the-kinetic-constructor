import logging
from typing import TYPE_CHECKING, Dict

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QSizePolicy

from data.positions_map import positions_map
from objects.arrow import Arrow
from objects.ghosts.ghost_arrow import GhostArrow
from settings.string_constants import (
    ANTI,
    BLUE,
    CLOCK_ICON,
    CLOCKWISE,
    CLOCKWISE_ICON,
    COUNTER_CLOCKWISE,
    COUNTER_CLOCKWISE_ICON,
    PRO,
    RED,
    STATIC,
)
from utilities.TypeChecking.TypeChecking import Color

if TYPE_CHECKING:
    from widgets.graph_editor.graphboard.graphboard import GraphBoard
    from widgets.graph_editor.infobox.attribute_panel.attribute_panel import (
        AttributePanel,
    )

from PyQt6.QtWidgets import QVBoxLayout


class AttributeBox(QFrame):
    def __init__(
        self, attribute_panel: "AttributePanel", graphboard: "GraphBoard", color: Color
    ) -> None:
        self.attribute_panel = attribute_panel
        self.graphboard = graphboard
        self.color = color

        super().__init__(self.attribute_panel)
        # Set object name for the frame
        self.setObjectName("AttributeBox")

        # Add black border to the frame
        self.setStyleSheet("#AttributeBox { border: 1px solid black; }")

        self.pixmap_cache: Dict[str, QPixmap] = {}

        header_text = {BLUE: "Left", RED: "Right"}.get(color, "")
        header_color = {BLUE: BLUE, RED: RED}.get(color, "")

        self.info_header = self.create_info_header(
            header_text, Qt.AlignmentFlag.AlignHCenter, header_color
        )
        self.attributebox_layout = QVBoxLayout(self)
        self.setLayout(self.attributebox_layout)
        self.setContentsMargins(0, 0, 0, 0)  # Remove padding on the edges
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)
        self.attribute_labels = self.create_attribute_labels()
        self.clock_label = self.create_clock_label()  # Create the clock label
        self.layout().addWidget(self.info_header)
        for label in self.attribute_labels.values():
            self.layout().addWidget(label)

        # COMMENT THIS OUT FOR LAYOUT MANAGEMENT
        # self.setStyleSheet("QFrame { border: 1px solid black; }")

    ### LABEL CREATION ###

    def create_clock_label(self) -> QLabel:
        """
        Creates a QLabel for the clock icon.

        Returns:
            QLabel: The created QLabel object which will contain the clock pixmap.
        """
        label = QLabel()
        label.setObjectName("clock_label")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        return label

    def update_clock_label(self, arrow: "Arrow") -> None:
        """
        Update the clock label based on the arrow object.

        Args:
            arrow (Arrow): The arrow object containing the data.
        """
        if arrow.rotation_direction:
            if arrow.rotation_direction == CLOCKWISE:
                clock_icon = CLOCKWISE_ICON
            elif arrow.rotation_direction == COUNTER_CLOCKWISE:
                clock_icon = COUNTER_CLOCKWISE_ICON
            else:
                clock_icon = CLOCK_ICON

            self.set_clock_pixmap(self.clock_label, clock_icon)
        else:
            self.clock_label.setText("")

    def create_info_header(
        self, text: str, alignment: Qt.AlignmentFlag, color: str
    ) -> QLabel:
        """
        Create an info header QLabel widget with the specified text, alignment, and color.

        Args:
            text (str): The text to be displayed in the info header.
            alignment (Qt.AlignmentFlag): The alignment of the info header text.
            color (str): The color of the info header text.

        Returns:
            QLabel: The created info header widget.
        """
        info_header = QLabel(text, self.attribute_panel)
        info_header.setAlignment(alignment)
        info_header.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        info_header.setStyleSheet(
            f"color: {color}; font-size: {int(self.attribute_panel.height()*0.07)}px; font-weight: bold;"
        )
        return info_header

    def create_attribute_labels(self) -> Dict[str, QLabel]:
        """
        Creates attribute labels for motion type, rotation direction, start/end, and turns.

        Returns:
            A dictionary of QLabel objects representing the attribute labels.
        """

        attribute_labels: Dict[str, QLabel] = {}

        label_names = [
            "motion_type_label",
            "start_end_label",
            "turns_label",
        ]

        color_box_height = (
            self.attribute_panel.height()
        )  # Get the height of the color box
        label_height = (
            color_box_height / 4
        )  # Set the height of the labels to be 1/4 of the color box height

        for name in label_names:
            label = QLabel()
            label.setObjectName(name)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            label.setMaximumHeight(int(label_height))
            label.setFixedWidth(self.attribute_panel.width())
            attribute_labels[name] = label

        self.motion_type_label = attribute_labels["motion_type_label"]
        self.start_end_label = attribute_labels["start_end_label"]
        self.turns_label = attribute_labels["turns_label"]

        return attribute_labels

    ### LABEL UPDATING ###

    def update_labels(self, arrow: "Arrow") -> None:
        """
        Update the labels in the infobox widget based on the arrow object.

        Args:
            widget (QFrame): The infobox widget.
            arrow (Arrow): The arrow object containing the data.

        Returns:
            None
        """

        infobox_height = (
            self.attribute_panel.height()
        )  # Get the height of the infobox widget

        self.motion_type_label.setText(
            f"<h1><span style='font-weight: bold; font-style: italic; font-size: {int(infobox_height * 0.07)}px;'>{arrow.motion_type.capitalize()}</h1>"
        )

        if arrow.rotation_direction:
            if arrow.rotation_direction == CLOCKWISE:
                clock_icon = CLOCKWISE_ICON
            elif arrow.rotation_direction == COUNTER_CLOCKWISE:
                clock_icon = COUNTER_CLOCKWISE_ICON
            else:
                clock_icon = CLOCK_ICON

            self.set_clock_pixmap(self.clock_label, clock_icon)
        else:
            self.clock_label.setText("")

        if arrow.motion_type in [PRO, ANTI, STATIC]:
            self.start_end_label.setText(
                f"<span style='font-weight: bold; font-style: italic; font-size: {int(infobox_height * 0.07)}px;'>{arrow.start_location.capitalize()} → {arrow.end_location.capitalize()}</span>"
            )
        elif arrow.motion_type == "":
            self.start_end_label.setText("")
        self.turns_label.setText(
            f"<span style='font-size: {int(infobox_height * 0.07)}px;'>{arrow.turns}</span>"
        )

    ### HELPERS ###

    def preload_pixmaps(self) -> None:
        """
        Preload and cache the pixmaps.

        This method loads and caches the pixmaps for the infobox clock.

        It scales them to a size of 60x60 pixels, and stores them in the pixmap_cache dictionary.

        Returns:
            None
        """
        for icon_name in [CLOCKWISE_ICON, COUNTER_CLOCKWISE_ICON]:
            pixmap = QPixmap(icon_name)
            scaled_pixmap = pixmap.scaled(
                int(self.attribute_panel.column_frame.height() / 3),
                int(self.attribute_panel.column_frame.height() / 3),
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
        label = QLabel(text, self.attribute_panel)  # Set attribute_panel as parent
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
