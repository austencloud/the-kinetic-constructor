from typing import TYPE_CHECKING, Dict, List
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QWidget, QSizePolicy
from objects.motion import Motion
from settings.string_constants import (
    ICON_DIR,
    RED,
    RED_HEX,
    BLUE_HEX,
)
from utilities.TypeChecking.TypeChecking import Colors
from widgets.graph_editor.attr_panel.attr_box_widgets.attr_box_widget import (
    AttrBoxWidget,
)

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
        self.font_size = self.width() // 10
        self.widgets: List[AttrBoxWidget] = []

        self.pixmap_cache: Dict[str, QPixmap] = {}  # Initialize the pixmap cache
        self.init_ui()

    def calculate_button_size(self) -> int:
        return int((self.pictograph.view.height() // 2 // 4) * 1)

    def init_ui(self):
        self.setup_box()

        # Create widgets and add them to the layout with calculated heights
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Initialize and set maximum heights for child widgets
        self.header_widget = HeaderWidget(self)
        self.motion_type_widget = MotionTypesWidget(self)
        self.start_end_widget = StartEndWidget(self)
        self.turns_widget = TurnsWidget(self)

        # Add child widgets to the layout
        self.layout.addWidget(self.header_widget)
        self.layout.addWidget(self.motion_type_widget)
        self.layout.addWidget(self.start_end_widget)
        self.layout.addWidget(self.turns_widget)

        # Apply the layout to the AttrBox
        self.setLayout(self.layout)

        # Set the AttrBox to have a dynamic size based on its content
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

    def setup_box(self) -> None:
        self.setObjectName("AttributeBox")
        self.apply_border_style(RED_HEX if self.color == RED else BLUE_HEX)

    def apply_border_style(self, color_hex: str) -> None:
        self.border_width = 3
        self.setStyleSheet(
            f"#AttributeBox {{ border: {self.border_width}px solid {color_hex}; }}"
        )

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
        self.turns_widget.turnbox.setCurrentIndex(-1)

    def update_attr_box(self, motion: Motion = None) -> None:
        if motion:
            self.turns_widget.update_clocks(motion.rotation_direction)
            self.start_end_widget.update_start_end_boxes(
                motion.start_location, motion.end_location
            )
            self.motion_type_widget.update_motion_type_box(motion.motion_type)
            self.turns_widget.update_turnbox(motion.turns)
        else:
            self.clear_attr_box()

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self.setMinimumWidth(int(self.pictograph.view.width() * 0.85))
        self.setMaximumWidth(int(self.pictograph.view.width() * 0.85))
        self.header_spacing = int(self.width() * 0.02)
        ratio_total = 1 + 1 + 1 + 2
        available_height = self.height()
        header_height = int(available_height * (1 / ratio_total))
        motion_types_height = int(available_height * (1 / ratio_total))
        start_end_height = int(available_height * (1 / ratio_total))
        turns_widget_height = int(available_height * (2 / ratio_total))
        self.header_widget.setMaximumHeight(header_height)
        self.motion_type_widget.setMaximumHeight(motion_types_height)
        self.start_end_widget.setMaximumHeight(start_end_height)
        self.turns_widget.setMaximumHeight(turns_widget_height)
