import logging
from typing import TYPE_CHECKING, Dict, Literal
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)
from objects.motion import Motion
from settings.string_constants import (
    RED,
    ICON_PATHS,
    RED_HEX,
    BLUE_HEX,
)
from utilities.TypeChecking.TypeChecking import Colors

if TYPE_CHECKING:
    from widgets.graph_editor.pictograph.pictograph import Pictograph
    from widgets.graph_editor.attr_panel.attr_panel import (
        AttrPanel,
    )
from widgets.graph_editor.attr_panel.attr_box_widgets.header_widget import HeaderWidget
from widgets.graph_editor.attr_panel.attr_box_widgets.motion_types_widget import (
    MotionTypesWidget,
)
from widgets.graph_editor.attr_panel.attr_box_widgets.start_end_widget import (
    StartEndWidget,
)
from widgets.graph_editor.attr_panel.attr_box_widgets.turns_widget import TurnsWidget


class AttrBox(QFrame):
    def __init__(
        self, attr_panel: "AttrPanel", pictograph: "Pictograph", color: Colors
    ) -> None:
        super().__init__(attr_panel)
        self.attr_panel = attr_panel
        self.pictograph = pictograph
        self.color = color
        self.turns_widget = None
        self.pixmap_cache: Dict[str, QPixmap] = {}  # Initialize the pixmap cache
        self.init_ui()


    def calculate_button_size(self) -> int:
        return int((self.pictograph.view.height() // 2 // 4) * 1)

    def init_ui(self):
        self.setup_box()
        self.button_size = self.calculate_button_size()
        self.icon_size = QSize(int(self.button_size * 0.5), int(self.button_size * 0.5))

        self.header_widget = HeaderWidget(self, self.color)
        self.motion_type_widget = MotionTypesWidget(self)
        self.start_end_widget = StartEndWidget(self)
        self.turns_widget = TurnsWidget(self.pictograph, self.color, self)

        self.layout().addWidget(self.header_widget)
        self.layout().addWidget(self.motion_type_widget)
        self.layout().addWidget(self.start_end_widget)
        self.layout().addWidget(self.turns_widget)

    def setup_box(self) -> None:
        self.setObjectName("AttributeBox")
        self.apply_border_style(RED_HEX if self.color == RED else BLUE_HEX)
        self.setFixedSize(
            int(self.attr_panel.width() / 2), int(self.attr_panel.height())
        )
        self.setLayout(QVBoxLayout(self))
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(self.widget_spacing)

    def apply_border_style(self, color_hex: str) -> None:
        self.border_width = 3
        self.setStyleSheet(
            f"#AttributeBox {{ border: {self.border_width}px solid {color_hex}; }}"
        )
        self.attr_box_width = int(self.attr_panel.width()/2)
        self.header_spacing = int(self.attr_box_width * 0.02)
        self.widget_spacing = int(self.attr_box_width * 0.05)

    ### CREATE LABELS ###

    def create_attribute_labels(self) -> Dict[str, QLabel]:
        labels = {}
        for name in [
            "motion_type_label",
            "start_end_label",
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

    def preload_pixmaps(self) -> None:
        for icon_name, icon_path in ICON_PATHS.items():
            if not icon_path:
                logging.warning(f"No file path specified for icon '{icon_name}'.")
                continue
            pixmap = QPixmap(icon_path)
            if pixmap.isNull():
                logging.error(
                    f"Failed to load icon '{icon_name}' from path '{icon_path}'."
                )
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

    def update_attr_box(self) -> None:
        motion = self.pictograph.get_motion_by_color(self.color)
        if motion:
            self.update_labels(motion)

    def update_labels(self, motion: "Motion") -> None:
        self.start_end_widget.update_start_end_boxes()
        self.motion_type_widget.update_motion_type_box()
        self.turns_widget.turns_label.setText(f"{motion.turns}")

    def get_turns_button_stylesheet(self, button: Literal["small", "large"]) -> str:
        if button == "small":
            size = self.width() / 7
        elif button == "large":
            size = self.width() / 5

        border_radius = size / 2

        return (
            f"QPushButton {{"
            f"   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(255, 255, 255, 255), stop:1 rgba(200, 200, 200, 255));"
            f"   border-radius: {border_radius}px;"
            f"   border: 1px solid black;"
            f"   min-width: {size}px;"
            f"   min-height: {size}px;"  # Adjust height to match width for a circle
            f"   max-width: {size}px;"
            f"   max-height: {size}px;"
            f"}}"
            f"QPushButton:hover {{"
            f"   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(230, 230, 230, 255), stop:1 rgba(200, 200, 200, 255));"
            f"}}"
            f"QPushButton:pressed {{"
            f"   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 rgba(204, 228, 247, 255), stop:1 rgba(164, 209, 247, 255));"
            f"}}"
        )

    def get_combobox_style(self) -> str:
        # ComboBox style
        return (
            "QComboBox {"
            "   border: 2px solid black;"
            "   border-radius: 10px;"
            "}"
            "QComboBox::drop-down {"
            "   subcontrol-origin: padding;"
            "   subcontrol-position: top right;"
            "   width: 15px;"
            "   border-left-width: 1px;"
            "   border-left-color: darkgray;"
            "   border-left-style: solid;"
            "   border-top-right-radius: 3px;"
            "   border-bottom-right-radius: 3px;"
            "}"
            "QComboBox::down-arrow {"
            "   image: url('resources/images/icons/combobox_arrow.png');"
            "   width: 10px;"
            "   height: 10px;"
            "}"
        )

    def clear_attr_box(self):
        # Clear all attributes in the attribute box
        # You might want to clear labels, reset combo boxes, etc.
        self.motion_type_widget.clear_motion_type_box()
        self.start_end_widget.clear_start_end_boxes()
        self.turns_widget.clear_turns_label()

    # Update the update_attr_box method to only update when the corresponding arrow is selected
    def update_attr_box(self, arrow=None):
        if arrow:
            self.update_labels(arrow)
        else:
            self.clear_attr_box()

    def update_attr_box_size(self) -> None:
        self.setFixedHeight(int(self.attr_panel.height()))
        self.setFixedWidth(int(self.attr_panel.width() / 2))
        for child in self.children():
            if isinstance(child, QFrame):
                child.deleteLater()

        if self.turns_widget:
            for child in self.turns_widget.children():
                if isinstance(child, QFrame):
                    child.deleteLater()
        self.update()

        self.header_widget.update_header_widget_size()
        self.motion_type_widget.update_motion_type_widget_size()
        self.start_end_widget.update_start_end_widget_size()
        self.turns_widget.update_turns_widget_size()
