import logging
from typing import TYPE_CHECKING, Literal, Dict
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QSpacerItem,
    QWidget,
)

from data.positions_map import positions_map
from objects.arrow import Arrow
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

if TYPE_CHECKING:
    from widgets.graph_editor.graphboard.graphboard import GraphBoard
    from widgets.graph_editor.attribute_panel.attribute_panel import (
        AttributePanel,
    )
    from objects.ghosts.ghost_arrow import GhostArrow
from PyQt6.QtWidgets import QSizePolicy


class AttributeBox(QFrame):
    def __init__(
        self, attribute_panel: "AttributePanel", graphboard: "GraphBoard", color: Color
    ) -> None:
        super().__init__(attribute_panel)
        self.attribute_panel = attribute_panel
        self.graphboard = graphboard
        self.color = color
        self.pixmap_cache: Dict[str, QPixmap] = {}  # Initialize the pixmap cache
        self.init_ui()

    def calculate_button_size(self) -> int:
        return int((self.graphboard.view.height() // 2 // 4) * 1)

    def init_ui(self) -> None:
        self.setup_box()
        self.button_size = self.calculate_button_size()  # Re-implemented button size
        self.icon_size = QSize(
            int(self.button_size * 0.6), int(self.button_size * 0.6)
        )  # Re-implemented icon size

        self.info_header = self.create_info_header(
            "Left" if self.color == BLUE else "Right", self.color
        )

        # self.layout().addWidget(self.info_header)
        self.attribute_labels = self.create_attribute_labels()
        self.clock_label = self.create_clock_label()
        self.add_labels_to_layout()

        self.left_button_column = self.setup_button_column(
            0, ["swap_motion_type", "swap_start_end", "decrement_turns"], column="left"
        )
        self.right_button_column = self.setup_button_column(
            self.width() - self.button_size, ["increment_turns"], column="right"
        )
        self.preload_pixmaps()

    def setup_box(self) -> None:
        self.setObjectName("AttributeBox")
        self.apply_border_style(RED_HEX if self.color == RED else BLUE_HEX)
        self.setFixedSize(
            int(self.attribute_panel.width()), int(self.attribute_panel.height() / 2)
        )
        self.setLayout(QVBoxLayout(self))
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def apply_border_style(self, color_hex: str) -> None:
        self.setStyleSheet(f"#AttributeBox {{ border: 2px solid {color_hex}; }}")

    ### CREATE LABELS ###

    def create_info_header(self, text: str, color: Color) -> QLabel:
        info_header = QLabel(text, self)
        info_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        info_header.setFixedHeight(int(self.height() / 4))

        color_hex = RED_HEX if color == RED else BLUE_HEX
        info_header.setStyleSheet(
            f"color: {color_hex}; font-size: {int(self.height() * 0.07)}px; font-weight: bold;"
        )
        info_header.setStyleSheet(
            f"color: {color_hex}; font-size: {int(self.height() * 0.14)}px; font-weight: bold;"
        )
        return info_header

    def create_attribute_labels(self) -> Dict[str, QLabel]:
        labels = {}
        for name in [
            "motion_type_label",
            "start_end_label",
            "turns_label",
        ]:
            label = self.create_label(self.height() // 4)
            label.setObjectName(name)
            labels[name] = label
        return labels

    def create_label(self, height: int) -> QLabel:
        label = QLabel(self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setFixedSize(self.width(), height)
        return label

    def create_clock_label(self) -> QLabel:
        label = self.create_label(self.height() // 4)
        label.setObjectName("clock_label")
        return label

    def add_labels_to_layout(self) -> None:
        self.layout().addWidget(self.info_header)
        for label in self.attribute_labels.values():
            self.layout().addWidget(label)

    def setup_button_column(self, x_position: int, button_names: list, column: Literal["left", "right"]) -> None:
        button_column_frame = QFrame(self)
        button_column_layout = QVBoxLayout(button_column_frame)
        button_column_layout.setContentsMargins(0, 0, 0, 0)
        button_column_layout.setSpacing(0)

        button_column_frame.setFixedSize(self.button_size, self.height())
        button_column_frame.move(x_position, 0)

        # For the left column, add a spacer at the top
        if column == "left":
            top_spacer = QSpacerItem(
                self.button_size,
                self.button_size,
                QSizePolicy.Policy.Fixed,
                QSizePolicy.Policy.Expanding
            )
            button_column_layout.addItem(top_spacer)

        # For the right column, add the clock label at the top
        if column == "right":
            button_column_layout.addWidget(self.clock_label)

        # Add spacer(s)
        middle_spacer = QSpacerItem(
            self.button_size,
            self.button_size,
            QSizePolicy.Policy.Fixed,
            QSizePolicy.Policy.Expanding
        )
        button_column_layout.addItem(middle_spacer)

        # For the left column, add the buttons
        if column == "left":
            for button_name in button_names:
                button = self.create_button(
                    ICON_PATHS[button_name], getattr(self, f"{button_name}_callback")
                )
                button_column_layout.addWidget(button)

        # For the right column, add the increment button at the bottom
        if column == "right" and "increment_turns" in button_names:
            increment_button = self.create_button(
                ICON_PATHS["increment_turns"], self.increment_turns_callback
            )
            button_column_layout.addWidget(increment_button)

        button_column_frame.raise_()
        return button_column_frame
        
    def create_button(self, icon_path: str, callback) -> QPushButton:
        button = QPushButton(self)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(self.icon_size)  # Use the re-implemented icon size
        button.setFixedSize(
            self.button_size, self.button_size
        )  # Use the re-implemented button size
        button.clicked.connect(callback)
        return button

    # Button Callbacks
    def swap_motion_type_callback(self) -> None:
        arrow = self.graphboard.get_arrow_by_color(self.color)
        if arrow:
            arrow.swap_motion_type()
            self.update_labels(arrow)

    def swap_start_end_callback(self) -> None:
        arrow = self.graphboard.get_arrow_by_color(self.color)
        if arrow:
            arrow.swap_rot_dir()
            self.update_labels(arrow)

    def decrement_turns_callback(self) -> None:
        arrow = self.graphboard.get_arrow_by_color(self.color)
        if arrow:
            arrow.subtract_turn()
            self.update_labels(arrow)

    def increment_turns_callback(self) -> None:
        arrow = self.graphboard.get_arrow_by_color(self.color)
        if arrow:
            arrow.add_turn()
            self.update_labels(arrow)
    
    def preload_pixmaps(self) -> None:
        # Preloads pixmaps for the icons
        for icon_name, icon_path in ICON_PATHS.items():
            if not icon_path:  # Check if the path is empty
                logging.warning(f"No file path specified for icon '{icon_name}'.")
                continue
            pixmap = QPixmap(icon_path)
            if pixmap.isNull():  # Check if the QPixmap could not load the image
                logging.error(f"Failed to load icon '{icon_name}' from path '{icon_path}'.")
                continue
            scaled_pixmap = pixmap.scaled(
                self.button_size,
                self.button_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.pixmap_cache[icon_name] = scaled_pixmap
    
    def set_clock_pixmap(self, clock_label: QLabel, icon_name: str) -> None:
        if icon_name not in self.pixmap_cache:
            logging.error(f"Icon name '{icon_name}' not found in pixmap cache.")
            return
        pixmap = self.pixmap_cache[icon_name]
        if pixmap.isNull():
            logging.error(f"Pixmap for icon name '{icon_name}' is null.")
            return
        clock_label.setPixmap(pixmap)
        
    def update_attribute_box(self) -> None:
        arrow = self.graphboard.get_arrow_by_color(self.color)
        if arrow:
            self.update_labels(arrow)

    def update_labels(self, arrow: "Arrow") -> None:
        """
        Update the labels in the infobox widget based on the arrow object.

        Args:
            widget (QFrame): The infobox widget.
            arrow (Arrow): The arrow object containing the data.

        Returns:
            None
        """

        infobox_height = self.attribute_panel.height()
        self.attribute_labels["motion_type_label"].setText(
            f"<h1><span style='font-weight: bold; font-style: italic; font-size: {int(infobox_height * 0.07)}px;'>{arrow.motion_type.capitalize()}</h1>"
        )

        # if arrow.rotation_direction:
        #     if arrow.rotation_direction == CLOCKWISE:
        #         clock_icon = CLOCKWISE_ICON
        #     elif arrow.rotation_direction == COUNTER_CLOCKWISE:
        #         clock_icon = COUNTER_CLOCKWISE_ICON
        #     else:
        #         clock_icon = CLOCK_ICON

        #     self.set_clock_pixmap(self.attribute_labels["clock_label"], clock_icon)
        # else:
        #     self.attribute_labels["clock_label"].setText("")

        if arrow.motion_type in [PRO, ANTI, STATIC]:
            self.attribute_labels["start_end_label"].setText(
                f"<span style='font-weight: bold; font-style: italic; font-size: {int(infobox_height * 0.07)}px;'>{arrow.start_location.capitalize()} → {arrow.end_location.capitalize()}</span>"
            )
        elif arrow.motion_type == "":
            self.attribute_labels["start_end_label"].setText("")
        self.attribute_labels["turns_label"].setText(
            f"<span style='font-size: {int(infobox_height * 0.07)}px;'>{arrow.turns}</span>"
        )


    def update_button_size(self) -> None:
        self.button_size = self.calculate_button_size()  # Re-implemented button size
        self.icon_size = QSize(
            int(self.button_size * 0.6), int(self.button_size * 0.6)
        )  # Re-implemented icon size
        for child in self.children():
            if isinstance(child, QPushButton):
                child.setFixedSize(self.button_size, self.button_size)
                child.setIconSize(self.icon_size)
        for child in self.clock_label.children():
            if isinstance(child, QLabel):
                child.setFixedSize(self.button_size, self.button_size)
                child.setPixmap(child.pixmap().scaled(self.button_size, self.button_size, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.update()
        

        
    def update_attribute_box_size(self) -> None:
        self.setFixedHeight(int(self.attribute_panel.graphboard.graph_editor.height() / 2))
        self.setFixedWidth(int(self.attribute_panel.graphboard.graph_editor.height() / 2))
        #delete the buttons layouts 
        for child in self.children():
            if isinstance(child, QFrame):
                child.deleteLater()
        self.init_ui()
        self.update()
        