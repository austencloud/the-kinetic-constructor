from typing import TYPE_CHECKING, Dict, List
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QFrame, QVBoxLayout, QSizePolicy
from objects.motion import Motion
from constants.string_constants import (
    RED,
    RED_HEX,
    BLUE_HEX,
)
from utilities.TypeChecking.TypeChecking import Colors
from widgets.graph_editor.attr_panel.attr_box_widgets.attr_box_widget import (
    AttrBoxWidget,
)
from widgets.graph_editor.attr_panel.custom_button import CustomButton

if TYPE_CHECKING:
    from objects.pictograph.pictograph import Pictograph
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
        self.combobox_border = 2
        self.pixmap_cache: Dict[str, QPixmap] = {}  # Initialize the pixmap cache
        self.init_ui()

    def calculate_button_size(self) -> int:
        return int((self.pictograph.view.height() // 2 // 4) * 1)

    def init_ui(self):
        self.setup_box()

        # Create widgets and add them to the layout with calculated heights
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout.setSpacing(0)
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
            f"#AttributeBox {{ border: {self.border_width}px solid {color_hex}; border-style: inset; }}"
        )

    ### CREATE LABELS ###

    def clear_attr_box(self) -> None:
        self.motion_type_widget.clear_motion_type_box()
        self.start_end_widget.clear_start_end_boxes()
        self.turns_widget.turnbox.setCurrentIndex(-1)
        self.turns_widget.update_clocks(None)

    def update_attr_box(self, motion: Motion = None) -> None:
        self.turns_widget.update_clocks(motion.rotation_direction)
        self.start_end_widget.update_start_end_boxes(
            motion.start_location, motion.end_location
        )
        self.motion_type_widget.update_motion_type_box(motion.motion_type)
        if motion.rotation_direction:
            self.turns_widget.update_turnbox(motion.turns)

    def resize_attr_box(self) -> None:
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

        self.header_widget.resize_header_widget()
        self.turns_widget.resize_turns_widget()
        self.motion_type_widget.resize_motion_type_widget()
        self.start_end_widget.resize_start_end_widget()

        self.header_widget.header_label.setFont(QFont("Arial", int(self.width() / 10)))

        for button in self.findChildren(CustomButton):
            button.update_custom_button_size()
