import logging
from typing import TYPE_CHECKING, Dict, Literal
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget
from objects.arrow import Arrow
from objects.motion import Motion
from settings.string_constants import (
    ICON_DIR,
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
        # self.add_black_border_to_all_widgets()

    def calculate_button_size(self) -> int:
        return int((self.pictograph.view.height() // 2 // 4) * 1)

    def init_ui(self):
        self.setup_box()
        self.button_size = self.calculate_button_size()
        self.icon_size = QSize(int(self.button_size * 0.5), int(self.button_size * 0.5))

        self.header_widget = HeaderWidget(self)
        self.motion_type_widget = MotionTypesWidget(self)
        self.start_end_widget = StartEndWidget(self)
        self.turns_widget = TurnsWidget(self)

        self.layout().addWidget(self.header_widget)
        self.layout().addWidget(self.motion_type_widget)
        self.layout().addWidget(self.start_end_widget)
        self.layout().addWidget(self.turns_widget)

    def setup_box(self) -> None:
        self.setFixedWidth(int(self.attr_panel.width() / 2))
        self.setObjectName("AttributeBox")
        self.apply_border_style(RED_HEX if self.color == RED else BLUE_HEX)
        self.setLayout(QVBoxLayout(self))
        self.layout().setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(self.widget_spacing)

    def apply_border_style(self, color_hex: str) -> None:
        self.border_width = 3
        self.setStyleSheet(
            f"#AttributeBox {{ border: {self.border_width}px solid {color_hex}; }}"
        )
        self.attr_box_width = int(self.attr_panel.width() / 2 - self.border_width * 2)
        self.header_spacing = int(self.attr_box_width * 0.02)
        self.widget_spacing = int(self.attr_box_width * 0.00)

    ### CREATE LABELS ###

    def get_combobox_style(self) -> str:
        # ComboBox style
        return f"""
            QComboBox {{
                border: 2px solid black;
                border-radius: 10px;
            }}

            QComboBox::drop-down {{
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 15px;
                border-left-width: 1px;
                border-left-color: darkgray;
                border-left-style: solid;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }}

            QComboBox::down-arrow {{
                image: url('{ICON_DIR}combobox_arrow.png');
                width: 10px;
                height: 10px;
            }}
        """

    def clear_attr_box(self) -> None:
        self.motion_type_widget.clear_motion_type_box()
        self.start_end_widget.clear_start_end_boxes()
        self.turns_widget.clear_turns_label()

    def update_attr_box(self, motion: Motion = None) -> None:
        if motion:
            self.turns_widget.update_clocks(motion.rotation_direction)
            self.start_end_widget.update_start_end_boxes(
                motion.start_location, motion.end_location
            )
            self.motion_type_widget.update_motion_type_box(motion.motion_type)
            self.turns_widget.update_turns_label_box(motion.turns)
        else:
            self.clear_attr_box()

    def update_attr_box_size(self) -> None:
        self.setFixedWidth(
            int(
                (
                    self.attr_panel.pictograph.graph_editor.width()
                    - self.attr_panel.pictograph.graph_editor.arrowbox.view.width()
                    - self.attr_panel.pictograph.view.width()
                )
                / 2
            )
        )
        self.setMaximumHeight(self.attr_panel.height())
        self.header_widget.update_header_widget_size()
        self.motion_type_widget.update_motion_type_widget_size()
