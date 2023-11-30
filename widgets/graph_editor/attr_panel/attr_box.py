import logging
from typing import TYPE_CHECKING, Dict
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QPushButton,
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

    def calculate_button_size(self) -> int:
        return int((self.pictograph.view.height() // 2 // 4) * 1)

    def init_ui(self):
        self.setup_box()
        self.button_size = self.calculate_button_size()
        self.icon_size = QSize(int(self.button_size * 0.5), int(self.button_size * 0.5))

        self.header_widget = HeaderWidget(self, self.color)
        self.motion_type_widget = MotionTypesWidget(self)
        self.start_end_widget = StartEndWidget(self.pictograph, self.color, self)
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
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

    def apply_border_style(self, color_hex: str) -> None:
        self.border_width = 5
        self.setStyleSheet(
            f"#AttributeBox {{ border: {self.border_width}px solid {color_hex}; }}"
        )
        self.attr_box_width = int(self.width())

    def get_button_style(self) -> str:
        return (
            "QPushButton {"
            "   border-radius: 15px;"
            "   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "   stop:0 rgba(255, 255, 255, 255), stop:1 rgba(229, 229, 229, 255));"
            "   border: 1px solid #8f8f91;"
            "   min-width: 30px;"
            "   min-height: 30px;"
            "}"
            "QPushButton:pressed {"
            "   background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, "
            "   stop:0 rgba(204, 228, 247, 255), stop:1 rgba(164, 209, 247, 255));"
            "}"
            "QPushButton:hover:!pressed {"
            "   border: 1px solid #1c1c1c;"
            "}"
        )

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

    def create_button(self, icon_path, callback):
        button = QPushButton(self)
        button.setIcon(QIcon(icon_path))
        button.setIconSize(self.icon_size)
        button.setFixedSize(self.button_size, self.button_size)
        button.clicked.connect(callback)

        # Return the button without setting a stylesheet
        return button

    def swap_motion_type_callback(self) -> None:
        arrow = self.pictograph.get_arrow_by_color(self.color)
        if arrow:
            arrow.swap_motion_type()
            self.update_labels(arrow)

    def swap_start_end_callback(self) -> None:
        arrow = self.pictograph.get_arrow_by_color(self.color)
        if arrow:
            arrow.swap_rot_dir()
            self.update_labels(arrow)

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
        arrow = self.pictograph.get_arrow_by_color(self.color)
        if arrow:
            self.update_labels(arrow)

    def update_labels(self, motion: "Motion") -> None:
        self.start_end_widget.update_combo_boxes()
        self.turns_widget.turns_label.setText(f"{motion.turns}")

    def update_attr_box_size(self) -> None:
        self.setFixedHeight(int(self.attr_panel.pictograph.graph_editor.height() / 2))
        self.setFixedWidth(int(self.attr_panel.pictograph.graph_editor.height() / 2))
        for child in self.children():
            if isinstance(child, QFrame):
                child.deleteLater()

        if self.turns_widget:
            for child in self.turns_widget.children():
                if isinstance(child, QFrame):
                    child.deleteLater()
        self.init_ui()
        self.header_widget.setup_header_widget()
        self.update()

        self.header_widget.update_header_widget_size()
        self.motion_type_widget.update_motion_type_widget_size()
        self.start_end_widget.update_start_end_widget_size()
        self.turns_widget.update_turns_widget_size()
