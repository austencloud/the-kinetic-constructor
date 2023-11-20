import logging
from typing import TYPE_CHECKING, Dict

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QPushButton,
    QSpacerItem,
    QWidget,
)

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
    ICON_PATHS,
    RED_HEX,
    BLUE_HEX,
)
from utilities.TypeChecking.TypeChecking import Color
from PyQt6.QtGui import QIcon


if TYPE_CHECKING:
    from widgets.graph_editor.graphboard.graphboard import GraphBoard
    from widgets.graph_editor.infobox.attribute_panel.attribute_panel import (
        AttributePanel,
    )


class AttributeBox(QFrame):
    def __init__(
        self, attribute_panel: "AttributePanel", graphboard: "GraphBoard", color: Color
    ) -> None:
        self.attribute_panel = attribute_panel
        self.graphboard = graphboard
        self.color = color

        super().__init__(self.attribute_panel)
        self.setObjectName("AttributeBox")
        border_color = RED_HEX if color == RED else BLUE_HEX
        self.setStyleSheet(f"#AttributeBox {{ border: 2px solid {border_color}; }}")

        self.pixmap_cache: Dict[str, QPixmap] = {}

        header_text = {BLUE: "Left", RED: "Right"}.get(color, "")
        header_color = {BLUE: BLUE, RED: RED}.get(color, "")

        self.setLayout(QVBoxLayout(self))

        self.info_header = self.create_info_header(
            header_text, Qt.AlignmentFlag.AlignCenter, header_color
        )
        self.layout().addWidget(self.info_header)

        self.setFixedHeight(int(self.attribute_panel.height() / 2))
        self.setFixedWidth(int(self.attribute_panel.width()))

        self.setContentsMargins(0, 0, 0, 0)  # Remove padding on the edges
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.attribute_labels = self.create_attribute_labels()
        self.clock_label = self.create_clock_label()  # Create the clock label
        self.layout().addWidget(self.info_header)
        for label in self.attribute_labels.values():
            self.layout().addWidget(label)

        self.setup_left_button_column()
        self.setup_right_button_column()

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
    ) -> QWidget:
        """
        Create an info header QLabel widget with the specified text, alignment, and color.

        Args:
            text (str): The text to be displayed in the info header.
            alignment (Qt.AlignmentFlag): The alignment of the info header text.
            color (str): The color of the info header text.

        Returns:
            QVBoxLayout: The layout containing the created info header widget and the underline.
        """
        info_header = QLabel(text, self.attribute_panel)
        info_header.setAlignment(alignment)
        info_header.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        header_color = RED_HEX if color == RED else BLUE_HEX
        info_header.setStyleSheet(
            f"color: {header_color}; font-size: {int(self.attribute_panel.height()*0.07)}px; font-weight: bold;"
        )

        # Create a QFrame to act as an underline
        underline = QFrame()
        underline.setFixedHeight(1)  # Set the height to 1 to create a line effect
        underline.setStyleSheet("background-color: black;")

        # Create a layout to hold the header and the underline
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(info_header)
        layout.addWidget(underline)

        widget = QWidget()
        widget.setLayout(layout)

        return widget

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

    def setup_right_button_column(self):
        buttonColumnFrame = QFrame(self)
        buttonColumnLayout = QVBoxLayout(buttonColumnFrame)
        buttonColumnFrame.setLayout(buttonColumnLayout)
        buttonColumnLayout.setContentsMargins(0, 0, 0, 0)
        buttonColumnLayout.setSpacing(0)

        buttonSize = self.height() // 4
        buttonColumnFrame.setFixedSize(buttonSize, self.height())

        # Add spacers to push the button to the bottom
        for _ in range(3):
            spacer = QSpacerItem(
                buttonSize,
                buttonSize,
                QSizePolicy.Policy.Fixed,
                QSizePolicy.Policy.Fixed,
            )
            buttonColumnLayout.addItem(spacer)


        increment_turns_button = QPushButton(buttonColumnFrame)
        increment_turns_button.setIcon(QIcon(ICON_PATHS["increment_turns"]))
        increment_turns_button.clicked.connect(
            lambda: self.graphboard.get_arrow_by_color(self.color).add_turn()
        )
        increment_turns_button.setFixedSize(buttonSize, buttonSize)


        icon_size = int(buttonSize * 0.6)
        increment_turns_button.setIconSize(QSize(icon_size, icon_size))

        buttonColumnLayout.addWidget(increment_turns_button)

        buttonColumnFrame.move(self.width() - buttonSize, 0) 
        buttonColumnFrame.raise_()

    def setup_left_button_column(self):
        buttonColumnFrame = QFrame(self)
        buttonColumnLayout = QVBoxLayout(buttonColumnFrame)
        buttonColumnFrame.setLayout(buttonColumnLayout)
        buttonColumnLayout.setContentsMargins(0, 0, 0, 0)
        buttonColumnLayout.setSpacing(0)

        buttonSize = self.height() // 4
        buttonColumnFrame.setFixedSize(buttonSize, self.height())

        # Top spacer to push the buttons down
        top_spacer = QSpacerItem(
            buttonSize, buttonSize, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed
        )
        buttonColumnLayout.addItem(top_spacer)

        # Define the button functionalities based on the color
        button_functions = [
            (
                "swap_motion_type",
                lambda: self.graphboard.get_arrow_by_color(
                    self.color
                ).swap_motion_type(),
            ),
            (
                "swap_start_end",
                lambda: self.graphboard.get_arrow_by_color(self.color).swap_rot_dir(),
            ),
            (
                "decrement_turns",
                lambda: self.graphboard.get_arrow_by_color(self.color).subtract_turn(),
            ),
        ]

        # Create and add buttons with the functionalities
        for func_name, callback in button_functions:
            button = QPushButton(buttonColumnFrame)
            button.setIcon(QIcon(ICON_PATHS[func_name]))
            button.clicked.connect(callback)
            button.setFixedSize(buttonSize, buttonSize)

            # Set the icon size to 85% of the button size
            icon_size = int(buttonSize * 0.6)
            button.setIconSize(QSize(icon_size, icon_size))

            buttonColumnLayout.addWidget(button)

        buttonColumnFrame.move(0, 0)  # Position to the left
        buttonColumnFrame.raise_()

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
        Preloads and caches pixmaps for the attribute panel.

        This method loads the pixmaps for the CLOCKWISE_ICON and COUNTER_CLOCKWISE_ICON
        and scales them to a size that is one-third of the height of the attribute panel's
        column frame. The scaled pixmaps are then stored in the pixmap_cache dictionary.
        """
        for icon_name in [CLOCKWISE_ICON, COUNTER_CLOCKWISE_ICON]:
            pixmap = QPixmap(icon_name)
            scaled_pixmap = pixmap.scaled(
                int(self.height() / 4),
                int(self.height() / 4),
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
